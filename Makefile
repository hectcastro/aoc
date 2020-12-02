format:
	black .

lint:
	flake8 --exclude .venv .

ci: lint
	black --check --diff .

.PHONY: ci format lint
