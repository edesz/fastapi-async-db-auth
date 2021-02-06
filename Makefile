.DEFAULT_GOAL := api
.EXPORT_ALL_VARIABLES:
HOST=0.0.0.0
API_PORT=8050
HOSTNAME=localhost
POSTGRES_PORT=5434
POSTGRES_DB=test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
API_USER_NAME=anthony
API_USER_PASSWORD=mysecret

## Run API
api:
	@echo "+ $@"
	@docker-compose up -d --build
	@sleep 5
	@tox -e api
.PHONY: api

## Run alembic init
alembic-init:
	# ./run.sh "alembicinit"
	tox -e migrate -- init migrations
.PHONY: alembic-init

## Run alembic autogenerate
alembic-auto:
	# ./run.sh "alembicauto"
	tox -e migrate -- revision --autogenerate -m "create user table"
.PHONY: alembic-auto

## Run alembic migration
alembic-migrate:
	# ./run.sh "alembicmigrate"
	tox -e migrate -- upgrade head
.PHONY: alembic-migrate

## Run tests
run-tests:
	@echo "+ $@"
	@docker-compose up -d --build
	@sleep 5
	@tox -e test
	@docker-compose down -v
	@docker rmi postgres
	@docker images
.PHONY: run-tests

## Show test summary report(s)
test-summary:
	@echo "+ $@"
	@tox -e testsummary
.PHONY: test-summary

## Run tests and reports
.PHONY: tests
tests: run-tests test-summary

## Remove Python file artifacts
clean-tests:
	@echo "+ $@"
	@find ./api -type f -name "*.py[co]" -delete
	@find ./api -type d -name "__pycache__" -delete
	@find "api/tests/test-logs/htmlcov" -type f -delete
	@rm -rf api/tests/test-logs/htmlcov
	@find "api/tests/test-logs/" -type f -name "*report*" -delete
	@rm -rf api/tests/test-logs/coverage.xml api/.coverage
.PHONY: clean-tests

## Verify
verify:
	tox -e verify
.PHONY: verify

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
.PHONY: list
