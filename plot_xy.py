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
from scipy import stats
from statsmodels.formula.api import ols
import lttb

pd.plotting.register_matplotlib_converters()

from file_parser import parse_file

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
    "savefig.directory": os.path.dirname(os.path.realpath(__file__)),
}
plt.rcParams.update(tex_fonts)
plt.style.use("tableau-colorblind10")
# end of settings


def calculate_saturation_current(vds, kappa, ld):
    return 0.5 * kappa * vds**2 * (1 + ld * vds)


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


def crop_data(data, crop_index="date", crop=None):
    if crop is not None:
        data.sort_values(by=crop_index, inplace=True)
        index_to_drop = (
            data[(data[crop_index] < crop[0]) | (data[crop_index] > crop[1])].index
            if len(crop) > 1
            else data[data[crop_index] < crop[0]].index
        )
        data.drop(index_to_drop, inplace=True)

    # y = 1/(0.000858614 + 0.000259555 * np.log(y) + 1.35034*10**-7 * np.log(y)**3)
    # print(f"    Begin date: {data.date.iloc[0].tz_convert('Europe/Berlin')}")
    # print(f"    End date:   {data.date.iloc[-1].tz_convert('Europe/Berlin')} (+{(data.date.iloc[-1]-data.date.iloc[0]).total_seconds()/3600:.1f} h)")


def filter_butterworth(window_length=0.00005):
    from scipy.signal import filtfilt, butter

    b, a = butter(3, window_length)

    def filter(data):
        return filtfilt(b, a, data)

    return filter


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
    if axis_settings.get("x_scale") == "time":
        ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())
        # ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m-%d %H:%M"))
        ax.xaxis.set_major_formatter(matplotlib.dates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
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


def fit_data(data, x_axis, y_axis):
    model = ols(f"{y_axis} ~ {x_axis}", data).fit()

    # Calculate uncertainty for 3 sigma from the standard error
    uncertainty = (
        model.bse * stats.t.interval(0.997300203936740, len(data) - 1)[1]
    )  # 1 sigma (1-alpha = 0.682689492137086) = 68%, 2 sigma = 0.954499736103642, 3 sigma = 0.997300203936740, etc

    return {
        "intercept": model.params.Intercept,
        "slope": model.params[x_axis],
        "uncertainty": uncertainty[x_axis],
    }


def downsample_data(x_data, y_data):
    # This is hacky
    x_is_time = False
    if pd.api.types.is_datetime64_any_dtype(x_data):
        x_is_time = True
        x_data = pd.to_datetime(x_data).astype(np.int64)

    x_data, y_data = lttb.downsample(np.array([x_data, y_data]).T, n_out=1000, validators=[]).T

    if x_is_time:
        x_data = pd.to_datetime(x_data, utc=True)

    return x_data, y_data


def plot_data(ax, data, x_axis, column_settings):
    settings: dict
    for column, settings in column_settings.items():
        if column in data:
            if "cmap" in settings:
                data_points = max(len(data) // 1000, 1)
                downsampled_data = data.iloc[::data_points]
                print(f"  Scatter data downsampled to {len(downsampled_data)} points from {len(data)}.")
                ax.scatter(
                    downsampled_data[x_axis], downsampled_data[column], alpha=0.7, c=downsampled_data.date, **settings
                )
            else:
                data_to_plot = data[[x_axis, column]].dropna()
                if len(data_to_plot) > 1000:
                    x_data, y_data = downsample_data(*(data_to_plot[idx] for idx in data_to_plot))
                else:
                    x_data, y_data = (data_to_plot[idx] for idx in data_to_plot)
                print(f"  Plotting {len(x_data)} values.")
                ax.plot(x_data, y_data, marker="", alpha=0.7, **settings)


def plot_series(plot, show_plot_window):
    print(f"Plotting {plot['description']}")
    # Load the data to be plotted
    plot_files = (plot_file for plot_file in plot["files"] if plot_file.get("show", True))
    data = pd.concat((load_data(plot_file)[0] for plot_file in plot_files), sort=True)
    data.reset_index(drop=True, inplace=True)

    # If we have something to plot, proceed
    if not data.empty:
        crop_data(data, **plot.get("crop", {}))

        data = data.resample("30s", on="date").mean()
        data.reset_index(drop=False, inplace=True)
        plot_settings = plot["primary_axis"]
        number_of_plots = sum([plot[axis].get("show", 0) for axis in ("primary_axis", "xy_plot")])
        process_data(
            data=data, columns=plot_settings["columns_to_plot"], plot_type=plot_settings.get("plot_type", "absolute")
        )

        if plot_settings.get("show"):
            ax1 = plt.subplot(number_of_plots, 1, len(plt.get_fignums())+1)
            # plt.tick_params('x', labelbottom=False)
            prepare_axis(ax=ax1, axis_settings=plot_settings["axis_settings"], color_map=plt.cm.tab10.colors)

            x_axis = plot_settings["x-axis"]
            plot_data(ax1, data, x_axis=x_axis, column_settings=plot_settings["columns_to_plot"])

            lines, labels = ax1.get_legend_handles_labels()

            plot_settings = plot.get("secondary_axis", {})
            if plot_settings.get("show", False):
                ax2 = ax1.twinx()
                prepare_axis(ax=ax2, axis_settings=plot_settings["axis_settings"], color_map=plt.cm.tab10.colors)

                plot_data(ax2, data, x_axis=x_axis, column_settings=plot_settings["columns_to_plot"])

                # ax2.set_ylabel(plot_settings["label"])

                lines2, labels2 = ax2.get_legend_handles_labels()
                lines += lines2
                labels += labels2

            plt.legend(lines, labels, loc=plot.get("legend_position", "upper left"))

        plot_settings = plot["xy_plot"]
        if plot_settings.get("show"):
            ax = plt.subplot(number_of_plots, 1, len(plt.get_fignums())+1)
            x_axis = plot_settings["x-axis"]
            y_axis = plot_settings["y-axis"]
            fit = fit_data(data, x_axis, y_axis)
            data["fit"] = fit["slope"] * data[x_axis] + fit["intercept"]
            prepare_axis(ax=ax, axis_settings=plot_settings["axis_settings"], color_map=plt.cm.tab10.colors)
            plot_data(ax, data, x_axis=x_axis, column_settings=plot_settings["columns_to_plot"])
            lines2, labels2 = ax.get_legend_handles_labels()

            ax.legend(lines2, labels2, loc=plot_settings.get("legend_position", "upper left"))
            if plot_settings.get("annotation"):
                ax.annotate(
                    plot_settings["annotation"]["label"].format(slope=fit["slope"], uncertainty=fit["uncertainty"]),
                    plot_settings["annotation"]["xy"],
                    # f"Tempco: ({fit['slope']:.3e} ± {fit['uncertainty']:.2e}) \\unit[per-mode=symbol]{{\\ohm \\per \\kelvin}}",
                    # xy=(0.9,0.1),
                    xycoords="axes fraction",
                    xytext=(-5, 0),
                    textcoords="offset points",
                    horizontalalignment="right",
                    bbox=dict(
                        boxstyle="round", facecolor="white", alpha=0.8, edgecolor="0.8"
                    ),  # use the same values as the legend
                )

    fig = plt.gcf()

    if plot.get("plot_size"):
        fig.set_size_inches(*plot["plot_size"])
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


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="x-y plot generator for line and scatter plots.")
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
