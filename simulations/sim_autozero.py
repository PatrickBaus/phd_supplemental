#!/usr/bin/env python
# pylint: disable=duplicate-code
import argparse
import os

import allantools as at
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import lttb

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


def bin_psd(x_data, y_data, bins):
    inds = np.digitize(x_data, bins)
    x_binned = np.zeros(len(bins)-1)
    y_binned = np.zeros(len(bins)-1)

    for i in range(len(bins)-1):
        # Return NaN for empty bins
        x_binned[i] = np.nan if len(x_data[inds == i+1]) == 0 else np.mean(x_data[inds == i+1])
        y_binned[i] = np.nan if len(x_data[inds == i+1]) == 0 else np.mean(y_data[inds == i+1])

    return x_binned[~np.isnan(x_binned)], y_binned[~np.isnan(y_binned)]


def downsample_data(x_data, y_data):
    x_data, y_data = lttb.downsample(np.array([x_data, y_data]).T, n_out=1000, validators=[]).T
    return x_data, y_data


def generate_noise():
    np.random.seed(42)
    nr = int(1e6)#2**20  # number of datapoints in time-series
    adev0 = 165e-9  # This number is modeled after the HP3458A 10 V input amplifier
    f_c = 1.5

    tau0 = 1/50 * 10  # sample interval (NPLC=10)
    FS = 1.0 / tau0
    # Generate noise: white (beta=-2), flicker (beta=-3), random-walk (beta=-4)
    # betas = (-2,-3, -4,)
    # betas = (-2,)
    labels = {
        -2: "White noise",
        -3: "Flicker noise",
    }  # betas  # mu = -1  # mu = 0  # 0 mu = 1

    # discrete variance for noiseGen()
    # We normalize all adevs to adev0 at tau0
    # This is done according to "Discrete simulation of power law noise" eq. 7
    # The normalization_coefficients like (2*np.log(2) come from
    # "Characterization of Frequency Stability" Appendix II
    # It can also be found in
    # "Considerations on the Measurement of the Stability of Oscillators with Frequency Counters" table I.
    normalization_coefficients = {
        -2: 1,
        -3: 1/f_c,
    }
    qd = {
        beta: adev0**2 / (normalization_coefficients[beta] * 2 * (2 * np.pi) ** beta * tau0 ** (beta + 1) * (2 * np.pi) ** 2)
        for beta in labels.keys()
    }

    colored_noise = [at.Noise(nr+2, qd[beta], beta) for beta in (-2, -3)]  # FIXME: drop the +2

    for noise in colored_noise:
        print(
            f"Generating {labels[noise.b].lower()} -> Q_d: {noise.qd} beta: {noise.b} tau0: {tau0} h_alpha: {noise.frequency_psd_from_qd(tau0)}")
        noise.generateNoise()

    return colored_noise


def plot_noise(colored_noise, apply_az: bool, plot_types: list[str], show_plot_window: bool, plot_settings: dict):
    adev0 = 165e-9  # This number is modeled after the HP3458A 10 V input amplifier

    tau0 = 1/50 * 10  # sample interval (NPLC=10)
    FS = 1.0 / tau0
    offset = 10
    plot_direction = "horizontal"
    labels = {
        -2: "White noise",
        -3: "Flicker noise",
        -4: "Random walk",
    }  # betas  # mu = -1  # mu = 0  # 0 mu = 1
    beta_colors = {
        -2: colors[0],
        -3: colors[2],
        -4: colors[1],
    }

    n = 0  # number of averages
    # phase2frequency() conversion "eats" 1 value, because is differentiates the phase input
    # So we will drop 1 more to get an even of sample length
    amplitudes = [at.phase2frequency(noise.time_series, FS)[:-1] for noise in colored_noise]
    amplitude = np.sum(amplitudes, 0)
    variance = np.var(amplitude)
    print("Number of samples:", len(amplitude), "Variance sigma^2:", variance)
    if apply_az:
        # Apply the AZ algorithm
        w = 10
        amplitude = amplitude[::2] - amplitude[1::2]
        #amplitude = amplitude[::2] - np.convolve(amplitude[1::2], np.ones(w), 'same') / w
        FS /= 2
        variance_az = np.var(amplitude)
        print("Number of samples after AZ:", len(amplitude), "Variance sigma^2:", variance_az)
    amplitude += offset
    if n > 1:
        amplitude = np.average(amplitude.reshape(-1, n), axis=1)

    if "psd" in plot_types:
        # compute amplitude PSD
        freqs, psd = at.noise.scipy_psd(amplitude, f_sample=FS, nr_segments=2**8)
        if apply_az:
            print("Autozero psd:", np.mean(psd), "Increase:", np.mean(psd)/adev0**2)
        f_max = {
            -2: FS,
            -3: FS,
        }
        # downsample the data to logscale bins
        bins = np.logspace(np.floor(np.log10(np.min(freqs[1:]))), np.ceil(np.log10(np.max(freqs))), num=200)
        freqs, psd = bin_psd(freqs, psd, bins=bins)

        # compute amplitude PSD prefactor h_a
        has = {noise.b : noise.frequency_psd_from_qd(tau0) for noise in colored_noise}

        # If both white noise and flicker noise is present calculate the corner frequency
        if -2 in has and -3 in has:
            print("Noise corner frequency:", has[-3]/has[-2], "Hz")

    if "adev" in plot_types:
        taus = np.logspace(-2, 3, num=50)
        # compute ADEV
        taus, adev = at.oadev(amplitude, rate=FS, data_type="freq")[:2]
        adev_taus = {
            -2: [tau for tau in taus if tau <= 2e4] if apply_az else [1e-1, ] +  [tau for tau in taus if tau <= 5e-1],
            -3: taus,
            -4: [tau for tau in taus if tau >= 1e-2],
        }

    if "amplitude" in plot_types:
        time = np.arange(len(amplitude)) * (tau0 * 2) if apply_az else np.arange(len(amplitude)) * tau0
        # downsample the result for easier plotting
        time, amplitude = downsample_data(time, amplitude)

    fig, axs = plt.subplots(
        len(plot_types) if plot_direction != "horizontal" else 1,
        len(plot_types) if plot_direction == "horizontal" else 1,
        layout="constrained",
    )
    axs = (
        [
            axs,
        ]
        if len(plot_types) == 1
        else axs
    )

    # Amplitude plot
    if "amplitude" in plot_types:
        print(f"  Plotting {len(amplitude)} values.")
        ax = axs[plot_types.index("amplitude")]
        ax.plot(
            time,
            amplitude,
            color=colors[8] if apply_az else colors[3],
        )
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(plot_settings["ylim"])
        ax.set_xlabel(r"Time in $\unit{\second}$")
        ax.set_ylabel(r"Amplitude in $\unit{\V}$")

    # PSD plot
    if "psd" in plot_types:
        ax = plt.subplot(
            len(plot_types) if plot_direction != "horizontal" else 1,
            len(plot_types) if plot_direction == "horizontal" else 1,
            plot_types.index("psd") + 1,
        )

        print(f"  Plotting {len(freqs)} values.")
        ax.loglog(freqs, psd, ".", markersize=4, color=colors[8] if apply_az else colors[3])
        for noise, ha in zip(colored_noise, has.values()):
            ax.loglog(
                [freq for freq in freqs if freq <= f_max.get(noise.b, FS) and freq > 0],
                [(ha * pow(freq, noise.b + 2)) for freq in freqs if freq <= f_max.get(noise.b, FS) and freq > 0],
                "--",
                label=labels[noise.b],
                color=beta_colors[noise.b],
            )

        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(plot_settings["ylim"])
        ax.legend(loc="upper right")
        ax.set_xlabel(r"Frequency in $\unit{\Hz}$")
        ax.set_ylabel(r"$S_y(f)$ in $\displaystyle \unit{\V^2 \per \Hz}$")

    # ADEV plot
    if "adev" in plot_types:
        ax = plt.subplot(
            len(plot_types) if plot_direction != "horizontal" else 1,
            len(plot_types) if plot_direction == "horizontal" else 1,
            plot_types.index("adev") + 1,
        )

        print(f"  Plotting {len(taus)} values.")
        ax.loglog(taus, adev, "o", markersize=3, color=colors[8] if apply_az else colors[3])
        for noise in colored_noise:
            ax.loglog(
                adev_taus[noise.b],
                [noise.adev_from_qd(tau0, tau) * tau ** ((-3 - noise.b) / 2) for tau in adev_taus[noise.b]],
                "--",
                label=labels[noise.b],
                color=beta_colors[noise.b],
            )

        ax.legend(loc="upper right")
        ax.grid(True, which="minor", ls="-", color="0.85")
        ax.grid(True, which="major", ls="-", color="0.45")
        ax.set_ylim(plot_settings["ylim"])
        ax.set_xlabel(r"$\tau$ in \unit{\second}")
        ax.set_ylabel(r"ADEV $\sigma_A(\tau)$ in \unit{\V}")

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
    parser.add_argument('--autozero', action='store_true', help="Apply the autozero algorithm.")

    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    phi = (5**0.5 - 1) / 2
    scale = 2 / 3
    plot_types = ["amplitude", "psd", "adev"]

    colored_noise = generate_noise()

    for plot_type in plot_types:
        plot_settings = {
            "plot_size": (441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi),
            "fname": f"../../images/autozero{'' if args.autozero else '_raw'}_{plot_type}.pgf",
            "ylim": (-4.5e-6+10, 4.5e-6+10) if plot_type == "amplitude" else (None, None),
        }
        plot_noise(colored_noise=colored_noise, apply_az=args.autozero, plot_types=[plot_type, ], show_plot_window=not args.silent, plot_settings=plot_settings)
