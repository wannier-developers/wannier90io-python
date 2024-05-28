W90 = $(abspath ../../wannier90.x)
POSTW90 = $(abspath ../../postw90.x)
W90CHK2CHK = $(abspath ../../w90chk2chk.x)

EXAMPLES_1 = $(foreach idx,01 02 03 04,example$(idx))
EXAMPLES_2 = $(foreach idx,05 06 07 09 10 11 13 17 18 19 20,example$(idx))
EXAMPLES = $(EXAMPLES_1) $(EXAMPLES_2)

define seedname
	$(basename $(wildcard *.win))
endef

define normalize_seedname
	$(foreach fname, $(wildcard $(call seedname)*), mv $(fname) $(addsuffix $(suffix $(fname)), wannier);)
endef

ifeq ($(WANNIER90_VERSION), 2.0.1)
	WRITE_HR = "hr_plot=true"
else
	WRITE_HR = "write_hr=true"
endif

# Only implemented in version 3.x
ifeq ($(WANNIER90_VERSION), 2.0.1)
	WRITE_U_MATRICES = ""
else ifeq ($(WANNIER90_VERSION), 2.1)
	WRITE_U_MATRICES = ""
else
	WRITE_U_MATRICES = "write_u_matrices=true"
endif

define modify_win
	echo $(WRITE_HR) >> wannier.win
	echo "write_xyz=true" >> wannier.win
	echo "bands_plot=true" >> wannier.win
	echo "kpath=true" >> wannier.win
	echo "kpath_task=bands" >> wannier.win
	echo "geninterp=true" >> wannier.win
endef

.PHONY: default
default: $(EXAMPLES)

.PHONY: $(EXAMPLES)
$(EXAMPLES):
	cp fixtures.mk ./examples/$@
	$(MAKE) -C ./examples/$@ -f fixtures.mk run-$@

.PHONY: $(foreach example,$(EXAMPLES_2),run-$(example))
$(foreach example,$(EXAMPLES_2),run-$(example)):
	$(call normalize_seedname)
	$(W90) -pp wannier

.PHONY: run-example01
run-example01:
	$(call normalize_seedname)
	$(W90) -pp wannier
	echo "write_xyz=true" >> wannier.win
	$(W90) wannier
	$(W90CHK2CHK) -export wannier

.PHONY: run-example02
run-example02:
	$(call normalize_seedname)
	$(W90) -pp wannier
	echo $(WRITE_HR) >> wannier.win
	echo "write_xyz=true" >> wannier.win
	$(W90) wannier
	$(W90CHK2CHK) -export wannier

.PHONY: run-example03
run-example03:
	$(call normalize_seedname)
	$(W90) -pp wannier
	$(call modify_win)
	$(W90) wannier
	$(W90CHK2CHK) -export wannier
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90) wannier

.PHONY: run-example04
run-example04:
	$(call normalize_seedname)
	$(W90) -pp wannier
	$(call modify_win)
	echo "geninterp_alsofirstder=true" >> wannier.win
	echo $(WRITE_U_MATRICES) >> wannier.win
	$(W90) wannier
	$(W90CHK2CHK) -export wannier
	echo "" >> wannier_geninterp.kpt
	echo "crystal" >> wannier_geninterp.kpt
	head -n 1 wannier_band.kpt >> wannier_geninterp.kpt
	awk 'FNR > 1 {OFS=" "; print NR-1,$$1,$$2,$$3}' wannier_band.kpt >> wannier_geninterp.kpt
	$(POSTW90) wannier
