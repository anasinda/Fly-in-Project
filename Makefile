PYTHON = python3
MAIN = main.py
MAP ?= maps/easy/01_linear_path.txt


all: install

install:
		pip install -r requirements.txt

run:
		$(PYTHON) $(MAIN) $(MAP)

clean:
		find . -type d -name ".mypy_cache" -exec rm -rf {} +
		find . -type d -name "__pycache__" -exec rm -rf {} +
		find . -type f -name "*.pyc" -delete

lint:
	mypy *.py
	flake8 *.py

.PHONY: install run clean lint
