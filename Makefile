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
	find . -name '.*.sw?' -o -name __pycache__ -o -name '*.pyc' -delete

build: clean
	$(VENV_PYTHON) setup.py bdist_wheel

tests: install-editable
	PATH=$(VENV_BIN):$(PATH) python -m pytest -vv --cov=source

coverage: install-editable
	PATH=$(VENV_BIN):$(PATH) python -m pytest -vv --cov=source --cov-report=html

lint:
	$(VENV_BIN)/flake8 .
	$(VENV_BIN)/mypy -p user_manager

format:
	$(VENV_BIN)/isort .
	$(VENV_BIN)/black .

example-cli:
	./example_cli.sh

example-api: venv install-editable
	$(VENV_PYTHON) ./example_api.py
