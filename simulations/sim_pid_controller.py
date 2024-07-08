#!/usr/bin/env python
import argparse
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.integrate import odeint
import seaborn as sns


colors = sns.color_palette("colorblind")
__version__ = "0.9.0"

# Use these settings for the PhD thesis
tex_fonts = {
    "text.usetex": True,  # Use LaTeX to write all text
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pgf.rcfonts": False,     # don't setup fonts from rc parameters
    "text.latex.preamble": "\n".join([ # plots will use this preamble
        r"\usepackage{siunitx}",
    ]),
    #"pgf.texsystem": "lualatex",
    "pgf.preamble": "\n".join([ # plots will use this preamble
        r"\usepackage{siunitx}",
    ]),
    "savefig.directory": os.path.dirname(os.path.realpath(__file__)),
}
plt.rcParams.update(tex_fonts)
plt.style.use("tableau-colorblind10")
# end of settings


@dataclass
class PidParams:
    """
    The PID parameters
    """

    kp: float
    ki: float
    kd: float

@dataclass
class ModelParams:
    """
    The PID parameters
    """

    K: float
    tau: float
    theta: float


class PidController:
    """
    This is an ideal PID controller. It does not include output limits or other fancy stuff, but does derivative on
    error.
    """
    def __init__(self, pid_params: PidParams):
        self.__params = pid_params
        self.__errorsum = 0
        self.__previous_input = 0

    def reset(self):
        self.__errorsum = 0
        self.__previous_input = 0

    def compute(self, setpoint:float, process_variable: float):
        """
        Computes kp * error + Int(ki * error) + kd * d/dt error
        """
        error = setpoint - process_variable

        self.__errorsum += self.__params.ki * error
        d_error = self.__params.kd * (self.__previous_input - process_variable)

        # Update internal state and return the computed value
        self.__previous_input = process_variable

        return self.__params.kp * error + self.__errorsum + d_error

class FOPDTModel:
    def __init__(self, model_params: ModelParams, time):
        self.__params = model_params
        self.__time_offset = int(np.round((time[-1] - time[0]) / len(time) * model_params.theta))

    def __compute(self, process_variable, timestamp, pid_input):
        # Ensure causality. If the timestamp is from the past, there is no information about the future
        if timestamp <= self.__params.theta:
            return 0

        return (-process_variable + self.__params.K * pid_input) / self.__params.tau

    def compute(self, PV, ts, CV):
        _,y = odeint(self.__compute, PV, ts, args=(CV[i+1-self.__time_offset], ))
        return y[0]

params = {
    "Ziegler-Nichols": PidParams(kp=596.36/4095, ki=1.06/4095, kd=0),        # Z-N
    "SIMC": PidParams(kp=331.31/4095, ki=0.84/4095, kd=0),      # SIMC
    "AMIGO": PidParams(kp=134.48/4095, ki=0.37/4095, kd=0),     # AMIGO
}
plot_colors = {
    "Ziegler-Nichols": colors[0],
    "SIMC": colors[1],
    "AMIGO": colors[4],
}

controller = {
    key: PidController(params[key]) for key in params
}

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PID simulator.")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
    parser.add_argument('--silent', action='store_true', help="Do not show the plot when set.")

    return parser


parser = init_argparse()
args = parser.parse_args()

model = ModelParams(K=0.0032*4095, tau=395, theta=187)
# Create time range
t_max = 3600    # in s
t = np.arange(start=0, stop=t_max, step=1)
plant = FOPDTModel(model, t)

SP = np.zeros(len(t))
PVs = {
    key: np.zeros(len(t)) for key in params
}
CVs = {
    key: np.zeros(len(t)) for key in params
}

# Init setpoint
SP[0:10] = 0  # initial setpoint
SP[10:] = 1.0  # initial setpoint

# Loop over the time and calculate the PID controller outputs
for i in range(len(t)-1):
    time_step = [t[i], t[i + 1]]
    for param_type in params:
        CVs[param_type][i+1] = controller[param_type].compute(SP[i], PVs[param_type][i])
        PVs[param_type][i+1] = plant.compute(PVs[param_type][i], time_step, CVs[param_type])


ax = plt.subplot(111)
for i, param_type in enumerate(params):
    plt.plot(
        t / 60,
        PVs[param_type],
        linewidth=1,
        alpha=0.7,
        label=param_type,
        color=plot_colors[param_type],
    )

plt.plot(
    t / 60,
    SP,
    linewidth=1,
    linestyle="dashed",
    alpha=0.7,
    label=f"Setpoint",
    color=colors[2],
)
# ax.set_yscale('log')
# ax.set_xscale('log')
plt.legend(loc="best")
plt.ylabel(r"Temperature deviation in \unit{\K}")
plt.xlabel(r"Time in \unit{\minute}")
#
fig = plt.gcf()
#  fig.set_size_inches(11.69,8.27)   # A4 in inch
#  fig.set_size_inches(128/25.4 * 2.7 * 0.8, 96/25.4 * 1.5 * 0.8)  # Latex Beamer size 128 mm by 96 mm
phi = (5**.5-1) / 2  # golden ratio
fig.set_size_inches(
    441.01773 / 72.27 * 0.9, 441.01773 / 72.27 * 0.9 * phi  # FIXME: reduce factor to 0.89
)  # TU thesis
plt.tight_layout()

fname = "../../images/sim_pid_controller_comparison.pgf"
print(f"Saving image to '{fname}'")
plt.savefig(fname)

if not args.silent:
    plt.show()
