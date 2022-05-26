.PHONY: all
all: setup.txt dev-requirements.txt

.PHONY: install
install: setup.txt dev-requirements.txt
	pip-sync $^
	pip install -e ../

setup.txt: ../pyproject.toml
	pip-compile $< --output-file $@

dev-requirements.txt: dev-requirements.in setup.txt
	pip-compile $<

%.txt: %.in
	pip-compile $<
