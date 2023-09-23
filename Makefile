# vim: noexpandtab filetype=make

PLUGIN_NAME := yf_stock_ticker
SUBDIR := $(PLUGIN_NAME)
PYTHON := venv/bin/python3
SHELLCHECK := venv/bin/shellcheck

.PHONY: help

.DEFAULT: help
help:
	@echo "make all"
	@echo "       prepare development environment, lint and test"
	@echo "make venv"
	@echo "       prepare development environment"
	@echo "make lint"
	@echo "       run linting"
	@echo "make test"
	@echo "       run tests"
	@echo "make build"
	@echo "       build release"
	@echo "make clean"
	@echo "       remove all development files and directories"

venv: venv/bin/activate

venv/bin/activate: requirements_dev.txt
	python3 -m venv venv
	$(PYTHON) -m pip install -U pip wheel
	$(PYTHON) -m pip install -r requirements_dev.txt

lint: venv $(SUBDIR)/*.sh $(SUBDIR)/*.py
	$(SHELLCHECK) $(SUBDIR)/*.sh
	$(PYTHON) -m pylint $(SUBDIR)/*.py

test: venv $(SUBDIR)/*.py
	$(PYTHON) -m pytest -v -x

all: lint test

clean_bytecode: venv
	$(PYTHON) -m pyclean . --debris

build: clean_bytecode $(SUBDIR)/*.*
	RELEASE=$$($(SUBDIR)/$(PLUGIN_NAME).sh --version) ;\
	tar --uid=0 --gid=0 -zcvf $(PLUGIN_NAME)_$${RELEASE}.tgz $(SUBDIR)

clean: clean_bytecode
	rm -rf venv
	rm -f $(PLUGIN_NAME)_*.tgz

