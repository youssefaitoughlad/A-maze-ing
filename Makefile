
# Add to your Makefile
test:
	pytest tests/ -v --cov=config_parser --cov=mazegen

test-verbose:
	pytest tests/ -v --tb=long --cov-report=html

test-quick:
	pytest tests/ -v --maxfail=1
