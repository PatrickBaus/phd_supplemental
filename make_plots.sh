#!/bin/bash
source env/bin/activate
./plot_generic.py --silent "generic_plots/*.py"
./plot_ltspice_monte-carlo.py --silent "histogram_plots/*.py
cd simulations
./sim_laplace_fopdt.py --silent
./sim_pid_controller_pode.py --silent
./sim_pid_controller.py --silent
deactivate
