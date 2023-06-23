import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "Vescent D2-105-500 gain peaking",
    "show": True,
    "output_file": {"fname": "../images/vescent_gain_peaking.pgf"},
    #'crop': {
    #    "crop_index": "frequency",
    #    "crop": [1e2, 5e6],
    # },
    "legend_position": "lower left",
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
            "vescent": {
                "label": "Vescent D2-105-500 (\qty{50}{\mA}, $V_{DS} = \qty{9.8}{\V}$)",
                "color": colors[3],
            },
            "vescent_300mA": {
                "label": "Vescent D2-105-500 (\qty{300}{\mA}, $V_{DS} = \qty{4.0}{\V}$)",
                "color": colors[0],
            },
            "vescent_400mA": {
                "label": r"Vescent D2-105-500 (\qty{400}{\mA}, $V_{DS} = \qty{1.7}{\V}$)",
                "color": colors[4],
            },
            "vescent_450mA": {
                "label": "Vescent D2-105-500 (\qty{450}{\mA}, $V_{DS} = \qty{0.5}{\V}$)",
                "color": colors[2],
            },
        },
    },
    "files": [
        {
            "filename": "./current_source_noise/vescent_d2-105-500_no_display_2kHz.csv",
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
            "filename": "./current_source_noise/vescent_d2-105-500_300mA.csv",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "vescent_300mA",
                },
                "scaling": {},
            },
        },
        {
            "filename": "./current_source_noise/vescent_d2-105-500_400mA.csv",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "vescent_400mA",
                },
                "scaling": {},
            },
        },
        {
            "filename": "./current_source_noise/vescent_d2-105-500_450mA.csv",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "vescent_450mA",
                },
                "scaling": {},
            },
        },
    ],
}
