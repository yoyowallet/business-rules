.PHONY: clean tests coverage

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf dist

.PHONY: deps-clean
deps-clean:
	if command -v pyenv >/dev/null 2>&1; then pyenv local 3.12; fi
	# Remove the environment and ignore errors if it does not exist.
	poetry env remove 3.12 2>/dev/null || true
	poetry env use 3.12

.PHONY: deps
deps: deps-clean
	poetry install

tests:
	poetry run pytest $(pytest_args)

tox:
	poetry run tox $(tox_args)

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
