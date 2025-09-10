.PHONY: all
 all: clean install deps tests coverage

.PHONY: install
install:
	sudo apt-get update
	sudo apt-get install make build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
	libncursesdev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
	# python3.9 does not come with distutils on Ubuntu 22.04 so we need to symlink it
	# or the tox tests will fail for python 3.9
	sudo ln -sf /usr/lib/python3.10/distutils /usr/lib/python3.9/distutils

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

.PHONY: tests
PYTEST_ARGS ?=
tests:
	poetry run pytest $(pytest_args) ${PYTEST_ARGS}

.PHONY: tox
TOX_ARGS ?=
tox:
	poetry run tox ${TOX_ARGS}

.PHONY: coverage
coverage:
	mkdir -p test-results
	poetry run py.test --junitxml=test-results/junit.xml --cov-report term-missing --cov=./business_rules $(pytest_args)
	poetry run coverage html  # open htmlcov/index.html in a browser

.PHONY: merge-upstream
merge-upstream:
	# Merge the venmo/business-rules upstream master branch to our fork
	# Once this command completes there will likely be conflicts so you will need to fix them and commit the changes.
	git remote add upstream git@github.com:venmo/business-rules.git
	git fetch upstream
	git merge upstream/master
