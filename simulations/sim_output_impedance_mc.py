#!/usr/bin/env python
import argparse

import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import ScalarFormatter
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


class FixedOrderFormatter(ScalarFormatter):
    """Formats axis ticks using scientific notation with a constant order of
    magnitude"""
    def __init__(self, order_of_mag=0, useOffset=False, useMathText=True):
        super().__init__(useOffset=useOffset, useMathText=useMathText)
        if order_of_mag != 0:
            self.set_powerlimits((order_of_mag,order_of_mag,))

    def _set_offset(self, range):
        mean_locs = np.mean(self.locs)

        if range / 2 < np.absolute(mean_locs):
            p10 = 10 ** np.floor(np.log10(range))
            self.offset = (np.ceil(np.mean(self.locs) / p10) * p10)
        else:
            self.offset = 0

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Output impedance simulator using Monte Carlo methods.")
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version {__version__}")
    parser.add_argument('--silent', action='store_true', help="Do not show the plot when set.")

    return parser


def f(x):
    return 2.720*3.298 / x


parser = init_argparse()
args = parser.parse_args()

mean_x = 1.85e-9
sigma_x = 1.56e-9
sLim=0.682689492137086
n_samples = int(1e8)
print(f"Rolling the dice {n_samples:.0e} times.")

np.random.seed(42)
sampled_x = np.random.normal(mean_x, sigma_x, n_samples)
result = f(sampled_x)
result = result[result>0]
ax1 = plt.subplot(111)
n, bins, _ = ax1.hist(result, range=[0,2e10], bins=400, color=colors[0])
print("Number of counts in all bins:",np.sum(n))
max_res = bins[np.argmax(n)]
gHi = np.where(result >= max_res)
gLo = np.where(result < max_res)
vSortLo = np.sort(result[gLo])
vSortHi = np.sort(result[gHi])
NormLo = vSortLo[int((1.0-sLim)*np.size(vSortLo))]
NormHi = vSortHi[int(sLim      *np.size(vSortHi))]
print(f"Most likely result: {max_res:.2e} -{max_res-NormLo:.2e} +{NormHi-max_res:.2e}")
ax1.vlines(NormLo, ymin=0, ymax=10**6, color=colors[1], label='1-sigma')
ax1.vlines(NormHi, ymin=0, ymax=10**6, color=colors[1])

plt.legend(loc="best")
ax1.grid(True, which="minor", ls="-", color='0.85')
ax1.grid(True, which="major", ls="-", color='0.45')
ax1.xaxis.set_major_formatter(FixedOrderFormatter(9, useOffset=True))
ax1.set_ylabel(r"Counts")
ax1.set_xlabel(r"Output impedance in \unit{\ohm}")
#
fig = plt.gcf()
#  fig.set_size_inches(11.69,8.27)   # A4 in inch
#  fig.set_size_inches(128/25.4 * 2.7 * 0.8, 96/25.4 * 1.5 * 0.8)  # Latex Beamer size 128 mm by 96 mm
phi = (5**.5-1) / 2  # golden ratio
fig.set_size_inches(
    441.01773 / 72.27 * 0.89, 441.01773 / 72.27 * 0.89 * phi
)  # TU thesis
plt.tight_layout()

fname = "../../images/dgDrive_output_impedance_dc_mc.pgf"
print(f"Saving image to '{fname}'")
plt.savefig(fname)

if not args.silent:
    plt.show()
