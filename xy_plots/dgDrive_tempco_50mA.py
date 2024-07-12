import pandas as pd

import seaborn as sns

colors = sns.color_palette("colorblind")
# cmap = sns.color_palette("ch:s=-.25,rot=-.25_r", as_cmap=True)
cmap = sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)  # TODO: revert colourmap, see above
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": r"DgDrive-500-LN v2.3.1 (\#14, \qty{50}{\mA}) Tempco test",
    "show": True,
    "crop": {
        "crop_index": "date",
        "crop": ["2021-03-15 6:00:00", "2022-03-03 17:00:00"],
    },
    "output_file": {
        "fname": "../images/dgDrive_tempco_50mA.pgf",
    },
    "plot_size": (441.01773 / 72.27 * 0.9, 441.01773 / 72.27 * 0.9 * phi * 2),
    "legend_position": "upper right",
    "primary_axis": {
        "show": True,
        "axis_settings": {
            "x_label": r"Time (UTC)",
            "y_label": r"Current deviation in \unit{\A}",
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
                "label": "Current deviation",
                "color": colors[0],
            },
        },
    },
    "secondary_axis": {
        "show": True,
        "axis_settings": {
            "grid_options": [{"visible": False}, ],
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
        "show": True,
        "legend_position": "upper left",
        "x-axis": "temperature",
        "y-axis": "value",
        "annotation": {
            "label": r"({slope:.3e} ± {uncertainty:.0e}) \unit{{\A \per \kelvin}}",
            "xy": (0.95, 0.2),
        },
        "columns_to_plot": {
            "value": {
                "label": "Current deviation",
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
            "y_label": r"Current deviation in \unit{\A}",
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
            "filename": "xy_plots/DgDrive-2-3-1_Tempco_2021-03-16_15:59:05+00:00.zip",  # Fixed direction. Going up now
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "skiprows": 7,
                "columns": {
                    0: "date",
                    1: "value",
                    9: "temperature",
                },
                "scaling": {
                    "value": lambda x: (x["value"] - x["value"][x.date >= "2021-03-15 6:00:00"].min())
                    / 100,  # in A and relative coordinates
                    "date": lambda data: pd.to_datetime(data.date, utc=True),
                },
            },
        },
    ],
}
