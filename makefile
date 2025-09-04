.PHONY: clean tests coverage

clean:
	if command -v pyenv >/dev/null 2>&1; then pyenv local 3.12; fi
	poetry env remove 3.12 || true
	poetry env use 3.12

deps: clean
	poetry install

tests:
	poetry run pytest $(pytest_args)

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
