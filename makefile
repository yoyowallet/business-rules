.PHONY: clean test coverage

clean:
	-find . -type f -name "*.pyc" -delete
	poetry env remove 3.8 || true
	poetry env use 3.8

deps:
	poetry install

test:
	poetry run py.test $(pytest_args)

coverage:
	poetry run py.test --cov-report term-missing --cov=./business_rules $(pytest_args)
