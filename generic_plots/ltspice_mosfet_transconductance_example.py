import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "MOSFET gm LTSpice example",
    "show": True,
    "output_file": {"fname": "../images/ltspice_mosfet_transconductance_example.pgf"},
    "plot_size": (441.01773 / 72.27 * 0.9, 441.01773 / 72.27 * 0.9 * phi),
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Drain Current $I_{D}$ in \unit{\A}",
            "y_label": r"Transconductance $g_m$ in \unit{\siemens}",
            "invert_x": True,
            "invert_y": False,
            "y_scale": "linear",
            "fixed_order": -3,
            "grid_options": [
                {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
        "x-axis": "Id",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "gm": {
                "label": r"$g_m$",
                "color": colors[0],
                "linewidth": 1,
            },
        },
    },
    "files": [
        {
            "filename": "generic_plots/mosfet_gm.zip",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {0: "Vsg", 1: "Id", 2: "gm"},
                "scaling": {
                    "gm": lambda x: -x["gm"],
                },
            },
        },
    ],
}
