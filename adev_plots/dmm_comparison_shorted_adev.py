import pandas as pd
import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
            "description": "DMMs shorted input",
            "show": True,
            #'zoom': ['2021-12-03 12:30:00', '2022-10-14 18:04:27.561289+02:00'],
            "output_file": {"fname": "../images/dmm_comparison_shorted_adev.pgf"},
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
                    "34470a_noaz": {
                        "label": r"Keysight 34470A (No AZ)",
                        "color": colors[1],
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
                    "k2002_noaz": {
                        "label": r"Keithley Model 2002 (No AZ)",
                        "color": colors[3],
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
                    "filename": "adev_plots/DMM_shorted_input_3458a_2022-11-19_08:42:49+00:00.zip",
                    "show": True,
                    "parser": "ltspice_fets",
                    "options": {
                        "columns": {
                            0: "date",
                            1: "3458a",
                        },
                        "scaling": {
                            "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                        },
                    },
                },
                {
                    "filename": "adev_plots/DMM_shorted_input_k2002_2022-11-21_08:19:36+00:00.zip",
                    "show": True,
                    "parser": "ltspice_fets",
                    "options": {
                        "columns": {
                            0: "date",
                            1: "k2002",
                        },
                        "scaling": {
                            "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                        },
                    },
                },
                {
                    "filename": "adev_plots/DMM_shorted_input_k2002_2022-12-06_21:21:42+00:00.zip",
                    "show": False,
                    "parser": "ltspice_fets",
                    "options": {
                        "columns": {
                            0: "date",
                            1: "k2002_noaz",
                        },
                        "scaling": {
                            "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                        },
                    },
                },
                {
                    "filename": "adev_plots/DMM_shorted_input_34470a_2022-12-02_16:56:31+00:00.zip",
                    "show": True,
                    "parser": "ltspice_fets",
                    "options": {
                        "columns": {
                            0: "date",
                            1: "34470a",
                        },
                        "scaling": {
                            "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                        },
                    },
                },
                {
                    "filename": "adev_plots/DMM_shorted_input_34470a_2022-11-29_11:49:13+00:00.zip",
                    "show": False,
                    "parser": "ltspice_fets",
                    "options": {
                        "columns": {
                            0: "date",
                            1: "34470a_noaz",
                        },
                        "scaling": {
                            "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                        },
                    },
                },
                {
                    "filename": "adev_plots/DMM_shorted_input_dmm6500_2022-11-21_13:47:07+00:00.zip",
                    "show": True,
                    "parser": "ltspice_fets",
                    "options": {
                        "columns": {
                            0: "date",
                            1: "dmm6500",
                        },
                        "scaling": {
                            "date": lambda data: pd.to_datetime(data.date, utc=True, format="ISO8601"),
                        },
                    },
                },
            ],
        }
