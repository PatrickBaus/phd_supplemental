import pandas as pd

import seaborn as sns

colors = sns.color_palette("colorblind")
# cmap = sns.color_palette("ch:s=-.25,rot=-.25_r", as_cmap=True)
cmap = sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)  # TODO: revert colourmap, see above
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": r"ATOMICS Master laser",
    "show": True,
    "crop": {
        "crop_index": "date",
        "crop": ["2022-06-20 04:00:00", "2022-06-20 14:00:00"],
    },
    "output_file": {
        "fname": "../images/atomics_master_barometer.pgf",
    },
    "plot_size": (441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * ((5**0.5 - 1) / 2)),
    "legend_position": "upper left",
    "primary_axis": {
        "show": True,
        "axis_settings": {
            "x_label": r"Time (UTC)",
            "y_label": r"Pressue in \unit{\hecto\pascal}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "time",
            "grid_options": [
                {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
        "x-axis": "date",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "air_pressure": {
                "label": "Air pressue",
                "color": colors[0],
            },
        },
    },
    "secondary_axis": {
        "show": True,
        "axis_settings": {
            "y_label": r"Voltage in \unit{\V}",
            "invert_x": False,
            "invert_y": True,
            "x_scale": "lin",
            "grid_options": [{"visible": False}, ],
        },
        "x-axis": "date",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "piezo_voltage": {
                "label": "Piezo voltage",
                "color": colors[3],
            },
        },
    },
    "xy_plot": {
        "show": True,
        "legend_position": "upper right",
        "x-axis": "air_pressure",
        "y-axis": "piezo_voltage",
        "annotation": {
            "label": r"({slope:.3e} ± {uncertainty:.0e}) \unit{{\V \per \hecto\pascal}}",
            "xy": (0.55, 0.1),
        },
        "columns_to_plot": {
            "piezo_voltage": {
                "label": "Piezo voltage",
                "s": 1,  # point size
                "cmap": cmap,
            },
            "fit": {
                "label": "Regression",
                "color": colors[3],
            },
        },
        "axis_settings": {
            "x_label": r"Pressure in \unit{\hecto\pascal}",
            "y_label": r"Voltage in \unit{\V}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "lin",
            "grid_options": [
                {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
    },
    "files": [
        {
            "filename": "xy_plots/laser_drift_015.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "date",
                    3: "air_pressure",
                    5: "piezo_voltage",
                },
                "scaling": {
                    "air_pressure": lambda x: x["air_pressure"] / 100,
                    "date": lambda data: pd.to_datetime(data.date, utc=True),
                },
            },
        },
    ],
}
