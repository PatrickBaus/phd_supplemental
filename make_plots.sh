#!/bin/bash
source env/bin/activate
./plot_generic.py --silent "generic_plots/*.py"
cd simulations
./sim_laplace_fopdt.py --silent
deactivate
