.PHONY: install lint format test test-cov clean

install:
	pip install -e ".[dev,test]"
	pre-commit install || true

lint:
	ruff check graphenda_shared/ tests/
	black --check graphenda_shared/ tests/
	isort --check-only graphenda_shared/ tests/
	mypy graphenda_shared/

format:
	black graphenda_shared/ tests/
	isort graphenda_shared/ tests/
	ruff check --fix graphenda_shared/ tests/

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=graphenda_shared --cov-report=term-missing --cov-report=html

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov build dist *.egg-info
