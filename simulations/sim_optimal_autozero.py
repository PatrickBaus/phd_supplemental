#!/usr/bin/env python
# pylint: disable=duplicate-code
import argparse
import os

import allantools as at
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
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


def generate_noise(dead_time: int, nplcs: NDArray[int]):
    np.random.seed(42)
    adev0 = 165e-9  # This number is modeled after the HP3458A 10 V input amplifier
    f_c = 1.5

    tau0 = 1/50
    FS = 1.0 / tau0
    # We need {dead_time} extra samples to remove due to the dead time of {dead_time} PLC
    # We need twice the number of samples to run
    if dead_time:
        nr = np.lcm.reduce(nplcs + dead_time)*2 *300 + 2  # We need to add 2, because of the phase2frequency() call, see below
    else:
        nr = np.lcm.reduce(nplcs + dead_time)*2 *int(2e4) + 2  # We need to add 2, because of the phase2frequency() call, see below
    print(f"Number of datapoints to be generated: {nr}")

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

    colored_noise = [at.Noise(nr, qd[beta], beta) for beta in (-2, -3)]

    for noise in colored_noise:
        print(
            f"Generating {labels[noise.b].lower()} -> Q_d: {noise.qd} beta: {noise.b} tau0: {tau0} h_alpha: {noise.frequency_psd_from_qd(tau0)}")
        noise.generateNoise()

    # phase2frequency() conversion "eats" 1 value, because is differentiates the phase input
    # So we will drop 1 more to get an even of sample length
    amplitudes = [at.phase2frequency(noise.time_series, FS)[:-1] for noise in colored_noise]
    amplitude = np.sum(amplitudes, 0)
    variance =  np.var(amplitude)
    print("Number of samples:", len(amplitude), "Variance sigma^2:", variance)

    amplitudes_az = {}
    for nplc in nplcs:
        # print(f"Variance for NPLC {nplc}, no AZ: {np.var(np.average(amplitude.reshape(-1, nplc), axis=1))}")
        # Apply AZ
        # Add dead time by removing every nplc+1 value
        if dead_time > 0:
            dead_times = np.arange(nplc, amplitude.size, nplc + dead_time)  # the list of entries to drop
            print(f"nplc: {nplc}, size: {amplitude.size}, dead time indices: {dead_times}")
            amplitude_az = np.delete(amplitude, dead_times)
        else:
            amplitude_az = amplitude
        # integrate the measurement
        amplitude_az = np.average(amplitude_az.reshape(-1, nplc), axis=1)
        # Subtract every second measurement
        amplitude_az = amplitude_az[0::2] - amplitude_az[1::2]
        amplitudes_az[nplc] = amplitude_az
        # var_az = np.var(amplitude_az)
        # print(f"Variance for NPLC {nplc}, AZ: {var_az}")
        # print(f"Variance for NPLC {nplc}, AZ, normalized: {1/np.sqrt(amplitude_az.size) * var_az}")

    return amplitude, amplitudes_az

def plot_noise(amplitude, amplitudes_az: dict[int], dead_time:int, show_plot_window: bool, plot_settings: dict):
    tau0 = 1/50  # sample interval NPLC=1
    FS = 1.0 / tau0

    taus = np.logspace(-2, 2, num=50)
    # compute ADEV
    adevs_az = {nplc : at.oadev(amplitude, rate=1/((nplc+dead_time)*2)*FS, data_type="freq", taus=taus)[:2] for nplc, amplitude in amplitudes_az.items()}
    taus_noaz, adev_noaz = at.oadev(amplitude, rate=FS, data_type="freq", taus=taus)[:2]

    fig, ax = plt.subplots(1, 1, layout="constrained")

    # ADEV plot
    plt.gca().set_prop_cycle(None)  # Reset the color cycle

    for nplc, (taus, adev) in adevs_az.items():
        ax.loglog(taus, adev, "-", markersize=3, label=f"NPLC {nplc}")

    ax.loglog(taus_noaz, adev_noaz, "--")

    ax.legend(loc="upper right")
    ax.grid(True, which="minor", ls="-", color="0.85")
    ax.grid(True, which="major", ls="-", color="0.45")
    ax.set_ylim(1e-8, 2e-6)  # Set limits, so that all plots look the same
    # ax.set_title(r'Allan Deviation')
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

    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()

    phi = (5**0.5 - 1) / 2
    scale = 2 / 3

    dead_times = (0, 1, )

    for dead_time in dead_times:
        amplitude, amplitudes_az = generate_noise(dead_time=dead_time, nplcs=np.array([1, 2, 5, 10, 20, 50,]))

        plot_settings = {
            "plot_size": (441.01773 / 72.27 * scale, 441.01773 / 72.27 * scale * phi),
            "fname": f"../../images/autozero_{'deadtime' if dead_time else ''}_nplcs_adev.pgf",
        }
        plot_noise(amplitude=amplitude, amplitudes_az=amplitudes_az, dead_time=dead_time, show_plot_window=not args.silent, plot_settings=plot_settings)
