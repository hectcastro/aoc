format:
	uv run ruff format 2020 2021 2024

lint:
	uv run ruff check 2020 2021 2024

types:
	find 2020 -maxdepth 1 -mindepth 1 -type d | xargs -n1 uv run mypy
	find 2021 -maxdepth 1 -mindepth 1 -type d | xargs -n1 uv run mypy
	find 2024 -maxdepth 1 -mindepth 1 -type d | xargs -n1 uv run mypy

ci: lint types
	uv run ruff format --check 2020 2021 2024

.PHONY: ci format lint types
