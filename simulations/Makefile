BUILD_DIR=../../images/

PGF_OBJECTS=$(SOURCES:.py=.pgf)

DOCKER=docker
DOCKER_COMMAND=run --rm -w /source/
DOCKER_MOUNT=--mount type=bind,source=`pwd`,target=/source --mount type=bind,source=$(abspath $(BUILD_DIR)),target=/images

EXAMPLE_FILES=\
	example_combined_noise_adev\
	example_combined_noise_psd\
	example_combined_noise_amplitude\
	example_random_walk_noise_amplitude\
	example_flicker_noise_amplitude\
	example_white_noise_amplitude

NOISE_FILES=$(foreach plt_name,white_noise flicker_noise random_walk_noise burst_noise autozero autozero_raw, $(foreach plt_type,amplitude psd adev,$(plt_name)_$(plt_type)))
NOISE_FILES+=drift_amplitude drift_adev flicker_noise_envelope autozero_nplcs_adev autozero_deadtime_nplcs_adev

PID_FILES=\
	sim_pid_controller_bode\
	sim_pid_controller_comparison

FOPDT_FILES=FOPDT_theory

OUTPUT_IMPEDANCE_FILES=dgDrive_output_impedance_dc_mc

all: example_plots noise_plots autozero pid fopdt output_impedance

docker:
	$(DOCKER) build ../ --tag 'thesis_figure_builder'

example_plots: docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_allan_variance_examples.py --silent

noise_plots: docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_allan_variance.py --silent
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_flicker_noise_envelope.py --silent
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_burst_noise.py --silent

autozero: docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_autozero.py --silent
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_autozero.py --silent --autozero
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_optimal_autozero.py --silent

pid: docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_pid_controller_bode.py --silent
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_pid_controller.py --silent

fopdt: docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_laplace_fopdt.py --silent

output_impedance: docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python sim_output_impedance_mc.py --silent

clean:
	@rm -f $(addprefix $(BUILD_DIR),$(addsuffix .pgf,$(NOISE_FILES)))
	@rm -f $(addprefix $(BUILD_DIR),$(addsuffix .pgf,$(EXAMPLE_FILES)))
	@rm -f $(addprefix $(BUILD_DIR),$(addsuffix .pgf,$(PID_FILES)))
	@rm -f $(addprefix $(BUILD_DIR),$(addsuffix .pgf,$(FOPDT_FILES)))
	@rm -f $(addprefix $(BUILD_DIR),$(addsuffix .pgf,$(OUTPUT_IMPEDANCE_FILES)))
