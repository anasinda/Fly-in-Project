install:
		python -m venv .venv
		.venv/bin/pip install --upgrade pip
		.venv/bin/pip install -r requirements.txt

clean:
		rm -rf __pycache__ */__pycache__ *.pyc .mypy_cache

delete_venv:
		rm -rf .venv
