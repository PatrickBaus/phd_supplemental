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
class Model:
    """
    The process model parameters
    """

    k: float
    tau: float
    theta: float


def process(y, t, u, k, tau):
    """
    u: float
        unit step height
    k: float
        process gain
    tau: float
        time constant of the process
    """
    dydt = -y / tau + k / tau * u
    return dydt


def calc_response(t, m, u):
    # Number of steps. Do one more step, because we need to do the unit step `u` in the first step. This will later
    # be stripped
    ns = len(t) - 1 + 1

    delta_t = t[1] - t[0]

    op = np.full(ns + 1, u)  # controller output
    pv = np.zeros(ns + 1)  # process variable

    # step input
    op[0] = 0

    # Simulate time delay
    ndelay = int(np.ceil(m.theta / delta_t))

    # Create the pv by iterating over the time steps
    for i in range(ns):
        # time delay
        iop = max(0, i - ndelay)
        # Integrate the differential equation
        _, y = odeint(process, pv[i], [0, delta_t], args=(op[iop], m.k, m.tau))
        pv[i + 1] = y[0]
    return (
        pv[1:],
        op[1:],
    )  # strip off the first value, which was used for the input step


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PID simulator.")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
    parser.add_argument('--silent', action='store_true', help="Do not show the plot when set.")

    return parser


parser = init_argparse()
args = parser.parse_args()

ns = 100
# Create time range
t = np.linspace(0, ns / 10.0, ns + 1)

# Set the model parameters
model = Model(k=1, tau=2.0, theta=4.0)
step_size = 1.0

pv, _ = calc_response(t, model, u=step_size)
pv2 = [
    model.k * (1.0 - np.exp(-(t[i] - model.theta) / model.tau)) for i in range(len(t))
]

ax = plt.subplot(111)
plt.plot(
    t,
    pv2,
    linewidth=1.5,
    label=r"$1-e^{-\frac{t-\theta}{\tau} }$",
    alpha=0.7,
    linestyle="dashed",
    color=colors[0],
)
plt.plot(
    [t[0], model.theta, model.theta + 0.0001, t[-1]],
    [0, 0, 1, 1],
    linewidth=1.5,
    label=r"$H(t- \theta)$",
    alpha=0.7,
    linestyle="dotted",
    color=colors[2],
)

plt.plot(t, pv, linewidth=1.5, label=r"$y(t)$", color=colors[3])
plt.legend(loc="best")
plt.ylabel("Process Output")
plt.ylim([-1, 1.5])

plt.xlim([0, 10])

plt.xlabel("Time")

fig = plt.gcf()
#  fig.set_size_inches(11.69,8.27)   # A4 in inch
#  fig.set_size_inches(128/25.4 * 2.7 * 0.8, 96/25.4 * 1.5 * 0.8)  # Latex Beamer size 128 mm by 96 mm
phi = (5**.5-1) / 2  # golden ratio
fig.set_size_inches(
    441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi
)  # TU thesis
plt.tight_layout()

fname = "../../images/FOPDT_theory.pgf"
print(f"Saving image to '{fname}'")
plt.savefig(fname)

if not args.silent:
    plt.show()
