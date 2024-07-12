#!/usr/bin/env python
# pylint: disable=duplicate-code
import argparse
import os

import allantools as at
import matplotlib.pyplot as plt
import numpy as np

import lttb
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


def generate_noise():
    np.random.seed(42)
    nr = 2 ** 25  # number of datapoints in time-series
    adev0 = 1.0

    tau0 = 1e-6  # sample interval
    FS = 1.0 / tau0
    # Generate noise: white (beta=-2), flicker (beta=-3), random-walk (beta=-4)
    # betas = (-2,-3, -4,)
    # betas = (-2,)
    labels = {
        -2: "White noise",
        -3: "Flicker noise",
        -4: "Random walk",
    }  # betas  # mu = -1  # mu = 0  # 0 mu = 1

    # discrete variance for noiseGen()
    # We normalize all adevs to adev0 at tau0
    # This is done according to "Discrete simulation of power law noise" eq. 7
    # The normalization_coefficients like (2*np.log(2) come from
    # "Characterization of Frequency Stability" Appendix II
    # It can also be found in
    # "Considerations on the Measurement of the Stability of Oscillators with Frequency Counters" table I.
    normalization_coefficients = {
        -2: 0.5 / tau0 / 1000,
        -3: 2 * np.log(2) / 5,  # np.log is the *natural* log
        -4: 2 / 3 * np.pi ** 2 * tau0 * 10000,
    }
    qd = {
        beta: adev0
              / (normalization_coefficients[beta] * 2 * (2 * np.pi) ** beta * tau0 ** (beta + 1) * (2 * np.pi) ** 2)
        for beta in labels.keys()
    }

    # We need to generate *all* noises, because the random numbers must be drawn in order to result in the same plots
    colored_noise = {beta: at.Noise(nr, qd[beta], beta) for beta in labels.keys()}
    for noise in colored_noise.values():
        print(
            f"Generating {labels[noise.b].lower()} -> Q_d: {noise.qd} beta: {noise.b} tau0: {tau0} h_alpha: {noise.frequency_psd_from_qd(tau0)}")
        noise.generateNoise()

    return colored_noise

def plot_noise(colored_noise: dict, betas, plot_types, show_plot_window: bool, plot_settings: dict):
    tau0 = 1e-6  # sample interval
    FS = 1.0 / tau0

    labels = {
        -2: "White noise",
        -3: "Flicker noise",
        -4: "Random walk",
    }  # betas  # mu = -1  # mu = 0  # 0 mu = 1
    beta_colors = {-2: colors[0], -3: colors[2], -4: colors[3], -9: colors[9]}
    # We misuse a python dict, which maintains insertion order, as an ordered set
    plots_to_show = dict.fromkeys(plot_types)
    plot_direction = "vertical"  # or "horizontal"
    plot_direction = "horizontal"  # or "vertical"

    # compute amplitude time series
    amplitude = {beta: at.phase2frequency(colored_noise[beta].time_series, FS) for beta in betas}
    amplitude = np.sum(tuple(amplitude.values()), 0)
    if "psd" in plots_to_show:
        # compute amplitude PSD
        freqs, psd = at.noise.scipy_psd(amplitude, f_sample=FS, nr_segments=4)
        f_max = {
            -2: FS,
            -3: 1e4,
            -4: 1e2,
        }
        # downsample the data to logscale bins
        bins = np.logspace(np.floor(np.log10(np.min(freqs[1:]))), np.ceil(np.log10(np.max(freqs))), num=200)
        freqs, psd = bin_psd(freqs, psd, bins=bins)

        # compute amplitude PSD prefactor h_a
        has = {beta : noise.frequency_psd_from_qd(tau0) for beta, noise in colored_noise.items()}

        # If both white noise and flicker noise is present calculate the corner frequency
        # Note: has will always contain all betas
        if -2 in betas and -3 in betas:
            print("Noise corner frequency:", has[-3]/has[-2], "Hz")

    if "adev" in plots_to_show:
        # compute ADEV
        taus, adev = at.oadev(amplitude, rate=FS, data_type="freq", taus="decade")[:2]
        adev_taus = {
            -2: [tau for tau in taus if tau <= 1e-3],
            -3: taus,
            -4: [tau for tau in taus if tau >= 1e-2],
        }

    if "amplitude" in plots_to_show:
        time = np.arange(len(amplitude)) * tau0
        # downsample the result for easier plotting
        time, amplitude = downsample_data(time, amplitude)

    fig, axs = plt.subplots(
        len(plots_to_show) if plot_direction != "horizontal" else 1,
        len(plots_to_show) if plot_direction == "horizontal" else 1,
        layout="constrained",
    )
    axs = [axs,] if len(plots_to_show) == 1 else axs

    # Amplitude plot
    if "amplitude" in plots_to_show:
        ax = axs[list(plots_to_show).index("amplitude")]
        label = None if len(betas) > 1 else labels[betas[0]]
        print(f"  Plotting {len(time)} values.")
        ax.plot(
            time,
            amplitude,
            color=beta_colors[np.sum(betas)],
            label=label
        )
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(plot_settings["ylim"])
        if label:
            ax.legend(loc="upper left")
        ax.set_xlabel(r"Time in $\unit{\second}$")
        ax.set_ylabel(r"Ampl. in arb. unit")

    # PSD plot
    if "psd" in plots_to_show:
        ax = plt.subplot(
            len(plots_to_show) if plot_direction != "horizontal" else 1,
            len(plots_to_show) if plot_direction == "horizontal" else 1,
            list(plots_to_show).index("psd") + 1,
        )

        print(f"  Plotting {len(freqs)} values.")
        ax.loglog(freqs, psd, ".", markersize=4, color=beta_colors[np.sum(betas)])
        for beta in betas:
            ax.loglog(
                [freq for freq in freqs if freq <= f_max[beta]],
                [has[beta] * pow(freq, beta + 2) for freq in freqs if freq <= f_max[beta]],
                "--",
                label=f"{labels[beta]} $h_{{{beta+2}}}f^{{{beta+2}}}$",
                color=beta_colors[beta],
            )

        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        #ax.set_ylim(5e-2, 5e6)  # Set limits, so that all plots look the same
        ax.legend(loc="upper right")
        ax.set_xlabel(r"Frequency in $\unit{\Hz}$")
        ax.set_ylabel(r"$S_y(f)$ in $\unit{1 \per \Hz}$")

    # ADEV plot
    if "adev" in plots_to_show:
        ax = plt.subplot(
            len(plots_to_show) if plot_direction != "horizontal" else 1,
            len(plots_to_show) if plot_direction == "horizontal" else 1,
            list(plots_to_show).index("adev") + 1,
        )

        print(f"  Plotting {len(taus)} values.")
        ax.loglog(taus, adev, "o", markersize=3, color=beta_colors[np.sum(betas)])
        for beta in betas:
            ax.loglog(
                adev_taus[beta],
                [colored_noise[beta].adev_from_qd(tau0, tau) * tau ** ((-3 - beta) / 2) for tau in adev_taus[beta]],
                "--",
                label=f"{labels[beta]} $\\propto \\sqrt{{h_{{{beta+2}}}}}\\tau^{{{(-3-beta)/2:+}}}$",
                color=beta_colors[beta],
            )

        ax.legend(loc="upper center")
        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        #ax.set_ylim(1e-2, 5e4)  # Set limits, so that all plots look the same
        ax.set_xlabel(r"$\tau$ in \unit{\second}")
        ax.set_ylabel(r"ADEV $\sigma_A(\tau)$")

    fig.set_size_inches(plot_settings["plot_size"])

    if plot_settings["fname"]:
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

    phi = 0.75  # use 0.75 for the thesis
    scale = 0.4  # scale to 2/3 for combined plots and use 0.4 for mini plots
    noise_types = [(-2, "white", (-250, 250)), (-3, "flicker", (-60, 50)), (-4, "random_walk", (-50, 180))]
    plot_types = ["amplitude", ]

    colored_noise = generate_noise()

    # Show individual noise components
    for beta, name, y_limit in noise_types:
        for plot_type in plot_types:
            plot_settings = {
                "plot_size": (441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi),
                "fname": f"../../images/example_{name}_noise_{plot_type}.pgf",
                "ylim": y_limit if plot_type == "amplitude" else (None, None),
            }
            plot_noise(colored_noise=colored_noise, betas=[beta, ], plot_types=[plot_type, ], show_plot_window=not args.silent, plot_settings=plot_settings)

    # Sum the noise components and show the plots again
    plot_types = ["amplitude", "psd", "adev"]

    phi = (5 ** 0.5 - 1) / 2
    scale = 2/3  # scale to 2/3 for combined plots and use 0.4 for mini plots

    for plot_type in plot_types:
        plot_settings = {
            "plot_size": (441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi),
            "fname": f"../../images/example_combined_noise_{plot_type}.pgf",
            "ylim": (None, None),
        }
        plot_noise(colored_noise=colored_noise, betas=[-2, -3, -4 ], plot_types=[plot_type, ],
            show_plot_window=not args.silent, plot_settings=plot_settings)
