import pandas as pd

import seaborn as sns

colors = sns.color_palette("colorblind")
# cmap = sns.color_palette("ch:s=-.25,rot=-.25_r", as_cmap=True)
cmap = sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)  # TODO: revert colourmap, see above
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": r"DgTemp Tempco Test",
    "show": True,
    "crop": {
        "crop_index": "date",
        "crop": ["2019-07-02 19:00:00", "2019-07-03 01:00:00"],
    },
    "output_file": {
        "fname": "../images/dgTemp_tempco.pgf",
    },
    "plot_size": (441.01773 / 72.27 * 0.8, 441.01773 / 72.27 * 0.8 * phi * 2),
    "legend_position": "upper left",
    "primary_axis": {
        "show": True,
        "axis_settings": {
            "x_label": r"Time (UTC)",
            "y_label": r"Resistance deviation in \unit{\ohm}",
            "invert_x": False,
            "invert_y": False,
            "fixed_order": -3,
            "x_scale": "time",
            "grid_options": [
                {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
        "x-axis": "date",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "value_ext": {
                "label": "Resistance deviation",
                "color": colors[0],
            },
        },
    },
    "secondary_axis": {
        "show": True,
        "axis_settings": {
            "y_label": r"Temperature in \unit{\celsius}",
            "invert_x": False,
            "invert_y": True,
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
        "legend_position": "upper right",
        "x-axis": "temperature",
        "y-axis": "value_ext",
        "annotation": {
            "label": r"({slope:.3e} ± {uncertainty:.1e}) $\textstyle \unit{{\ohm \per \kelvin}}$",
            "xy": (0.7, 0.2),
        },
        "columns_to_plot": {
            "value_ext": {
                "label": "Resistance deviation",
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
            "y_label": r"Resistance deviation in \unit{\ohm}",
            "invert_x": False,
            "invert_y": False,
            "fixed_order": -3,
            "x_scale": "lin",
            "grid_options": [
                {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
    },
    "files": [
        {
            "filename": "generic_plots/Rev2_INL_2019-07-02_08:08:20+00:00.zip",  # Shared with the stability plot
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    1: "date",
                    2: "value_ext",
                    4: "value_int",
                },
                "scaling": {
                    "value_ext": lambda x: (x["value_ext"] - x["value_ext"].mean())
                    / (2**31 - 1)
                    * 4.096
                    / (50 * 10**-6)
                    + 220e-3,
                    "value_int": lambda x: (x["value_int"] - x["value_int"].mean())
                    / (2**31 - 1)
                    * 4.096
                    / (50 * 10**-6)
                    - 25e-3,
                    # "value": lambda x : x["value"] / (2**31-1) * 4.096,# / (50*10**-6) - 25e-3,
                    "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                },
            },
        },
        {
            "filename": "xy_plots/fluke1524_2019-07-01_12:59:50+00:00.zip",  # Fixed direction. Going up now
            "show": True,
            "parser": "fluke1524",
            "options": {
                "sensor_id": 2,  # Fluke Sensor 1 = Board Temp, Sensor 2 = Ambient
                "scaling": {
                    "temperature": lambda x: x["temperature"] - 273.15,
                },
            },
        },
    ],
}
