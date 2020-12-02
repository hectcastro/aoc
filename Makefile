format:
	black .

lint:
	flake8 --exclude .venv .

types:
	find . -name "*.py" | grep -v .venv | xargs mypy

ci: lint types
	black --check --diff .

.PHONY: ci format lint types
