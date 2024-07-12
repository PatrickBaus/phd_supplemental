#!/usr/bin/env python
import argparse
import glob
import importlib

import allantools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import seaborn as sns

from file_parser import parse_file

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
    # "pgf.texsystem": "lualatex",
    "pgf.preamble": "\n".join(
        [  # plots will use this preamble
            r"\usepackage{siunitx}",
            r"\sisetup{per-mode = symbol}%"
        ]
    ),
    "savefig.directory": os.path.dirname(os.path.realpath(__file__)),
}
plt.rcParams.update(tex_fonts)
# plt.style.use('tableau-colorblind10')
# plt.style.use('seaborn-colorblind')
# sns.set_theme()
# end of settings


def noise_gen(noise_type="white", amplitude=1, N=1e5):
    from random import seed

    seed(42)

    noise_beta = {
        "blue": 1,  # mu = -2
        "white": 0,  # mu = -1
        "pink": -1,  # mu = 0
        "brown": -2,  # 0 mu = 1
        "drift": -3,  # mu = 2
    }
    beta = noise_beta[noise_type]
    x = np.arange(0, N // 2 + 1)
    mag = amplitude * x ** (beta / 2) * np.random.randn(N // 2 + 1)
    pha = 2 * np.pi * np.random.rand(N // 2 + 1)
    real = mag * np.cos(pha)
    imag = mag * np.sin(pha)
    real[0] = 0
    imag[0] = 0

    c = real + 1j * imag
    tod = np.fft.irfft(c)

    return tod


def load_data(plot_file):
    print(f"  Parsing: '{plot_file['filename']}'...")
    data = parse_file(**plot_file)

    return data


def crop_data(data, zoom_date=None, crop_secondary=None):
    if zoom_date is not None:
        index_to_drop = data[(data.date < zoom_date[0]) | (data.date > zoom_date[1])].index
        data.drop(index_to_drop, inplace=True)

    # y = 1/(0.000858614 + 0.000259555 * np.log(y) + 1.35034*10**-7 * np.log(y)**3)
    print(f"    Begin date: {data.date.iloc[0].tz_convert('Europe/Berlin')}")
    print(
        f"    End date:   {data.date.iloc[-1].tz_convert('Europe/Berlin')} (+{(data.date.iloc[-1]-data.date.iloc[0]).total_seconds()/3600:.1f} h)"
    )


def process_data(data, columns, plot_type):
    sample_rate = (len(data) - 1) / (data.iloc[-1].date - data.iloc[0].date).total_seconds()
    df = pd.DataFrame()
    for i, column in enumerate(columns):
        if column in data:
            print(f"    Calculating ADEV for {column}.")
            (tau, adev, adev_error, n) = allantools.totdev(
                data[column].values, data_type="freq", rate=sample_rate
            )  # , taus="all")
            #(tau, adev, adev_error, n) = allantools.oadev(
            #    data[column].values, data_type="freq", rate=sample_rate, taus="all"
            #)
            df["tau"] = tau
            df[column] = adev
            df[column + "_error"] = adev_error
            print(f"    Done calculating ADEV for {column}.\n    ################")

    # Remove ADEV with tau < 1/8 tau_max
    # df = df[df.tau <= 1/8*max(df.tau)]
    return df


def prepare_axis(ax, label, color_map=None):
    # ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.grid(True, which="minor", ls="-", color="0.85")
    ax.grid(True, which="major", ls="-", color="0.45")

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_ylabel(r"Allan deviation in $\unit{\V}$")
    ax.set_xlabel(r"$\tau$ in \unit{\second}")

    if color_map is not None:
        ax.set_prop_cycle("color", color_map)


def plot_data(ax, data, column_settings):
    columns_to_plot = [(column, settings) for column, settings in column_settings.items() if column in data]
    for column, settings in columns_to_plot:
        # line = ax.fill_between(data.tau, data[column] + data[column + "_error"], data[column] - data[column + "_error"], alpha=0.2)
        ax.loglog(data.tau, data[column], marker="", alpha=0.7, **settings)


def plot_series(plot, show_plot_window):
    print(f"Plotting {plot['description']}")
    # Load the data to be plotted
    plot_files = (plot_file for plot_file in plot["files"] if plot_file.get("show", True))
    data_files = [load_data(plot_file)[0] for plot_file in plot_files]

    # If we have something to plot, proceed
    if len(data_files) > 0:
        for data in data_files:
            crop_data(data, zoom_date=plot.get("zoom"))
            print(
                f"    Data samples: {len(data)}; Sampling rate: {50*(data.date.iloc[-1] - data.date.iloc[0]).total_seconds()/(len(data)-1):.2f} PLC"
            )

            plot_settings = plot["primary_axis"]
            N = len(data)
            processed_data = process_data(
                data=data,
                columns=plot_settings["columns_to_plot"],
                plot_type=plot_settings.get("plot_type", "absolute"),
            )

            ax = plt.subplot(111)
            prepare_axis(ax=ax, label=plot_settings["label"])  # , color_map=plt.cm.tab10.colors)
            plot_data(ax, processed_data, column_settings=plot_settings["columns_to_plot"])

            # Create some artifical noise data
            # Quantization noise ~tau**-1
            # White nose ~tau**(-1/2)
            # Flicker noise ~const
            # Random walk ~tau**(1/2)
            # Linear drift ~tau
            # processed_data["drift_noise"] = np.sqrt(1/2) * 2e-6 / processed_data.tau[(processed_data.tau >= 2e1) & (processed_data.tau < 6e3)]**(1/4)
            # processed_data["drift_noise"] = np.sqrt(2 * np.log(2)) * 1.1e-7
            # processed_data["rw_noise_k2002"] = np.pi * np.sqrt(2/3) * 1e-9 * 1.5/2.6 * np.sqrt(processed_data.tau[processed_data.tau >= 8e3])
            # ax.loglog(processed_data.tau, processed_data["rw_noise_k2002"], marker="", alpha=1, color='black', linestyle="dotted", linewidth=1)
            # processed_data["rw_noise_3458a"] = np.pi * np.sqrt(2/3) * 0.996e-9 * np.sqrt(processed_data.tau[processed_data.tau >= 3e3])
            # processed_data["flicker_noise_3458a"] = np.where((processed_data.tau >= 1e1) & (processed_data.tau < 3e3) , np.sqrt(2 * np.log(2)) * 1.19e-7, np.nan)
            # print(processed_data["rw_noise_3458a", "flicker_noise_3458a"])
            # ax.loglog(processed_data.tau, processed_data[["rw_noise_3458a", "flicker_noise_3458a"]], marker="", alpha=1, color='black', linestyle="dotted", linewidth=1)
            # ax.loglog(processed_data.tau, processed_data["noise_gen"], marker="", label="Simulated noise", alpha=1, color='red', linewidth=1)

            lines, labels = ax.get_legend_handles_labels()
            plt.legend(lines, labels, loc="best")

    fig = plt.gcf()
    #  fig.set_size_inches(11.69,8.27)   # A4 in inch
    #  fig.set_size_inches(128/25.4 * 2.7 * 0.8, 96/25.4 * 1.5 * 0.8)  # Latex Beamer size 128 mm by 96 mm
    if plot.get("plot_size"):
        fig.set_size_inches(*plot["plot_size"])
    else:
        phi = (5**0.5 - 1) / 2  # golden ratio
        fig.set_size_inches(441.01773 / 72.27 * 0.9, 441.01773 / 72.27 * 0.9 * phi)
    if plot.get("title") is not None:
        plt.suptitle(plot["title"], fontsize=16)

    plt.tight_layout()
    if plot.get("title") is not None:
        plt.subplots_adjust(top=0.88)
    if plot.get("output_file"):
        print(f"  Saving image to '{plot['output_file']['fname']}'")
        plt.savefig(**plot["output_file"])
    if show_plot_window:
        plt.show()

    plt.close(fig)


phi = (5**0.5 - 1) / 2  # golden ratio


if __name__ == "__main__":
    plots = [


    ]


    def init_argparse() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Allan variance plotter.")
        parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
        parser.add_argument("plotfile", help="One or more yaml configurations to plot.")
        parser.add_argument("--silent", action="store_true", help="Do not show the plot when set.")

        return parser

    parser = init_argparse()
    args = parser.parse_args()
    plot_files = glob.glob(args.plotfile)
    for file_path in plot_files:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            plot_series(plot=module.plot, show_plot_window=not args.silent)
        except FileNotFoundError as exc:
            print(f"  Data file not found. Cannot plot graph: {exc}")
