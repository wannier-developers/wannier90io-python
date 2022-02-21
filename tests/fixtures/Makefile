WANNIER90_VERSIONS := 2.0.1 2.1 3.0.0 3.1.0

FIXTURE_DIRS := $(foreach version,$(WANNIER90_VERSIONS),./wannier90-$(version))
WANNIER90_FIXTURES := $(foreach version,$(WANNIER90_VERSIONS),_wannier90-$(version))

.PHONY: default
default: $(WANNIER90_FIXTURES)

.PHONY: $(WANNIER90_FIXTURES)
$(WANNIER90_FIXTURES): _wannier90-%: | $(FIXTURE_DIRS)
	./setup.sh $*
	cp fixtures.mk ./wannier90-$*
	WANNIER90_VERSION=$* $(MAKE) -C ./wannier90-$* -f fixtures.mk

$(FIXTURE_DIRS):
	mkdir -p $@

.PHONY: clean
clean:
	- rm -rf $(FIXTURE_DIRS)
