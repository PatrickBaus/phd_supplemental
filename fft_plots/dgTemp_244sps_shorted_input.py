import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "DgTemp 1.0.0, noise floor",
    "show": True,
    "output_file": {"fname": "../images/dgTemp_244sps_shorted_input.pgf"},
    #'crop': {
    #    "crop_index": "frequency",
    #    "crop": [1e2, 5e6],
    # },
    "legend_position": "upper right",
    "plot_size": (441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi),
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Frequency in \unit{\Hz}",
            "y_label": r"Noise density in \unit[power-half-as-sqrt,per-mode=symbol]{\V \Hz\tothe{-0.5}}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "log",
            "y_scale": "log",
            "grid_options": [
                {"which": "minor", "axis": "y", "ls": "-", "color": "0.85"}, {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
        "x-axis": "freq",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "dgTemp": {
                "label": "DgTemp v1.0.0, 244 Hz",
                "color": colors[0],
            },
        },
    },
    "files": [
        {
            "filename": "./fft_plots/dgTemp_244sps_shorted_input.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: "dgTemp",
                },
                "scaling": {},
            },
        },
    ],
}
