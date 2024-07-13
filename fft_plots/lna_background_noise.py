import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "LNA background noise",
    "show": True,
    "output_file": {"fname": "../images/lna_background_noise.pgf"},
    "legend_position": "upper right",
    "plot_size": (441.01773 / 72.27 * 0.9, 441.01773 / 72.27 * 0.9 * 0.45),  # FIXME: Change size scalar to 0.89
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Frequency in \unit{\Hz}",
            "y_label": r"Noise density in \unit[power-half-as-sqrt,per-mode=symbol]{\V \Hz\tothe{-0.5}}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "log",
            "y_scale": "log",
            "grid_options": [
                {"which": "minor", "ls": "-", "color": "0.85"}, {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
        "x-axis": "freq",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "lna_background": {
                "label": "LNA background",
                "color": colors[2],
                "linewidth": 1.5,  # FIXME: replace with 1.0
            },
            "lna_background_simulation": {
                "label": None,
                "color": colors[1],
                "linewidth": 1.5,  # FIXME: replace with 1.0
            },
            "lna_10R_background": {
                "label": r"LNA background (\qty{10}{\ohm})",
                "color": colors[0],
                "linewidth": 1.5,  # FIXME: replace with 1.0
            },
            "lna_10R_background_simulation": {
                "label": "LTSpice simulation",
                "color": colors[1],
                "linewidth": 1.5,  # FIXME: replace with 1.0
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
                    1: r"lna_10R_background",
                },
                "scaling": {
                    "lna_10R_background": lambda data: data["lna_10R_background"] * 10,
                },
            },
        },
        {
            "filename": "fft_plots/current_source_noise/lna_background.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "freq",
                    1: r"lna_background",
                },
                "scaling": {},
            },
        },
        {
            "filename": "fft_plots/current_source_noise/LNA_short_SR560_LTSpice.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "delimiter": "\t",
                "columns": {0: "freq", 1: "lna_background_simulation"},
                "scaling": {
                    # The gain is already included in the data
                    "lna_background_simulation": lambda data : data["lna_background_simulation"][(10 <= data["freq"]) & (data["freq"] <= 1e6)] / 10000.867,
                },
            },
        },
        {
            "filename": "fft_plots/current_source_noise/LNA_10R_SR560_LTSpice.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "delimiter": "\t",
                "columns": {0: "freq", 1: "lna_10R_background_simulation"},
                "scaling": {
                    #  A gain of 9800 is used as the same number is used by the FFT generator. The simulation puts
                    #  the gain at 9716.7159.
                    "lna_10R_background_simulation": lambda data : data["lna_10R_background_simulation"][(10 <= data["freq"]) & (data["freq"] <= 1e6)] / 9800,
                },
            },
        },
    ],
}
