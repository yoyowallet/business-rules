.PHONY: clean test coverage

clean:
	-find . -type f -name "*.pyc" -delete
	poetry env remove 3.11 || true
	poetry env use 3.11

deps:
	poetry install

test:
	poetry run py.test $(pytest_args)

coverage:
	mkdir -p test-results
	poetry run py.test --junitxml=test-results/junit.xml --cov-report term-missing --cov=./business_rules $(pytest_args)
	poetry run coverage html  # open htmlcov/index.html in a browser

merge-upstream:
	# Merge the venmo/business-rules upstream master branch to our fork
	# Once this command completes there will likely be conflicts so you will need to fix them and commit the changes.
	git remote add upstream git@github.com:venmo/business-rules.git
	git fetch upstream
	git merge upstream/master
