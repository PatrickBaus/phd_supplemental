import pandas as pd

import seaborn as sns

colors = sns.color_palette("colorblind")
# cmap = sns.color_palette("ch:s=-.25,rot=-.25_r", as_cmap=True)
cmap = sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)  # TODO: revert colourmap, see above
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "Leakage Current Nichicon UKL",
    "show": True,
    "crop": {
        "crop_index": "date",
        "crop": ["2019-12-28 02:00:00", "2019-12-28 18:00:00"],
    },
    "plot_size": (441.01773 / 72.27 * 0.9, 441.01773 / 72.27 * 0.9 * phi * 2),
    "output_file": {
        "fname": "../images/leakage_current_ukl.pgf",
    },
    "legend_position": "best",
    "primary_axis": {
        "show": True,
        "axis_settings": {
            "x_label": r"Time (UTC)",
            "y_label": r"Leakage current in \unit{\A}",
            "invert_x": False,
            "invert_y": False,
            "fixed_order": -9,
            "x_scale": "time",
            "grid_options": [
                {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
        "x-axis": "date",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "value": {
                "label": "Leakage current",
                "color": colors[0],
            },
        },
    },
    "secondary_axis": {
        "show": True,
        "axis_settings": {
            "y_label": r"Temperature in \unit{\celsius}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "lin",
            "grid_options": [{"visible": False}, ],
        },
        "x-axis": "date",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "temperature": {
                "label": "Temperature",
                "color": colors[3],
            },
        },
    },
    "xy_plot": {
        "show": True,
        "legend_position": "upper left",
        "x-axis": "temperature",
        "y-axis": "value",
        "annotation": {
            "label": r"({slope:.3e} ± {uncertainty:.1e}) $\textstyle \unit{{\A \per \kelvin}}$",
            "xy": (0.95, 0.2),
        },
        "columns_to_plot": {
            "value": {
                "label": "Leakage current",
                "s": 1,  # point size
                "cmap": cmap,
            },
            "fit": {
                "label": "Regression",
                "color": colors[3],
            },
        },
        "axis_settings": {
            "x_label": r"Temperature in \unit{\celsius}",
            "y_label": r"Leakage current in \unit{\A}",
            "invert_x": False,
            "invert_y": False,
            "fixed_order": -9,
            "x_scale": "lin",
            "grid_options": [
                {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
    },
    "files": [
        {
            "filename": "xy_plots/HP3458A_UKL_330uF_leakage_2019-12-27_11:25:34+00:00.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "date",
                    1: "value",
                    2: "temperature",
                },
                "scaling": {
                    "value": lambda x: x.value / 2.192e6,  # divide voltage by 2.192e6
                    "date": lambda data: pd.to_datetime(data.date, utc=True),
                },
            },
        },
    ],
}
