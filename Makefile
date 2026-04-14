MAIN = a_maze_ing.py
CONFIG = config.txt
FLAKE_EXCLUDE = .venv,__pycache__,.git,.mypy_cache,venv
MYPY_EXCLUDE = '(\.venv|__pycache__|\.git|\.mypy_cache|venv)'


.PHONY: install run debug clean lint lint-strict build

run:
	poetry run python3 $(MAIN) $(CONFIG) </dev/tty


install:
	poetry install


debug:
	poetry run python3 -m pdb $(MAIN) $(CONFIG)


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.egg-info" -exec rm -rf {} +


lint:
	poetry run flake8 . --exclude $(FLAKE_EXCLUDE)
	poetry run mypy . --exclude $(MYPY_EXCLUDE) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


lint-strict:
	poetry run flake8 . --exclude $(FLAKE_EXCLUDE) 
	poetry run mypy . --exclude $(MYPY_EXCLUDE) --strict


build:
	poetry build
	mv dist/*.whl . 2>/dev/null || true
	mv dist/*.gz . 2>/dev/null || true
	rm -rf dist build
