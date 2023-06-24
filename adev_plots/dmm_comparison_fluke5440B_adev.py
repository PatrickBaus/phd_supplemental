import pandas as pd
import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
            "description": "Fluke 5440B vs DMMs",
            "show": True,
            #'zoom': ['2021-12-03 12:30:00', '2022-04-01 08:00:00'],
            "output_file": {"fname": "../images/dmm_comparison_fluke5440B_adev.pgf"},
            "plot_size": (441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi),
            "primary_axis": {
                "label": "Voltage deviation in V",
                "plot_type": "relative",  # absolute, relative, proportional
                "columns_to_plot": {
                    "34470a": {
                        "label": r"Keysight 34470A",
                        "color": colors[5],
                        "linewidth": 1,
                    },
                    "3458a": {
                        "label": r"Keysight 3458A",
                        "color": colors[0],
                        "linewidth": 1,
                    },
                    "k2002": {
                        "label": r"Keithley Model 2002",
                        "color": colors[2],
                        "linewidth": 1,
                    },
                    "dmm6500": {
                        "label": r"Keithley DMM6500",
                        "color": colors[4],
                        "linewidth": 1,
                    },
                },
            },
            "files": [
                {
                    "filename": "adev_plots/Fluke5440B_vs_DMMs_2022-10-04_12:16:21+00:00.zip",
                    "show": True,
                    "parser": "ltspice_fets",
                    "options": {
                        "columns": {
                            0: "date",
                            1: "k2002",
                            2: "3458a",
                            3: "34470a",
                            4: "dmm6500",
                            6: "temperature",
                        },
                        "scaling": {
                            "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                        },
                    },
                },
            ],
        }
