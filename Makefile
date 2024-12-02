format:
	pipenv run ruff format 2020 2021 2024

lint:
	pipenv run ruff check 2020 2021 2024

types:
	find 2020 -type d | tail -n +2 | xargs -n1 pipenv run mypy
	find 2021 -type d | tail -n +2 | xargs -n1 pipenv run mypy

ci: lint types
	pipenv run ruff format --check 2020 2021 2024

.PHONY: ci format lint types
