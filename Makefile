.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
CC            = g++
CFLAGS        = -fPIC -Wall
LOCATION      = $(shell pwd)
PACKAGE       = py_vmdetect
VMDETECTBASE = ./$(PACKAGE)/src
VENVDIR       = $(LOCATION)/.venv
BINDIR        = $(VENVDIR)/bin


binary:
	python setup.py build_ext

vmdetect.so: vmdetect.o
	$(CC) $(CFLAGS) -shared -o ./$(PACKAGE)/vmdetect.so *.o
	find . -name '*.o' -exec rm -f {} +

vmdetect.o: $(VMDETECTBASE)/vmdetect.cpp
	$(CC) $(CFLAGS) -c $(VMDETECTBASE)/vmdetect.cpp


define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +


clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -fr {} +
	find . -name '*.pyo' -exec rm -fr {} +
	find . -name '*~' -exec rm -fr {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

remove-venv:
	rm -rf .venv/

lint: develop ## check style with prospector
	$(BINDIR)/prospector $(PACKAGE)
	$(BINDIR)/prospector tests

test: develop ## run tests quickly with the default Python
	$(BINDIR)/python setup.py test

test-all: develop ## run tests on every Python version with tox
	$(BINDIR)/tox

coverage: develop ## check code coverage quickly with the default Python
	$(BINDIR)/coverage run --source $(PACKAGE) setup.py test
	$(BINDIR)/coverage report -m
	$(BINDIR)/coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/$(PACKAGE).rst
	rm -f docs/modules.rst
	$(BINDIR)/sphinx-apidoc -o docs/ $(PACKAGE)
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	$(BINDIR)/watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	$(BINDIR)/twine upload dist/*

dist: binary clean ## builds source and wheel package
	pip install -r requirements_dev.txt
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

develop: binary
	python3 -m venv $(VENVDIR)
	test -f $(BINDIR)/pip  && $(BINDIR)/pip install -r requirements_dev.txt
	test -f $(BINDIR)/pip  || pip install -r requirements_dev.txt
	$(BINDIR)/python setup.py develop

install: binary clean ## install the package to the active Python's site-packages
	python setup.py install
