MAIN = a_maze_ing.py
CONFIG = config.txt
EXCLUDE_DIRS = .venv,__pycache__,.git,.mypy_cache,venv

.PHONY: install run debug clean lint lint-strict build

install:
	poetry install


run:
	poetry run python3 $(MAIN) $(CONFIG)


debug:
	poetry run python3 -m pdb $(MAIN) $(CONFIG)


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -rf {} +
	find . -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +


lint:
	poetry run flake8 . --exclude $(EXCLUDE_DIRS)
	poetry run mypy . --exclude $(EXCLUDE_DIRS) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


lint-strict:
	poetry run flake8 . --exclude $(EXCLUDE_DIRS) 
	poetry run mypy . --exclude $(EXCLUDE_DIRS) --strict


build:
	poetry build
	mv dist/*.whl .
	mv dist/*.gz .
	rm -rf dist build
