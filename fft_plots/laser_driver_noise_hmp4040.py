import numpy as np
from scipy.constants import elementary_charge

import seaborn as sns

colors = sns.color_palette("colorblind", 11)
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "DgDrive vs HMP4040",
    "show": False,
    "output_file": {"fname": "../images/laser_driver_noise_hmp4040.pgf"},
    #'crop': {
    #    "crop_index": "frequency",
    #    "crop": [1e2, 5e6],
    # },
    "legend_position": "upper right",
    "plot_size": (441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi),
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Frequency in \unit{\Hz}",
            "y_label": r"Noise density in \unit[power-half-as-sqrt,per-mode=symbol]{\A \Hz\tothe{-0.5}}",
            "invert_x": False,
            "invert_y": False,
            # "fixed_order": -9,
            "x_scale": "log",
            "y_scale": "log",
        },
        "x-axis": "freq",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "dgDrive": {
                "label": "DgDrive-500-LN v2.3.0",
                "color": colors[3],
            },
            "dgDrive_hmp4040": {
                "label": "DgDrive-500-LN v2.1.0 (HMP4040)",
                "color": colors[10],
            },
            "dgDrive_simulation": {
                "label": "LTSpice simulation (DgDrive)",
                "color": "black",
            },
            "shot_noise_200mA": {
                "label": r"Shot noise, \qty{200}{\mA}",
                "color": "red",
                "linestyle": "dotted",
                "linewidth": 1.5,
            },
            "shot_noise_100mA": {
                "label": r"Shot noise, \qty{100}{\mA}",
                "color": "red",
                "linestyle": "dashed",
                "linewidth": 1.5,
            },
            "shot_noise_20mA": {
                "label": r"Shot noise, \qty{20}{\mA}",
                "color": "red",
                "linestyle": "dashdot",
                "linewidth": 1.5,
            },
        },
    },
    "files": [
        {
            "filename": "./current_source_noise/dgDrive-500_2-3-0.csv",
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
            "filename": "./current_source_noise/dgDrive-500_2-1-0_hmp4040.csv",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "dgDrive_hmp4040",
                },
                "scaling": {
                    # "dgDrive": lambda x: 20*np.log10(x["dgDrive"])
                },
            },
        },
        {
            "filename": "current_regulator_v3_AD797+TIA_simple.txt",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "delimiter": "\t",
                "columns": {0: "freq", 1: "dgDrive_simulation"},
                "scaling": {
                    "shot_noise_100mA": lambda data: np.ones_like(data["freq"]) * np.sqrt(2 * elementary_charge * 0.1),
                    "shot_noise_200mA": lambda data: np.ones_like(data["freq"]) * np.sqrt(2 * elementary_charge * 0.18),
                    "shot_noise_20mA": lambda data: np.ones_like(data["freq"]) * np.sqrt(2 * elementary_charge * 0.02),
                },
            },
        },
    ],
}
