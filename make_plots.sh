#!/bin/bash
source env/bin/activate
./plot_generic.py --silent "generic_plots/*.py"
./plot_ltspice_monte-carlo.py --silent "histogram_plots/*.py"
./plot_xy.py --silent "xy_plots/*.py"
./plot_fft.py --silent "fft_plots/*.py"
./plot_allan_variance.py --silent "adev_plots/*.py"
./plot_popcorn_noise.py --silent
cd simulations
./sim_laplace_fopdt.py --silent
./sim_pid_controller_bode.py --silent
./sim_pid_controller.py --silent
./sim_output_impedance_mc.py --silent
./sim_allan_variance.py --silent
./sim_burst_noise.py --silent
deactivate
