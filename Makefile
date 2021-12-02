format:
	pipenv run black 2020
	pipenv run isort 2020

lint:
	pipenv run flake8 2020

types:
	find 2020 -name "*.py" | xargs -n1 pipenv run mypy

ci: lint types
	pipenv run black --check --diff 2020

.PHONY: ci format lint types
