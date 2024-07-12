import pandas as pd
import seaborn as sns

colors = sns.color_palette("colorblind", 11)
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
    "description": "011 Neon Lab (Back)",
    "show": True,
    "output_file": {"fname": "../images/pid_parameter_fit.pgf"},
    "zoom": [
        "2022-09-13 03:30:00",
        "2022-09-22 07:20:00",
    ],  # This range starts reasonably flat
    "crop_secondary_to_primary": False,
    "primary_axis": {
        "axis_settings": {
            "x_label": r"Time in \unit{\s}",
            "y_label": r"DAC outpt in \unit{\bit}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "lin",
            "y_scale": "lin",
        },
        "x-axis": "date",
        "label": r"DAC outpt in \unit{\bit}",
        "axis_fixed_order": 0,
        "columns_to_plot": {
            "output": {
                "label": "DAC output",
                "color": colors[4],
                "linewidth": 2.5,
            },
        },
    },
    "secondary_axis": {
        "show": True,
        "plot_type": "absolute",
        "axis_settings": {
            "x_label": r"Time in \unit{\s}",
            "y_label": r"Temperature in \unit{\celsius}",
            "invert_x": False,
            "invert_y": False,
            "x_scale": "lin",
            "y_scale": "lin",
            "grid_options": [{"visible": False}, ],
        },
        "columns_to_plot": {
            "temperature_labnode": {
                "label": "Temperature (LabNode)",
                "color": colors[0],
                "linewidth": 0.5,
            },
            "fit": {
                "label": "Fit",
                "color": colors[1],
                "linewidth": 2,
            },
        },
        "labels": {
            "temperature_labnode": "Temperature (Labnode)",
            "temperature_room": "Temperature (Aircon)",
            "fit": "Fit",
        },
    },
    "files": [
        {
            "filename": "fits/011_neon_back.zip",  # Neon back, 10k/10k resistors with nulls filled using locf()
            "show": True,
            "parser": "ltspice_fets",
            "options": {
                "columns": {
                    0: "date",
                    1: "output",
                    2: "temperature_room",
                    3: "temperature_labnode",
                },
                "scaling": {
                    "date": lambda x: pd.to_datetime(x.date, utc=True),
                    "temperature_labnode": lambda x: x["temperature_labnode"] - 273.15,
                    "temperature_room": lambda x: x["temperature_room"] - 273.15,
                },
            },
        },
    ],
}
