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
        r"\sisetup{per-mode = symbol}%"
    ]),
    #"pgf.texsystem": "lualatex",
    "pgf.preamble": "\n".join([ # plots will use this preamble
        r"\usepackage{siunitx}",
        r"\sisetup{per-mode = symbol}%"
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

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PID simulator.")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
    parser.add_argument('--silent', action='store_true', help="Do not show the plot when set.")

    return parser


parser = init_argparse()
args = parser.parse_args()

def transfer_function(s, params, alpha=0):
    return params.kp + params.ki/s + + (params.kd*s)/(alpha*params.kd*s + 1)

params = PidParams(kp=1, ki=0.1, kd=0.01)
# Create time range
t = np.logspace(-2, 4)


# 2*np.pi
ax = plt.subplot(111)
plt.plot(
    t,
    abs(transfer_function(1j*t, params)),
    linewidth=1,
    alpha=0.7,
    label=rf"PID, $K_p={params.kp}$, $K_i=\qty{{{params.ki}}}{{\per \s}}$, $K_d=\qty{{{params.kd}}}{{\s}}$",
    color=colors[0],
)

plt.plot(
    t,
    abs(transfer_function(1j*t, params, alpha=0.1)),
    linewidth=1,
    alpha=0.7,
    label=rf"PID+filter,$K_p={params.kp}$, $K_i=\qty{{{params.ki}}}{{\per \s}}$, $K_d=\qty{{{params.kd}}}{{\s}}$, $\alpha=\num{0.1}$",
    color=colors[1],
)

ax.set_yscale('log')
ax.set_xscale('log')
plt.legend(loc="best")
plt.ylabel("Controller Output")

plt.xlabel(r"Frequency in \unit{\radian \per \s}")

fig = plt.gcf()
#  fig.set_size_inches(11.69,8.27)   # A4 in inch
#  fig.set_size_inches(128/25.4 * 2.7 * 0.8, 96/25.4 * 1.5 * 0.8)  # Latex Beamer size 128 mm by 96 mm
phi = (5**.5-1) / 2  # golden ratio
fig.set_size_inches(
    441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi
)  # TU thesis
plt.tight_layout()

fname = "../../images/sim_pid_controller_bode.pgf"
print(f"Saving image to '{fname}'")
plt.savefig(fname)

if not args.silent:
    plt.show()
