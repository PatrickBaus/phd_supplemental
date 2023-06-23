import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "Parallel IRF9610 MOSFET Monto-Carlo Simulation",
    "show": True,
    "output_file": {"fname": "../images/ltspice_mosfet_mc_output_impedance.pgf"},
    "crop_secondary_to_primary": True,
    "plot_size": (441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi),
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Output impedance in \unit{\ohm}",
            "y_label": r"Counts",
            "invert_x": False,
            "invert_y": False,
            "y_fixed_order": None,
            "x_scale": "linear",
        },
        "x-axis": "num",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "Rout": {
                "label": "Parallel MOSFETs",
                "color": colors[1],
                # "bins": 50,
            },
            "Rout_s": {
                "label": "Single MOSFET",
                "color": colors[2],
                # "bins": auto,
            },
            "Rout_p_sigma": {
                "label": r"Parallel MOSFET $V_{DS}+1\sigma$",
                "color": colors[0],
                # "bins": auto,
            },
        },
    },
    "files": [
        {
            "filename": "mosfet_current_source_parallel_mc.csv",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {0: "num", 1: "Rout"},
                "scaling": {
                    "Rout": lambda x: 10 ** (x["Rout"] / 20),
                },
            },
        },
        {
            "filename": "mosfet_current_source_single_mc.csv",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {0: "num", 1: "Rout_s"},
                "scaling": {
                    "Rout_s": lambda x: 10 ** (x["Rout_s"] / 20),
                },
            },
        },
        {
            "filename": "mosfet_current_source_parallel_mc-sigma.csv",
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {0: "num", 1: "Rout_p_sigma"},
                "scaling": {
                    "Rout_p_sigma": lambda x: 10 ** (x["Rout_p_sigma"] / 20),
                },
            },
        },
    ],
}
