import numpy as np
import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "DgDrive vs competitors output imepdance",
    "show": True,
    "output_file": {"fname": "../images/dgDrive_output_impedance_comparison.pgf"},
    "plot_size": (441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi),
    "legend_position": "upper right",
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Frequency in \unit{\Hz}",
            "y_label": r"Output impedance in \unit{\ohm}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "log",
            "y_scale": "log",
            "grid_options": [
                {"which": "minor", "axis": "x", "ls": "-", "color": "0.85"}, {"which": "major", "ls": "-", "color": "0.45"}
            ]
        },
        "x-axis": "frequency",
        "plot_type": "absolute",  # absolute, relative, proportional
        "columns_to_plot": {
            "moglabs": {
                "label": "Moglabs DLC-202",
                "color": colors[2],
                "alpha": 1,
            },
            "vescent": {
                "label": "Vescent D2-105-500",
                "color": colors[5],
                "alpha": 1,
            },
            "smc11": {
                "label": r"Sisyph SMC11 (\qty{470}{\mA})",
                "color": colors[4],
                "alpha": 1,
            },
            "dgdrive_rth1004": {
                "label": r"DgDrive v2.3.1 (RTH1004)",
                "color": colors[3],
                "alpha": 1,
            },
            "dgdrive_rth1004_sim": {
                "label": None,
                "color": colors[3],
                "linestyle": "dashed",
                "alpha": 1,
            },
            "dgdrive_bode100": {
                "label": "DgDrive v2.3.1 (Bode 100)",
                "color": colors[0],
                "alpha": 1,
            },
            "dgdrive_bode100_sim": {
                "label": None,
                "color": colors[0],
                "linestyle": "dashed",
                "alpha": 1,
            },
            "315pF_limit": {
                "label": r"\qty{315}{\pF} limit",
                "color": "black",
                "fillstyle": "bottom",
                "linestyle": "dotted",
                "alpha": 1,
            },
        },
    },
    "files": [
        {
            "filename": "Moglabs-DLC-202",
            "show": True,
            "parser": "concat_series",
            "options": {
                "columns": {
                    0: "frequency",
                    1: "moglabs",
                },
                "scaling": {},
                "files": [
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_05Hz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_1Hz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_5Hz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_10Hz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_55Hz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_110Hz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_500Hz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_1kHz_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202+SR560_Impedance_50mA_100mVpp_5kHz_10kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 10e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202+SR560_Impedance_50mA_100mVpp_10kHz_10kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 10e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_50kHz_10gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 10,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_100kHz_100gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 100,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_500kHz_10gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 10,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Moglabs-DLC-202/Moglabs-DLC-202_Impedance_50mA_1Vpp_1MHz_10gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 10,
                            "sense_resistor": 10,
                        },
                    },
                ],
            },
        },
        {
            "filename": "Vescent D2-105-500 (SR560)",
            "show": True,
            "parser": "concat_series",
            "options": {
                "columns": {
                    0: "frequency",
                    1: "vescent",
                },
                "scaling": {},
                "files": [
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_05Hz_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,  # Fix: corrected gain
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_1Hz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,  # Fix: corrected gain
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_2500mHz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_5Hz_20kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 20e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_11Hz_20kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 20e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_26Hz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_51Hz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_110Hz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_260Hz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_510Hz_200gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 200,
                            "sense_resistor": 10,
                            "frequency": 510,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_1kHz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_2500Hz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                            "frequency": 2.5e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_5kHz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_10kHz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_25kHz_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 10,
                            "frequency": 25e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_50kHz_100gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 100,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_100kHz_50gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 50,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_250kHz_50gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 50,
                            "sense_resistor": 10,
                            "frequency": 250e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_500kHz_100gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 100,
                            "sense_resistor": 10,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/Vescent D2-105-500/Vescent-D2-105-500_Impedance_50mA_100mVpp_1MHz_200gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 200,
                            "sense_resistor": 10,
                        },
                    },
                ],
            },
        },
        {
            "filename": "SMC11",
            "show": True,
            "parser": "concat_series",
            "options": {
                "columns": {
                    0: "frequency",
                    1: "smc11",
                },
                "scaling": {},
                "files": [
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_05Hz_003HP_3LP_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_1100mHz_003HP_10LP_5kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 5e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_2600mHz_03HP_30LP_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_5500mHz_1HP_100LP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_11Hz_01HP_1kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                            "frequency": 11,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_26Hz_03HP_3kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_26Hz_03HP_3kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_26Hz_03HP_3kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_55Hz_03HP_3kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_110Hz_1HP_10kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_260Hz_3HP_30kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_510Hz_3HP_30kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_1100Hz_10HP_100kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_2600Hz_30HP_300kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_5kHz_30HP_300kLP_500gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 500,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_10kHz_100HP_1MLP_100gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 100,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_25kHz_100HP_1MLP_100gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 100,
                            "sense_resistor": 50,
                            "frequency": 25e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_50kHz_300HP_100gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 100,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_1Vpp_250kHz_3kHP_10gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 10,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_700mVpp_400kHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_700mVpp_500kHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_700mVpp_550kHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_700mVpp_600kHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_700mVpp_700kHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_500mVpp_800kHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/SMC11/SMC11_Impedance_50mA_500mVpp_1MHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                ],
            },
        },
        {
            "filename": "DgDrive v2.3.1 (RTH1004)",
            "show": True,
            "parser": "concat_series",
            "options": {
                "columns": {
                    0: "frequency",
                    1: "dgdrive_rth1004",
                },
                "scaling": {},
                "files": [
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1MR_5uA_4Vpp_0Hz55_003HP_10LP_200gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 200,
                            "sense_resistor": 1e6,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1MR_5uA_2Vpp_1Hz1_003HP_30LP_200gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 200,
                            "sense_resistor": 1e6,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1MR_5uA_4Vpp_5Hz5_003HP_100LP_200gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 200,
                            "sense_resistor": 1e6,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1MR_5uA_4Vpp_11Hz_003HP_1kLP_50gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 50,
                            "sense_resistor": 1e6,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1MR_5uA_4Vpp_26Hz_03HP_3kLP_20gain.zip",
                        "show": False,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 20,
                            "sense_resistor": 1e6,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1MR_5uA_4Vpp_55Hz_03HP_3kLP_20gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 20,
                            "sense_resistor": 1e6,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1MR_5uA_4Vpp_110Hz_1HP_10kLP_10gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 10,
                            "sense_resistor": 1e6,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_260Hz_3HP_30kLP_20kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 20e3,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_510Hz_3HP_30kLP_2kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 2e3,
                            "sense_resistor": 1e3,
                            "frequency": 510,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_1kHz_10HP_100kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_2k5Hz_30HP_300kLP_1kgain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1e3,
                            "sense_resistor": 1e3,
                            "frequency": 2.5*10**3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_5kHz_30HP_300kLP_500gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 500,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_10kHz_100HP_1MLP_200gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 200,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_25kHz_300HP_1MLP_50gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 50,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_50kHz_300HP_1MLP_50gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 50,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_100kHz_300HP_20gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 20,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_1kR_3mA_1Vpp_250kHz_300HP_20gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 20,
                            "sense_resistor": 1e3,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_50R_3mA_1Vpp_500kHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_50R_3mA_1Vpp_1MHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_50R_3mA_1Vpp_2M5Hz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_50R_3mA_1Vpp_5MHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_50R_3mA_1Vpp_10MHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                    {
                        "filename": "generic_plots/output_impedance_comparison/DgDrive_RTH1004/DgDrive-2-3-1_Impedance_50R_3mA_1Vpp_25MHz_1gain.zip",
                        "show": True,
                        "parser": "output_impedance_generic",
                        "options": {
                            "skiprows": 22,
                            "columns": {
                                0: "time",
                                1: "output_current",
                                2: "modulation_amplitude",
                            },
                            "x-axis": "time",
                            "gain": 1,
                            "sense_resistor": 50,
                        },
                    },
                ],
            },
        },
        {
            'filename': 'generic_plots/output_impedance_comparison/DgDrive-2-3-1_Impedance_simulation_RTH1004.zip',
            'show': True,
            'parser': 'ltspice_fets',
            'options': {
                "columns": {
                    0: "frequency",
                    1: "re",
                    2: "img",
                },
                "scaling": {
                    "dgdrive_rth1004_sim": lambda data: np.sqrt((data["re"] - 50) ** 2 + data["img"] ** 2),
                },
            },
        },
        {
            "filename": "generic_plots/output_impedance_comparison/DgDrive_output_impedance_2023-04-27T23_48_24.zip",
            "show": True,
            "parser": "bode100",
            "options": {
                "trace": 2,
                "columns": {
                    0: "frequency",
                    1: "dgdrive_bode100",
                },
            },
        },
        {
            'filename': 'generic_plots/output_impedance_comparison/DgDrive-2-3-1_Impedance_simulation_bode100.zip',
            'show': True,
            'parser': 'ltspice_fets',
            'options': {
                "columns": {
                    0: "frequency",
                    1: "re",
                    2: "img",
                },
                "scaling": {
                    "dgdrive_bode100_sim": lambda data: np.sqrt((data["re"] - 1000) ** 2 + data["img"] ** 2),
                },
            },
        },
        {
            'filename': 'generic_plots/output_impedance_comparison/Impedance_simulation_315pF.zip',
            'show': True,
            'parser': 'ltspice_fets',
            'options': {
                "columns": {
                    0: "frequency",
                    1: "re",
                    2: "img",
                },
                "scaling": {
                    "315pF_limit": lambda data: np.sqrt(data["re"] ** 2 + data["img"] ** 2),
                },
            },
        },
    ],
}
