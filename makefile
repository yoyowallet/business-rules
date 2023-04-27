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
	mkdir -p test-results
	poetry run py.test --junitxml=test-results/junit.xml --cov-report term-missing --cov=./business_rules $(pytest_args)
	poetry run coverage html  # open htmlcov/index.html in a browser
