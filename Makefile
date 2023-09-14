GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# help
TARGET_MAX_CHAR_NUM=20
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

# build python package
build:
	python setup.py sdist

# deploy package to pypi
deploy:
	twine upload dist/*

# run all tests with coverage
run-tests:
	pytest --cov=fastapi_versionizer --cov-fail-under=85 --no-cov-on-fail tests/

# type check python
type-check:
	mypy .

# lint
lint:
	flake8 fastapi_versionizer tests examples

# install dev dependencies
install-dev:
	pip install -r requirements.dev.txt

# enable commit hook
install-commit-hooks:
	pre-commit install --hook-type commit-msg
