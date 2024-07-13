#!/usr/bin/env python
import argparse
import glob
import importlib

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.legend
import numpy as np
import os
import pandas as pd
from matplotlib.ticker import ScalarFormatter
from scipy import integrate
import seaborn as sns

from file_parser import parse_file

__version__ = "0.9.0"

# Use these settings for the PhD thesis
tex_fonts = {
    "text.usetex": True,  # Use LaTeX to write all text
    "font.family": "serif",
    #"font.family": "sans-serif",
    # Use 10pt font in plots, to match 10pt font in thesis document
    # Use 9pt font in plots, to match 9pt font in presentation
    "axes.labelsize": 10,
    #"axes.labelsize": 9,
    "font.size": 10,
    #"font.size": 9,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    #"legend.fontsize": 5,
    "xtick.labelsize": 8,
    #"xtick.labelsize": 7,
    "ytick.labelsize": 8,
    #"ytick.labelsize": 7,
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
plt.style.use("tableau-colorblind10")
# end of settings


class FixedOrderFormatter(ScalarFormatter):
    """Formats axis ticks using scientific notation with a constant order of
    magnitude"""

    def __init__(self, order_of_mag=0, useOffset=False, useMathText=True):
        super().__init__(useOffset=useOffset, useMathText=useMathText)
        if order_of_mag != 0:
            self.set_powerlimits(
                (
                    order_of_mag,
                    order_of_mag,
                )
            )

    def _set_offset(self, range):
        mean_locs = np.mean(self.locs)

        if range / 2 < np.absolute(mean_locs):
            ave_oom = np.floor(np.log10(mean_locs))
            p10 = 10 ** np.floor(np.log10(range))
            self.offset = np.ceil(np.mean(self.locs) / p10) * p10
        else:
            self.offset = 0


def make_format(current, other):
    # current and other are axes
    def format_coord(x, y):
        # x, y are data coordinates
        # convert to display coords
        display_coord = current.transData.transform((x, y))
        inv = other.transData.inverted()
        # convert back to data coords with respect to ax
        ax_coord = inv.transform(display_coord)
        coords = [ax_coord, (x, y)]
        return "Left: {:<40}    Right: {:<}".format(
            *["({}, {:.6E})".format(matplotlib.dates.num2date(x).strftime("%H:%M:%S"), y) for x, y in coords]
        )

    return format_coord


def load_data(plot_file):
    print(f"  Parsing: '{plot_file['filename']}'...")
    data = parse_file(**plot_file)

    return data


def crop_data(data, crop_index=None, crop=None):
    if crop_index is not None:
        index_to_drop = (
            data[(data[crop_index] < crop[0]) | (data[crop_index] > crop[1])].index
            if len(crop) > 1
            else data[data[crop_index] < crop[0]].index
        )
        data.drop(index_to_drop, inplace=True)


def filter_rolling(window_length):
    def filter(data):
        if len(data) <= window_length:
            return None

        return data.rolling(window=window_length).mean()

    return filter


def process_data(data, columns, plot_type):
    if plot_type == "relative":
        data[columns] = data[columns] - data[columns].mean().tolist()
    elif plot_type == "proportional":
        data[columns] = data[columns] / data[columns].iloc[:30].mean().tolist() - 1


def prepare_axis(ax, axis_settings, color_map=None):
    if axis_settings.get("fixed_order") is not None:
        ax.yaxis.set_major_formatter(FixedOrderFormatter(axis_settings["fixed_order"], useOffset=True))
    else:
        ax.yaxis.get_major_formatter().set_useOffset(False)

    if axis_settings.get("y_scale") == "log":
        ax.set_yscale("log")
    if axis_settings.get("x_scale") == "log":
        ax.set_xscale("log")
    if axis_settings.get("invert_y"):
        ax.invert_yaxis()
    if axis_settings.get("invert_x"):
        ax.invert_xaxis()

    if axis_settings["grid_options"]:
        for option in axis_settings["grid_options"]:
            ax.grid(**option)

    ax.set_ylabel(axis_settings["y_label"])
    if axis_settings.get("x_label") is not None:
        ax.set_xlabel(axis_settings["x_label"])

    if color_map is not None:
        ax.set_prop_cycle("color", color_map)


def plot_data(ax, data, x_axis, column_settings):
    for column, settings in column_settings.items():
        if column in data:
            ax.plot(
                data[x_axis][~np.isnan(data[column])],
                data[column][~np.isnan(data[column])],
                color=settings["color"],
                marker="",
                label=settings["label"],
                alpha=0.7,
                linewidth=settings.get("linewidth", 1),
                linestyle=settings.get("linestyle", "-"),
                zorder=settings.get("zorder", None),
            )


def integrate_data(data, x_axis, column_settings):
    print("  Integrated current noise:")
    for column, settings in column_settings.items():
        if column in data:
            current_data = data.dropna(subset=column)
            current_data_100khz = data.dropna(subset=column)[
                (current_data[x_axis] >= 10**1) & (current_data[x_axis] <= 10**5)
            ]
            current_data = current_data[(current_data[x_axis] >= 10**1) & (current_data[x_axis] <= 10**6)]
            rms_100khz = integrate.trapezoid(current_data_100khz[column] ** 2, current_data_100khz[x_axis])
            rms = integrate.trapezoid(current_data[column] ** 2, current_data[x_axis])
            print(
                f"    {column}: {np.min(current_data_100khz[x_axis])} Hz - {np.max(current_data_100khz[x_axis])} kHz, {np.sqrt(rms_100khz):.2e} A_rms; {np.min(current_data[x_axis])} Hz - {np.max(current_data[x_axis])} kHz, {np.sqrt(rms):.2e} A_rms"
            )


def plot_series(plot, show_plot_window):
    print(f"Plotting {plot['description']}")
    # Load the data to be plotted
    plot_files = (plot_file for plot_file in plot["files"] if plot_file.get("show", True))
    data = pd.concat((load_data(plot_file)[0] for plot_file in plot_files), sort=True)

    # If we have something to plot, proceed
    if not data.empty:
        crop_data(data, **plot.get("crop", {}))

        plot_settings = plot["primary_axis"]
        process_data(
            data=data, columns=plot_settings["columns_to_plot"], plot_type=plot_settings.get("plot_type", "absolute")
        )

        ax1 = plt.subplot(111)
        prepare_axis(ax=ax1, axis_settings=plot_settings["axis_settings"], color_map=plt.cm.tab10.colors)

        x_axis = plot_settings["x-axis"]
        integrate_data(data, x_axis=x_axis, column_settings=plot_settings["columns_to_plot"])
        plot_data(ax1, data, x_axis=x_axis, column_settings=plot_settings["columns_to_plot"])

        lines, labels = ax1.get_legend_handles_labels()

        plot_settings = plot.get("secondary_axis", {})
        if plot_settings.get("show", False):
            ax2 = ax1.twinx()
            prepare_axis(ax=ax2, axis_settings=plot_settings["axis_settings"], color_map=plt.cm.tab10.colors)

            plot_data(ax2, data, x_axis=x_axis, column_settings=plot_settings["columns_to_plot"])

            lines2, labels2 = ax2.get_legend_handles_labels()
            lines += lines2
            labels += labels2
        if labels:
            plt.legend(lines, labels, loc=plot.get("legend_position", "upper left"))

    fig = plt.gcf()

    if plot.get("plot_size"):
        fig.set_size_inches(*plot["plot_size"])
    if plot.get("title") is not None:
        plt.suptitle(plot["title"], fontsize=16)

    plt.tight_layout()
#    plt.tight_layout(pad=0.1)  # Disable padding. This is done by latex. We need a bit of padding for special character.
    if plot.get("title") is not None:
        plt.subplots_adjust(top=0.88)
    if plot.get("output_file"):
        print(f"  Saving image to '{plot['output_file']['fname']}'")
        plt.savefig(**plot["output_file"])
    if show_plot_window:
        plt.show()

    plt.close(fig)


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FFT plot generator for noise plots.")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
    parser.add_argument("plotfile", help="One or more yaml configurations to plot.")
    parser.add_argument("--silent", action="store_true", help="Do not show the plot when set.")

    return parser


if __name__ == "__main__":
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
