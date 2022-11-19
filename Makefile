VENV_BIN=.venv/bin
VENV_PYTHON=$(VENV_BIN)/python

.PHONY: build tests

venv:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

install-editable:
	$(VENV_BIN)/pip install -e .

clean:
	rm -Rf build dist *.egg-info
	find . -name '.*.sw?' -delete

build: clean
	$(VENV_PYTHON) setup.py bdist_wheel

tests:
	$(VENV_PYTHON) -m pytest -vv

lint:
	$(VENV_BIN)/flake8 .
	$(VENV_BIN)/mypy -p user_manager

isort:
	$(VENV_BIN)/isort .

black:
	$(VENV_BIN)/black .
