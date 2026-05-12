install:
		python -m venv .venv
		.venv/bin/pip install --upgrade pip
		.venv/bin/pip install -r requirements.txt

clean:
		find . -type d -name ".mypy_cache" -exec rm -rf {} +
		find . -type d -name "__pycache__" -exec rm -rf {} +
		find . -type f -name "*.pyc" -delete

delete_venv:
		rm -rf .venv
