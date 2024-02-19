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
	. $(VENV); pytest --cov-report=term \
		--cov-report=xml:reports/coverage/coverage.xml \
		--cov-report=html:_pages_build/coverage_report/ \
		--junitxml=reports/junit/junit.xml \
		--cov=src \
		--cov-fail-under=100

	# Remove .gitignore inside html report folder to send it to GH pages
	rm _pages_build/coverage_report/.gitignore

	. $(VENV); flake8 src \
		--exit-zero \
		--format=html \
		--htmldir ./_pages_build/flake8 \
		--statistics --tee \
		--output-file reports/flake8/flake8stats.txt

badges:
	. $(VENV); genbadge tests -o docs/badges/tests.svg
	. $(VENV); genbadge coverage -o docs/badges/coverage.svg
	. $(VENV); genbadge flake8 -o docs/badges/flake8.svg


# Build commands
build: venv
	rm -rf ./dist
	rm -rf ./build
	. $(VENV); python setup.py sdist bdist_wheel

