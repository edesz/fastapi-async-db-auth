.DEFAULT_GOAL := api

## Start database
start-db:
	@echo "+ $@"
	@docker-compose up -d --build
	@sleep 5
.PHONY: start-db

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

## Run API
api:
	@echo "+ $@"
	@tox -e api
.PHONY: api

## Stop containerized database
stop-container-db:
	@echo "+ $@"
	@docker-compose down
	@docker rmi postgres
	@docker images
	@docker volume ls
.PHONY: stop-container-db

## Run tests
run-tests:
	@echo "+ $@"
	@tox -e test
.PHONY: run-tests

## Show test summary report(s)
test-summary:
	@echo "+ $@"
	@tox -e testsummary
.PHONY: test-summary

## Run tests and reports
.PHONY: tests
tests: start-db run-tests stop-container-db test-summary

## Remove Python file artifacts during API development
clean-py:
	@echo "+ $@"
	@find ./api -type f -name "*.py[co]" -delete
	@find ./api -type d -name "__pycache__" -delete
.PHONY: clean-py

## Remove test artifacts
clean-test-coverage:
	@echo "+ $@"
	@find "api/tests/test-logs/htmlcov" -type f -delete
	@rm -rf api/tests/test-logs/htmlcov
	@find "api/tests/test-logs/" -type f -name "*report*" -delete
	@rm -rf api/tests/test-logs/coverage.xml api/.coverage
.PHONY: clean-test-coverage

## Clean tests
.PHONY: clean-tests
clean-tests: clean-py clean-test-coverage

## Verify
verify:
	tox -e verify
.PHONY: verify

## Remove alembic configuration
clean-alembic:
	@echo "+ $@"
	@rm -rf api/alembic/migrations
	@rm -f api/alembic/alembic.ini
.PHONY: clean-alembic

## Clean API
.PHONY: clean-api
clean-api: clean-py clean-alembic

## Remove Python file artifacts during API verification
clean-py-verify:
	@echo "+ $@"
	@find ./api_verify -type f -name "*.py[co]" -delete
	@find ./api_verify -type d -name "__pycache__" -delete
.PHONY: clean-py-verify

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
.PHONY: list
