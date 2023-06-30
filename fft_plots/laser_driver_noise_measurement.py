import numpy as np
from scipy.constants import elementary_charge

import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "DgDrive Noise comparison",
    "show": True,
    "output_file": {"fname": "../images/laser_driver_noise_measurement.pgf"},
    #'crop': {
    #    "crop_index": "frequency",
    #    "crop": [1e2, 5e6],
    # },
    "legend_position": "upper right",
    "plot_size": (441.01773 / 72.27 * 0.8 / phi, 441.01773 / 72.27 * 0.8),
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Frequency in \unit{\Hz}",
            "y_label": r"Noise density in \unit[power-half-as-sqrt,per-mode=symbol]{\A \Hz\tothe{-0.5}}",
            "invert_x": False,
            "invert_y": False,
            # "fixed_order": -9,
            "x_scale": "log",
            "y_scale": "log",
            # "y_scale": "lin",
        },
        "x-axis": "freq",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "toptica_dcc": {
                "label": "Toptica DCC 110",
                "color": colors[9],
            },
            "lqo": {
                "label": "LQO LQprO-140",
                "color": colors[1],
            },
            "moglabs": {
                "label": "Moglabs DLC-202",
                "color": colors[2],
            },
            "vescent": {
                "label": "Vescent D2-105-500 (no display)",
                "color": colors[5],
            },
            "dgDrive": {
                "label": "DgDrive-500-LN v2.3.0",
                "color": colors[3],
                "zorder": 2.02,
            },
            "dgDrive_simulation": {
                "label": "LTSpice simulation (DgDrive)",
                "color": "black",
                "zorder": 2.03,
            },
            "lna_background": {
                "label": r"LNA background (\qty{10}{\ohm})",
                "color": colors[0],
            },
            "smc11": {
                "label": "Sisyph SMC11 (\qty{470}{\mA})",
                "color": colors[4],
                "zorder": 2.01,
            },
            "tia_background": {
                "label": r"SR560 background (\qty{1}{\kilo\ohm})",
                "color": colors[7],
            },
        },
    },
    "files": [
        {
            "filename": "fft_plots/current_source_noise/lna_10R_background.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "lna_background",
                },
                "scaling": {},
            },
        },
        {
            "filename": "fft_plots/current_source_noise/dgDrive-500_2-3-0.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "dgDrive",
                },
                "scaling": {
                    # "dgDrive": lambda x: 20*np.log10(x["dgDrive"])
                },
            },
        },
        {
            "filename": "fft_plots/current_source_noise/tia_background_1k.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "tia_background",
                },
                "scaling": {},
            },
        },
        {
            "filename": "fft_plots/current_source_noise/toptica_dcc_110.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "toptica_dcc",
                },
                "scaling": {},
            },
        },
        {
            "filename": "fft_plots/current_source_noise/moglabs_dlc_202.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "moglabs",
                },
                "scaling": {},
            },
        },
        {
            "filename": "fft_plots/current_source_noise/vescent_d2-105-500_no_display.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "vescent",
                },
                "scaling": {},
            },
        },
        {
            "filename": "fft_plots/current_source_noise/smc11.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "smc11",
                },
                "scaling": {
                    # "smc11": lambda x: 20*np.log10(x["smc11"])
                },
            },
        },
        {
            "filename": "fft_plots/current_source_noise/LQprO-140.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "lqo",
                },
                "scaling": {},
            },
        },
        {
            "filename": "fft_plots/current_source_noise/current_regulator_v3_AD797+TIA_simple.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "delimiter": "\t",
                "columns": {0: "freq", 1: "dgDrive_simulation"},
                "scaling": {},
            },
        },
    ],
}
