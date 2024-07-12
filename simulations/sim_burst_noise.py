#!/usr/bin/env python
# pylint: disable=duplicate-code
import argparse
import os
import random

import allantools as at
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

import lttb
from markov_chain import ContinuousTimeMarkovModel
import seaborn as sns

# Select a color style. We do not use plt.style.use(), because the colors need to assigned in a fixed order according
# to the power law plot
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
            r"\sisetup{per-mode = symbol}%"
        ]
    ),
    "pgf.preamble": "\n".join(
        [  # plots will use this preamble
            r"\usepackage{siunitx}",
            r"\sisetup{per-mode = symbol}%"
        ]
    ),
    "savefig.directory": os.path.dirname(__file__),
}
plt.rcParams.update(tex_fonts)
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


def bin_psd(x_data, y_data, bins):
    inds = np.digitize(x_data, bins)
    x_binned = np.zeros(len(bins)-1)
    y_binned = np.zeros(len(bins)-1)

    for i in range(len(bins)-1):
        # Return NaN for empty bins
        x_binned[i] = np.NaN if len(x_data[inds == i+1]) == 0 else np.mean(x_data[inds == i+1])
        y_binned[i] = np.NaN if len(x_data[inds == i+1]) == 0 else np.mean(y_data[inds == i+1])

    # drop all np.NaN
    return x_binned[~np.isnan(x_binned)], y_binned[~np.isnan(x_binned)]


def downsample_psd(freqs, psd):
    bins=np.logspace(int(np.log10(np.min(freqs[1:]))), int(np.log10(np.max(freqs))), num=400)
    freqs, psd = bin_psd(freqs, psd, bins=bins)

    return freqs, psd


def plot_noise(plot_types, show_plot_window: bool, plot_settings: dict):
    np.random.seed(42)
    random.seed(42)

    # We misuse a python dict, which maintains insertion order, as an ordered set
    plots_to_show = dict.fromkeys(plot_types)
    PLOT_DIRECTION = "vertical"  # or "horizontal"
    PLOT_DIRECTION = "horizontal"  # or "vertical"

    N_PER_SEG = 100
    N = int(20e6) if "adev" in plots_to_show else int(2e6)  # use 20e6 for the adev plot else 2e6
    FS = 2e2

    TAU1S = {0.1: colors[0], 1: colors[2], 10: colors[3]}

    # compute amplitude time series
    amplitudes = [
        gen_burst_noise(number_of_samples=N, samplerate=FS, tau1=tau1, tau0=1, offset=i) for i, tau1 in enumerate(TAU1S.keys())
    ]

    if "psd" in plots_to_show:
        # compute amplitude PSD
        psds = [signal.welch(noise, FS, nperseg=len(noise) // N_PER_SEG, window="hann") for noise in amplitudes]

    if "adev" in plots_to_show:
        # compute ADEV
        taus = np.logspace(-2, 2, num=20)
        # Can't use totdev, because it takes too long. Use oadev instead.
        adevs = [at.oadev(noise, data_type="freq", rate=FS, taus=taus)[:2] for noise in amplitudes]

    fig, axs = plt.subplots(
        len(plots_to_show) if PLOT_DIRECTION != "horizontal" else 1,
        len(plots_to_show) if PLOT_DIRECTION == "horizontal" else 1,
        layout="constrained",
    )
    axs = (
        [
            axs,
        ]
        if len(plots_to_show) == 1
        else axs
    )

    # Amplitude plot
    if "amplitude" in plots_to_show:
        number_point_to_plot = 2000
        ax = axs[list(plots_to_show).index("amplitude")]
        for tau1, amplitude in zip(TAU1S.keys(), amplitudes):
            print(f"  Plotting {len(amplitude[:number_point_to_plot])} values.")
            ax.step(
                np.arange(number_point_to_plot) / FS,
                amplitude[:number_point_to_plot],
                label=f"$\\bar\\tau_1=\\qty{{{tau1}}}{{\\s}}$",
                color=TAU1S[tau1],
            )
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.legend(loc="upper right")
        ax.set_xlabel(r"Time in \unit{\second}")
        ax.set_ylabel(r"Amplitude in arb. unit")

    # PSD plot
    if "psd" in plots_to_show:
        ax = plt.subplot(
            len(plots_to_show) if PLOT_DIRECTION != "horizontal" else 1,
            len(plots_to_show) if PLOT_DIRECTION == "horizontal" else 1,
            list(plots_to_show).index("psd") + 1,
        )

        for tau1, (freqs, psd) in zip(TAU1S.keys(), psds):
            # downsample the data to logscale bins
            freqs, psd  = downsample_psd(freqs, psd)
            print(f"  Plotting {len(freqs[1:])} values.")
            (lines,) = ax.loglog(
                freqs,
                [burst_noise_psd(freq, tau1) for freq in freqs],
                "--",
                label=f"$\\bar\\tau_1=\\qty{{{tau1}}}{{\\s}}$",
                color=TAU1S[tau1],
            )
            ax.loglog(freqs, psd, ".", color=lines.get_color(), markersize=2)

        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        # ax.set_ylim(5e-2, 5e6)  # Set limits, so that all plots look the same
        ax.legend(loc="lower left")
        ax.set_xlabel(r"Frequency in $\unit{\Hz}$")
        ax.set_ylabel(r"$S_y(f)$ in $\unit{1 \per \Hz}$")

    # ADEV plot
    if "adev" in plots_to_show:
        ax = plt.subplot(
            len(plots_to_show) if PLOT_DIRECTION != "horizontal" else 1,
            len(plots_to_show) if PLOT_DIRECTION == "horizontal" else 1,
            list(plots_to_show).index("adev") + 1,
        )

        for tau1, (taus, adev) in zip(TAU1S.keys(), adevs):
            print(f"  Plotting {len(taus)} values.")
            (lines,) = ax.loglog(taus, [burst_noise_adev(T=tau, tau1=tau1, tau0=1) for tau in taus], "--", color=TAU1S[tau1])
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

    fig.set_size_inches(plot_settings["plot_size"])

    if plot_settings['fname']:
        print(f"Saving image to '{plot_settings['fname']}'")
        plt.savefig(plot_settings["fname"])

    if show_plot_window:
        plt.show()

    plt.close(fig)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Allan deviation simulator.")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
    parser.add_argument('--silent', action='store_true', help="Do not show the plot when set.")

    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    phi = (5**0.5 - 1) / 2  # golden ratio
    scale = 2 / 3  # scale to 0.89 for (almost) full text width
    plot_types = ["amplitude", "psd", "adev"]
    name = "burst"

    for plot_type in plot_types:
        plot_settings = {
            "plot_size": (441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi),
            "fname": f"../../images/{name}_noise_{plot_type}.pgf",
        }
        plot_noise(plot_types=[plot_type, ], show_plot_window=not args.silent, plot_settings=plot_settings)
