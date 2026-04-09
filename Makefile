MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint lint-strict

install:
	poetry install


run:
	poetry run python3 $(MAIN) $(CONFIG)


debug:
	poetry run python3 -m pdb $(MAIN) $(CONFIG)


Clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	:find . -name "*.pyc" -exec rm -rf {} +


lint:
	poetry run flake8 .
	poetry run mypy . --war-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


lint-strict:
	poetry run flake8 .
	poetry run mypy . --strict
