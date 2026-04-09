poetry run flake8 $1
poetry run mypy $1 --strict --ignore-missing-imports --warn-unused-ignores