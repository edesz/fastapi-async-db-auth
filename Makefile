.DEFAULT_GOAL := api

## Run API
api:
	@echo "+ $@"
	@docker-compose up -d --build
	@sleep 5
	@tox -e api
.PHONY: api

## Create Database
create-db:
	tox -e manage-db -- 'CREATE'
.PHONY: create-db

## Run alembic init
alembic-init:
	tox -e alembic -- init migrations
.PHONY: alembic-init

## Run alembic autogenerate
alembic-auto:
	tox -e alembic -- revision --autogenerate -m "create user table"
.PHONY: alembic-auto

## Run alembic migration
alembic-migrate:
	tox -e alembic -- upgrade head
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
	@docker volume ls
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

## Delete Database
delete-db:
	tox -e manage-db -- 'DROP'
.PHONY: delete-db

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
.PHONY: list
