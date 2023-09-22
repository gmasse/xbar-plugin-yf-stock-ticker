# vim: noexpandtab filetype=make

PLUGIN_NAME := yf_stock_ticker
SUBDIR := $(PLUGIN_NAME)
PYTHON := venv/bin/python3
SHELLCHECK := venv/bin/shellcheck

.PHONY: clean help

.DEFAULT: help
help:
	@echo "make all"
	@echo "       prepare development environment, lint and build"
	@echo "make venv"
	@echo "       prepare development environment"
	@echo "make lint"
	@echo "       run pylint"
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

build: $(SUBDIR)/*.*
	RELEASE=$$($(SUBDIR)/$(PLUGIN_NAME).sh --version) ;\
	tar --uid=0 --gid=0 -zcvf $(PLUGIN_NAME)_$${RELEASE}.tgz $(SUBDIR)

all: lint build

clean:
	rm -rf venv
	rm -f $(PLUGIN_NAME)_*.tgz

