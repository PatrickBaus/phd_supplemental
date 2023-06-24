import pandas as pd

import seaborn as sns

colors = sns.color_palette("colorblind")
cmap = sns.color_palette("ch:s=-.25,rot=-.25_r", as_cmap=True)
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "Leakage Current Nichicon UKL",
    "show": True,
    "crop": {
        "crop_index": "date",
        "crop": ["2019-12-28 02:00:00", "2019-12-28 18:00:00"],
    },
    "output_file": {
        "fname": "../images/leakage_current_ukl.pgf",
    },
    "legend_position": "best",
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Time (UTC)",
            "y_label": r"Leakage current in \unit{\A}",
            "invert_x": False,
            "invert_y": False,
            "fixed_order": -9,
            # "y_scale": "lin",
            "x_scale": "time",
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
            "show_grid": False,
            "y_label": r"Temperature in \unit{\celsius}",
            "invert_x": False,
            "invert_y": False,
            # "fixed_order": 9,
            # "y_scale": "lin",
            "x_scale": "lin",
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
        "legend_position": "upper left",
        "x-axis": "temperature",
        "y-axis": "value",
        "annotation": {
            "label": r"({slope:.3e} ± {uncertainty:.1e}) \unit{{\A \per \kelvin}}",
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
            # "y_scale": "lin",
            "x_scale": "lin",
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
