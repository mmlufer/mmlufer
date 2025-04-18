.PHONY: setup test lint format clean run-server

# Variables
PYTHON = python
PYTEST = pytest
COVERAGE = coverage
BLACK = black
ISORT = isort
FLAKE8 = flake8

# Directorios
SERVER_DIR = servers/filesystem
TESTS_DIR = tests

# Comandos
setup:
	pip install -r $(SERVER_DIR)/requirements.txt
	pip install -r $(SERVER_DIR)/requirements-dev.txt

test:
	$(PYTHON) $(TESTS_DIR)/run_tests.py

test-unit:
	$(PYTHON) $(TESTS_DIR)/run_tests.py --unit

test-integration:
	$(PYTHON) $(TESTS_DIR)/run_tests.py --integration

test-coverage:
	$(COVERAGE) run -m pytest $(TESTS_DIR)
	$(COVERAGE) report -m
	$(COVERAGE) html

lint:
	$(FLAKE8) $(SERVER_DIR) $(TESTS_DIR)
	$(BLACK) --check $(SERVER_DIR) $(TESTS_DIR)
	$(ISORT) --check-only $(SERVER_DIR) $(TESTS_DIR)

format:
	$(BLACK) $(SERVER_DIR) $(TESTS_DIR)
	$(ISORT) $(SERVER_DIR) $(TESTS_DIR)

run-server:
	$(PYTHON) $(SERVER_DIR)/server.py

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
