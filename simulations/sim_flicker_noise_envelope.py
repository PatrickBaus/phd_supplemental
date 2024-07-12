#!/usr/bin/env python
# pylint: disable=duplicate-code
import argparse
import os
import random

import allantools as at
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import seaborn as sns

from markov_chain import ContinuousTimeMarkovModel

colors = sns.color_palette("colorblind")
__version__ = "0.9.0"

# Use these settings for the PhD thesis
tex_fonts = {
    "text.usetex": True,  # Use LaTeX to write all text
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pgf.rcfonts": False,  # don't setup fonts from rc parameters
    "text.latex.preamble": "\n".join(
        [  # plots will use this preamble
            r"\usepackage{siunitx}",
        ]
    ),
    "pgf.preamble": "\n".join(
        [  # plots will use this preamble
            r"\usepackage{siunitx}",
        ]
    ),
    "savefig.directory": os.path.dirname(__file__),
}
plt.rcParams.update(tex_fonts)
plt.style.use("seaborn-v0_8-colorblind")
# end of settings


def gen_burst_noise(
    number_of_samples: int,
    samplerate: float,
    tau1: float,
    tau0: float = 1,
    std_gaussian_noise: float = 0,
    uniform_noise: float = 0,
    offset: float = 0,
) -> np.ndarray:
    rts_model = ContinuousTimeMarkovModel(
        ["down", "up"],
        [1 / tau0 / samplerate, 1 / tau1 / samplerate],
        np.array([[0.0, 1], [1, 0]]),
    )

    data = rts_model.generate_sequence(number_of_samples, delta_time=1, seed=42)

    if uniform_noise != 0:
        data = data + uniform_noise * (
            np.random.rand(
                data.size,
            )
            - 0.5
        )
    if std_gaussian_noise != 0:
        data = data + np.random.normal(0, std_gaussian_noise, data.size)
    return data + offset


def burst_noise_psd(f, tau1, tau0=1):
    return 4 / ((tau1 + tau0) * ((1 / tau1 + 1 / tau0) ** 2 + f**2 * (4 * np.pi**2)))


def burst_noise_adev(T, tau1, tau0=1, delta_y=1):
    Rxx0 = delta_y**2 * (tau1 * tau0) / (tau1 + tau0) ** 2
    tau_mean = 1 / (1 / tau1 + 1 / tau0)

    avar = (
        Rxx0 * tau_mean**2 / T**2 * (4 * np.exp(-T / tau_mean) - np.exp(-2 * T / tau_mean) + 2 * T / tau_mean - 3)
    )
    return np.sqrt(avar)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PID simulator.")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
    parser.add_argument('--silent', action='store_true', help="Do not show the plot when set.")

    return parser


if __name__ == "__main__":
    np.random.seed(42)
    random.seed(42)

    parser = init_argparse()
    args = parser.parse_args()

    # We misuse a python dict, which maintains insertion order, as an ordered set
    PLOTS_TO_SHOW = dict.fromkeys(
        [
            "amplitude",
            "psd",
            "adev",
        ]
    )
    PLOTS_TO_SHOW = dict.fromkeys(
        [
            "psd",
        ]
    )
    PLOT_DIRECTION = "vertical"  # or "horizontal"
    PLOT_DIRECTION = "horizontal"  # or "vertical"

    N_PER_SEG = 100
    N = int(20e6) if "adev" in PLOTS_TO_SHOW else int(2e6)  # use 20e6 for the adev plot else 2e6
    FS = 2e2

    TAU1S = [0.01, 0.1, 1, 10]
    # tau1s = [1, ]
    TAU_COLORS = (colors[0], colors[2], colors[3], colors[4])

    # compute amplitude time series
    amplitudes = [
        gen_burst_noise(number_of_samples=N, samplerate=FS, tau1=tau1, tau0=tau1, offset=i) for i, tau1 in enumerate(TAU1S)
    ]

    if "adev" in PLOTS_TO_SHOW:
        # compute ADEV
        taus = np.logspace(-2, 2, num=20)
        adevs = [at.oadev(noise, data_type="freq", rate=FS, taus=taus)[:2] for noise in amplitudes]

    fig, axs = plt.subplots(
        len(PLOTS_TO_SHOW) if PLOT_DIRECTION != "horizontal" else 1,
        len(PLOTS_TO_SHOW) if PLOT_DIRECTION == "horizontal" else 1,
        layout="constrained",
    )
    axs = (
        [
            axs,
        ]
        if len(PLOTS_TO_SHOW) == 1
        else axs
    )

    # Amplitude plot
    if "amplitude" in PLOTS_TO_SHOW:
        number_point_to_plot = 2000
        ax = axs[list(PLOTS_TO_SHOW).index("amplitude")]
        for i, (tau1, amplitude) in enumerate(zip(TAU1S, amplitudes)):
            ax.step(
                np.arange(number_point_to_plot) / FS,
                amplitude[:number_point_to_plot],
                label=f"$\\bar\\tau_1=\\qty{{{tau1}}}{{\\s}}$",
                color=TAU_COLORS[i]
            )
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.legend(loc="upper right")
        ax.set_xlabel(r"Time in \unit{\second}")
        ax.set_ylabel(r"Amplitude in arb. unit")

    # PSD plot
    if "psd" in PLOTS_TO_SHOW:
        ax = plt.subplot(
            len(PLOTS_TO_SHOW) if PLOT_DIRECTION != "horizontal" else 1,
            len(PLOTS_TO_SHOW) if PLOT_DIRECTION == "horizontal" else 1,
            list(PLOTS_TO_SHOW).index("psd") + 1,
        )

        freqs = np.logspace(-2, 2, num=20)
        for i, tau1 in enumerate(TAU1S):
            (lines,) = ax.loglog(
                freqs,
                [burst_noise_psd(freq, tau1, tau1) for freq in freqs],
                "--",
                label=f"$\\bar\\tau_1=\\tau_0=\\qty{{{tau1}}}{{\\s}}$",
                color=TAU_COLORS[i]
            )

        ax.loglog(
            freqs,
            np.add.reduce([[burst_noise_psd(freq, tau1, tau1) for freq in freqs] for tau1 in TAU1S]),
            "-",
            color="black",
            label="Envelope",
        )

        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(1e-4, 1e1)  # Set limits, so that all plots look the same
        ax.legend(loc="lower left")
        # ax.set_title(r'Frequency Power Spectral Density')
        ax.set_xlabel(r"Frequency in $\unit{\Hz}$")
        ax.set_ylabel(r"$S_y(f)$ in $\unit{1 \per \Hz}$")

    # ADEV plot
    if "adev" in PLOTS_TO_SHOW:
        ax = plt.subplot(
            len(PLOTS_TO_SHOW) if PLOT_DIRECTION != "horizontal" else 1,
            len(PLOTS_TO_SHOW) if PLOT_DIRECTION == "horizontal" else 1,
            list(PLOTS_TO_SHOW).index("adev") + 1,
        )
        plt.gca().set_prop_cycle(None)  # Reset the color cycle

        for i, (tau1, (taus, adev)) in enumerate(zip(TAU1S, adevs)):
            (lines,) = ax.loglog(taus, [burst_noise_adev(T=tau, tau1=tau1, tau0=1) for tau in taus], "--")
            ax.loglog(
                taus,
                adev,
                "o",
                markersize=3,
                label=f"$\\bar\\tau_1=\\qty{{{tau1}}}{{\\s}}$",
                color=lines.get_color(),
            )

        ax.legend(loc="upper right")
        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        # ax.set_ylim(1e-2, 1e4)  # Set limits, so that all plots look the same
        ax.set_xlabel(r"$\tau$ in \unit{\second}")
        ax.set_ylabel(r"ADEV $\sigma_A(\tau)$")

    # fig.set_size_inches(11.69,8.27)   # A4 in inch
    # fig.set_size_inches(128/25.4 * 2.7 * 0.8, 96/25.4 * 1.5 * 0.8)  # Latex Beamer size 128 mm by 96 mm
    phi = (5**0.5 - 1) / 2 if PLOT_DIRECTION == "horizontal" else (5**0.5 + 1) / 2  # golden ratio
    scale = 0.3 * len(PLOTS_TO_SHOW)
    scale = 2 / 3  # scale to 0.9 for (almost) full text width
    fig.set_size_inches(441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi)

    fname = "../../images/flicker_noise_envelope.pgf"
    if fname:
        print(f"Saving image to '{fname}'")
        plt.savefig(fname)

    if not args.silent:
        plt.show()
