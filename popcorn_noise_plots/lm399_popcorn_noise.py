import pandas as pd
import seaborn as sns

colors = sns.color_palette("colorblind", 11)
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "LM399 Burnin",
    "show": True,
    "output_file": {"fname": "../images/lm399_popcorn_noise.pgf"},
    "crop": {
        "crop_index": "date",
        "crop": ["2022-08-31 06:00:00", "2022-09-01 06:00:00"],
    },  # popcorn noise comparison, used in PhD thesis
    "primary_axis": {
        "axis_settings": {
            "show_grid": False,
            "fixed_order": -6,
            "x_scale": "time",
            "y_scale": "lin",
            # "limits_y": [22.75, 23.25],
        },
        "x-axis": "date",
        "plot_type": "relative",  # absolute, relative, proportional
        "axis_fixed_order": 0,
        "columns_to_plot": {  # popcorn noise comparison, used in PhD thesis
            "k2002_ch1": {
                "label": r"K2002 CH1",
                "color": colors[0],
                "linewidth": 0.5,
            },
            "k2002_ch9": {
                "label": r"K2002 CH9",
                "color": colors[0],
                "linewidth": 0.5,
            },
            "k2002_ch10": {
                "label": r"K2002 CH10",
                "color": colors[0],
                "linewidth": 0.5,
            },
        },
        "options": {
            "show_filtered_only": False,
        },
    },
    "files": [
        {
            "filename": "popcorn_noise_plots/LM399_popcorn_noise_test_2022-08-19_18:00:34+00:00.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {0: "date", 1: "k2002_ch1", 9: "k2002_ch9", 10: "k2002_ch10"},
                "scaling": {
                    "date": lambda data: pd.to_datetime(data.date, utc=True),
                },
            },
        },
    ],
}
