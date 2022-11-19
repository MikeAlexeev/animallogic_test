VENV_BIN=.venv/bin
VENV_PYTHON=$(VENV_BIN)/python

.PHONY: build

venv: 
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

install:
	$(VENV_PYTHON) setup.py install 

clean:
	rm -Rf build dist *.egg-info

build: clean
	$(VENV_PYTHON) setup.py bdist_wheel

check:
	$(VENV_BIN)/flake8 .

black:
	$(VENV_BIN)/black .
