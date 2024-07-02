import pandas as pd

import seaborn as sns

colors = sns.color_palette("colorblind")
cmap = sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "Leakage Current WIMA MKS4",
    "show": True,
    "crop": {
        "crop_index": "date",
        "crop": ["2020-03-19 20:00:00", "2023-03-20 10:11:49"],
    },
    "plot_size": (441.01773 / 72.27 * 0.9, 441.01773 / 72.27 * 0.9 * phi * 2),
    "output_file": {
        "fname": "../images/leakage_current_mks4.pgf",
    },
    "legend_position": "upper right",
    "primary_axis": {
        "show": True,
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
        "show": True,
        "legend_position": "upper left",
        "x-axis": "temperature",
        "y-axis": "value",
        "annotation": {
            "label": r"({slope:.3e} ± {uncertainty:.1e}) \unit{{\A \per \kelvin}}",
            "xy": (0.675, 0.4),
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
            "filename": "xy_plots/HP3458A_MKS4_150uF_50V_leakage_2020-03-19_13:51:19+00:00.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "date",
                    2: "value",
                    3: "temperature",
                },
                "scaling": {
                    "value": lambda x: x.value / 2.192e6,  # divide voltage by 2.192e6
                    "date": lambda data: pd.to_datetime(data.date, utc=True),
                },
            },
        },
    ],
}
