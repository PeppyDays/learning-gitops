include .env
export

format:
	poetry run python -m isort .
	poetry run python -m black .

test:
	poetry run python -m pytest

run:
	poetry install
	poetry run python src/cart/main.py
