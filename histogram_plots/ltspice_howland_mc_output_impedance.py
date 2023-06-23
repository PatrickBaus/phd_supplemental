import numpy as np

import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
      'description': 'Howland Current Source Output Impedance',
      'show': False,
      "output_file": {
          "fname": "../images/ltspice_howland_mc_output_impedance.pgf"
      },
      'crop_secondary_to_primary': True,
      "plot_size": (441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi),
      'primary_axis': {
        "axis_settings": {
          'x_label': r"Resistance in \unit{\ohm}",
          'y_label': r"Normalised resistance density in \unit{\per \ohm}",
          "invert_x": False,
          "invert_y": False,
          "x_fixed_order": 6,
          "x_scale": "linear",
        },
        'x-axis': "num",
        'plot_type': 'absolute',  # absolute, relative, proportional
        'columns_to_plot': {
            "Rout005": {
                "label": r"HCS, \qty{0.05}{\percent} tolerance",
                "color": colors[0],
                "density": True,
                "bins": 100,
                "range": (-1e8, 1e8),
                "range": (0, 5e7),
            },
            "Rout001": {
                "label": r"HCS, \qty{0.01}{\percent} tolerance",
                "color": colors[1],
                "density": True,
                "bins": 100,
                "range": (0, 5e7),
            },
            "Routi005": {
                "label": r"Improved HCS, \qty{0.05}{\percent} tolerance",
                "color": colors[3],
                "density": True,
                "bins": 100,
                "range": (0, 5e7),
            },
            "Routi001": {
                "label": r"Improved HCS, \qty{0.01}{\percent} tolerance",
                "color": colors[2],
                "density": True,
                "bins": 100,
                "range": (0, 5e7),
            },
        },
        'filter': None,#filter_savgol(window_length=101, polyorder=3),
      },
      'files': [
        {
          'filename': 'howland_current_source_001.txt',
          'show': True,
          'parser': 'ltspice_fets',
          'options': {
            "delimiter": "\t",
            "columns": {0: "num", 1: "Rout001"},
            "scaling": {
                "Rout001": lambda x: np.abs(x["Rout001"])
            },
          },
        },
        {
          'filename': 'howland_current_source_005.txt',
          'show': True,
          'parser': 'ltspice_fets',
          'options': {
            "delimiter": "\t",
            "columns": {0: "num", 1: "Rout005"},
            "scaling": {
                "Rout005": lambda x: np.abs(x["Rout005"])
            },
          },
        },
        {
          'filename': 'improved_howland_current_source_001.txt',
          'show': True,
          'parser': 'ltspice_fets',
          'options': {
            "delimiter": "\t",
            "columns": {0: "num", 1: "Routi001"},
            "scaling": {
                "Rout005": lambda x: np.abs(x["Routi001"])
            },
          },
        },
        {
          'filename': 'improved_howland_current_source_005.txt',
          'show': True,
          'parser': 'ltspice_fets',
          'options': {
            "delimiter": "\t",
            "columns": {0: "num", 1: "Routi005"},
            "scaling": {
                "Rout005": lambda x: np.abs(x["Routi005"])
            },
          },
        },
      ],
    }
