VENV = ./activate_venv

REQUIREMENTS_FREEZE ?= requirement-freeze.txt
DIR := $(shell pwd)
export PYTHONPATH := $(DIR)/src

.PHONY : venv

# Virtual environment commands
venv: # Create virtualenv
	python3 -m venv venv
	. $(VENV); python -m pip --no-cache-dir install pip wheel --upgrade;
	. $(VENV); python -m pip --no-cache-dir install -U -q -c constraints.txt pip
	. $(VENV); python -m pip --no-cache-dir install -U -c constraints.txt -r requirements-dev.txt

update: # Update dependencies
	. $(VENV); python -m pip install -U -c constraints.txt -r requirements-dev.txt

freeze: venv # Generate list of installed dependencies
	. $(VENV); pip freeze --exclude-editable > $(REQUIREMENTS_FREEZE)

# Test commands
test:
	. $(VENV); pytest --cov-report=term --cov-report=html --cov=src
	. $(VENV); coverage-badge -f -o badges/coverage.svg

# Build commands
build: venv
	rm -rf ./dist
	rm -rf ./build
	. $(VENV); python setup.py sdist
	. $(VENV); python -m pip install .
