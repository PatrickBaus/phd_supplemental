import seaborn as sns

colors = sns.color_palette("colorblind")
phi = (5**0.5 - 1) / 2  # golden ratio
plot = {
      'description': 'Hot Swap Oscillations',
      'title': None,
      'show': False,
      "output_file": {
        "fname": "../images/hot_swap.pgf"
      },
      'crop_secondary_to_primary': True,
      "legend_position": "best",
      'primary_axis': {
        "axis_settings": {
          'x_label': r"Time in \unit{\ms}",
          'y_label': r"Voltage in \unit{\V}",
          "invert_x": False,
          "invert_y": False,
          "fixed_order": None,
          "y_scale": "linear",
        },
        'x-axis': "time",
        'plot_type': 'absolute',  # absolute, relative, proportional
        'columns_to_plot': {
            "vout": {
                "label": "Input voltage",
                "color": colors[0],
            },
        },
      },
      'files': [
        {
          'filename': 'hot_swap.txt',
          'show': True,
          'parser': 'ltspice_fets',
          'options': {
            "delimiter": "\t",
            "columns": {
              0: "time",
              1: "vout",
            },
            "scaling": {
                "time": lambda x: x["time"]*1000
            },
          },
        },
      ],
    }
