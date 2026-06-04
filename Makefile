PYTHON = python3
MAIN = main.py
MAP ?= maps/easy/01_linear_path.txt

all: install

install:
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(MAP)

debug:
	$(PYTHON) -m pdb $(MAIN) $(MAP)

venv:
	$(PYTHON) -m venv .venv

clean:
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 *.py
	mypy *.py --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 *.py
	mypy *.py --strict

.PHONY: all install run debug venv clean lint lint-strict
