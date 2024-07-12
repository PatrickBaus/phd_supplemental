#!/usr/bin/env python
# pylint: disable=duplicate-code
import argparse
import os

import allantools as at
import matplotlib.pyplot as plt
import lttb
import numpy as np

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
        ]
    ),
    # "pgf.texsystem": "lualatex",
    "pgf.preamble": "\n".join(
        [  # plots will use this preamble
            r"\usepackage{siunitx}",
        ]
    ),
    "savefig.directory": os.path.dirname(__file__),
}
plt.rcParams.update(tex_fonts)
# end of settings


def bin_psd(x_data, y_data, bins):
    inds = np.digitize(x_data, bins)
    x_binned = np.zeros(len(bins)-1)
    y_binned = np.zeros(len(bins)-1)

    for i in range(len(bins)-1):
        # Return NaN for empty bins
        x_binned[i] = np.NaN if len(x_data[inds == i+1]) == 0 else np.mean(x_data[inds == i+1])
        y_binned[i] = np.NaN if len(x_data[inds == i+1]) == 0 else np.mean(y_data[inds == i+1])

    return x_binned[~np.isnan(x_binned)], y_binned[~np.isnan(y_binned)]


def downsample_data(x_data, y_data):
    x_data, y_data = lttb.downsample(np.array([x_data, y_data]).T, n_out=1000, validators=[]).T
    return x_data, y_data


def plot_noise(betas, plot_types, show_plot_window: bool, plot_settings: dict):
    np.random.seed(42)
    nr = 2**14  # number of datapoints in time-series
    adev0 = 1.0

    tau0 = 1e0  # sample interval
    FS = 1.0 / tau0
    D = 2 ** (0.5)  # normalized to the sample rate, similar to qd to make sure all ADEVs start at the same y-value
    # Generate noise: white (beta=-2), flicker (beta=-3), random-walk (beta=-4)
    # beta := alpha - 2
    # alpha = power-law coefficient (see thesis, section "Identifying Noise in Allan Deviation Plots")
    labels = {
        -2: "White noise",
        -3: "Flicker noise",
        -4: "Random walk",
        -5: "Linear drift",
    }  # betas  # mu = -1  # mu = 0  # mu = 1
    beta_colors = {-2: colors[0], -3: colors[2], -4: colors[3], -5: colors[4]}
    # We misuse a python dict, which maintains insertion order, as an ordered set
    plots_to_show = dict.fromkeys(plot_types)
    plot_direction = "vertical"  # or "horizontal"
    plot_direction = "horizontal"  # or "vertical"

    # discrete variance for noiseGen()
    # We normalize all adevs to adev0 at tau0
    # This is done according to "Discrete simulation of power law noise" eq. 7
    # The normalization_coefficients like (2*np.log(2) come from
    # "Characterization of Frequency Stability" Appendix II
    # It can also be found in
    # "Considerations on the Measurement of the Stability of Oscillators with Frequency Counters" table I.
    normalization_coefficients = {
        -2: 0.5 / tau0,
        -3: 2 * np.log(2),  # np.log is the *natural* log
        -4: 2 / 3 * np.pi**2 * tau0,
    }
    qd = {
        beta: adev0**2
        / (normalization_coefficients[beta] * 2 * (2 * np.pi) ** beta * tau0 ** (beta + 1) * (2 * np.pi) ** 2)
        for beta in betas if beta > -5
    }

    colored_noise = [at.Noise(nr, qd[beta], beta) for beta in betas if beta > -5]
    for noise in colored_noise:
        print("Generating Noise -> Q_d:", noise.qd, "beta:", noise.b, "tau0:", tau0)
        noise.generateNoise()

    # compute amplitude time series
    amplitudes = [at.phase2frequency(noise.time_series, FS) for noise in colored_noise]
    drift_amplitude = np.arange(nr - 1) * D + 0  # linear drift

    if "psd" in plots_to_show:
        # compute amplitude PSD
        psds = [at.noise.scipy_psd(amplitude, f_sample=FS, nr_segments=4) for amplitude in amplitudes]

        # compute amplitude PSD prefactor h_alpha (h_a)
        has = [noise.frequency_psd_from_qd(tau0) for noise in colored_noise]

    if "adev" in plots_to_show:
        # compute ADEV
        adevs = [at.totdev(noise.time_series, rate=FS, taus="decade")[:2] for noise in colored_noise]
        drift_taus, drift_adev, *_ = at.oadev(drift_amplitude, data_type="freq", rate=FS, taus="decade") # FIXME: Change to totdev

    fig, axs = plt.subplots(
        len(plots_to_show) if plot_direction != "horizontal" else 1,
        len(plots_to_show) if plot_direction == "horizontal" else 1,
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
        ax = axs[list(plots_to_show).index("amplitude")]
        for beta, amplitude in zip(filter(lambda beta: beta > -5, betas), amplitudes):
            x_data, y_data = downsample_data(np.arange(nr - 1) * tau0, amplitude)
            print(f"  Plotting {len(x_data)} values.")
            ax.plot(
                x_data,
                y_data,
                label=labels[beta],
                color=beta_colors[beta],
            )
        if -5 in betas:
            x_data, y_data = downsample_data(np.arange(nr - 1) * tau0, drift_amplitude)
            print(f"  Plotting {len(x_data)} values.")
            ax.plot(x_data, y_data, label=labels[-5], color=beta_colors[-5])
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(plot_settings["ylim"])  # Limits for random walk
        ax.legend(loc="upper left")
        ax.set_xlabel(r"Time in \unit{\second}")
        ax.set_ylabel(r"Ampl. in arb. unit")

    # PSD plot
    if "psd" in plots_to_show:
        ax = plt.subplot(
            len(plots_to_show) if plot_direction != "horizontal" else 1,
            len(plots_to_show) if plot_direction == "horizontal" else 1,
            list(plots_to_show).index("psd") + 1,
        )
        for beta, (freqs, psd), ha in zip(filter(lambda beta: beta > -5, betas), psds, has):
            # Downsample the psd
            bins = np.logspace(np.floor(np.log10(np.min(freqs[1:]))), np.ceil(np.log10(np.max(freqs))), num=200)
            freqs, psd = bin_psd(freqs, psd, bins=bins)

            print(f"  Plotting {len(freqs)} values.")
            (lines,) = ax.loglog(
                [freq for freq in freqs if freq != 0 or beta >= -2],
                [ha * pow(freq, beta + 2) for freq in freqs if freq != 0 or beta >= -2],
                "--",
                label=f"$h_{{{beta+2}}}f^{{{beta+2}}}$",
                color=beta_colors[beta],
            )
            ax.loglog(freqs, psd, ".", color=lines.get_color(), markersize=2)

        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(plot_settings["ylim"])  # Set limits, so that all plots look the same
        ax.legend(loc="upper right")
        # ax.set_title(r'Frequency Power Spectral Density')
        ax.set_xlabel(r"Frequency in $\unit{\Hz}$")
        ax.set_ylabel(r" $S_y(f)$ in $\unit{1 \per \Hz}$")

    # ADEV plot
    if "adev" in plots_to_show:
        ax = plt.subplot(
            len(plots_to_show) if plot_direction != "horizontal" else 1,
            len(plots_to_show) if plot_direction == "horizontal" else 1,
            list(plots_to_show).index("adev") + 1,
        )

        for noise, (taus, adev) in zip(colored_noise, adevs):
            print(f"  Plotting {len(taus)} values.")
            (lines,) = ax.loglog(
                taus,
                [noise.adev_from_qd(tau0, tau) * tau ** ((-3 - noise.b) / 2) for tau in taus],
                "--",
                label=f"$\\propto\\sqrt{{h_{{{noise.b+2}}}}}\\tau^{{{(-3-noise.b)/2:+}}}$",
                color=beta_colors[noise.b],
            )
            ax.loglog(taus, adev, "o", color=lines.get_color(), markersize=3)

        if -5 in betas:
            print(f"  Plotting {len(drift_taus)} values.")
            lines, = ax.loglog(drift_taus, [0.5**0.5 * D * (tau/tau0) for tau in drift_taus], '--', label=r'$\propto D\tau^{+1}$', color=beta_colors[-5])
            ax.loglog(drift_taus, drift_adev, 'o', color=lines.get_color(), markersize=3)

        ax.legend(loc="best")
        ax.grid(True, which="minor", axis="x", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(plot_settings["ylim"])  # Set limits, so that all plots look the same
        ax.set_xlim(None, 6e3)  # Set limits, so that all plots look the same, FIME: Check whether 5e3 is ok
        ax.set_xlabel(r"$\tau$ in \unit{\second}")
        ax.set_ylabel(r"ADEV $\sigma_A(\tau)$")

    fig.set_size_inches(plot_settings["plot_size"])

    if plot_settings["fname"]:
        print(f"  Saving image to '{plot_settings['fname']}'")
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

    phi = 0.75  # use 0.75 for the thesis
    scale = 0.4
    noise_types = [(-2, "white", (-6.5, 6.5)), (-3, "flicker", (-16, 16)), (-4, "random_walk", (-200, 250))]
    plot_types = ["amplitude", "psd", "adev"]

    for beta, name, y_limit in noise_types:
        for plot_type in plot_types:
            plot_settings = {
                "plot_size": (441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi),
                "fname": f"../../images/{name}_noise_{plot_type}.pgf",
                "ylim": y_limit if plot_type == "amplitude" else (5e-2, 5e6) if plot_type == "psd" else (1e-2, 5e4),
            }
            plot_noise(betas=[beta, ], plot_types=[plot_type, ], show_plot_window=not args.silent, plot_settings=plot_settings)

    # Plot drift
    plot_types = ["amplitude", "adev"]
    name = "drift"
    y_limit = (None, None)
    for plot_type in plot_types:
        plot_settings = {
            "plot_size": (441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi),
            "fname": f"../../images/{name}_{plot_type}.pgf",
            "ylim": y_limit if plot_type == "amplitude" else (5e-2, 5e6) if plot_type == "psd" else (1e-2, 5e4),
        }
        plot_noise(betas=[-5, ], plot_types=[plot_type, ], show_plot_window=not args.silent, plot_settings=plot_settings)
