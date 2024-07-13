SOURCE_DIR_GENERIC=generic_plots
SOURCE_DIR_HISTOGRAM=histogram_plots
# FIXME
SOURCE_DIR_XY=xy_plots
# FIXME
SOURCE_DIR_FFT=fft_plots
SOURCE_DIR_ADEV=adev_plots
SOURCE_DIR_FITS=fits
SOURCE_DIR_POPCORN=popcorn_noise_plots
SOURCE_DIR_INL=inl_plots

# Use this to filter out certain files if they should not be plotted
SOURCE_FILTER =

SOURCE_DIRS = \
	$(SOURCE_DIR_GENERIC)\
	$(SOURCE_DIR_HISTOGRAM)\
	$(SOURCE_DIR_XY)\
	$(SOURCE_DIR_FFT)\
	$(SOURCE_DIR_ADEV)\
	$(SOURCE_DIR_FITS)\
	$(SOURCE_DIR_POPCORN)\
	$(SOURCE_DIR_INL)
SOURCES = $(filter-out $(SOURCE_FILTER), $(foreach src_dir,$(SOURCE_DIRS), $(wildcard $(src_dir)/*.py)))

BUILD_DIR=../images/

PGF_OBJECTS=$(SOURCES:.py=.pgf)

DOCKER=docker
DOCKER_COMMAND=run --rm -w /figures/
DOCKER_MOUNT=--mount type=bind,source=`pwd`,target=/figures --mount type=bind,source=$(abspath $(BUILD_DIR)),target=/images

all: $(PGF_OBJECTS) simulations

docker:
	$(DOCKER) build . --tag 'thesis_figure_builder'

$(SOURCE_DIR_GENERIC)/%.pgf: $(SOURCE_DIR_GENERIC)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python plot_generic.py --silent $<

$(SOURCE_DIR_HISTOGRAM)/%.pgf: $(SOURCE_DIR_HISTOGRAM)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python plot_ltspice_monte-carlo.py --silent $<

$(SOURCE_DIR_XY)/%.pgf: $(SOURCE_DIR_XY)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python plot_xy.py --silent $<

$(SOURCE_DIR_FFT)/%.pgf: $(SOURCE_DIR_FFT)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python plot_fft.py --silent $<

$(SOURCE_DIR_ADEV)/%.pgf: $(SOURCE_DIR_ADEV)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python plot_allan_variance.py --silent $<

$(SOURCE_DIR_FITS)/%.pgf: $(SOURCE_DIR_FITS)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python fit_kraken.py --silent $<

$(SOURCE_DIR_POPCORN)/%.pgf: $(SOURCE_DIR_POPCORN)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python plot_popcorn_noise.py --silent $<

$(SOURCE_DIR_INL)/%.pgf: $(SOURCE_DIR_INL)/%.py docker
	$(DOCKER) $(DOCKER_COMMAND) $(DOCKER_MOUNT) thesis_figure_builder \
		python plot_inl.py --silent $<

.PHONY: simulations
simulations:
	cd simulations && $(MAKE)

debug:
	$(DOCKER) $(DOCKER_COMMAND) -it $(DOCKER_MOUNT) thesis_figure_builder \
		bash

clean:
	@rm -f $(addprefix $(BUILD_DIR),$(notdir $(PGF_OBJECTS)))
	@cd simulations && $(MAKE) clean
