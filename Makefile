.DEFAULT_GOAL := api
.EXPORT_ALL_VARIABLES:
HOST=0.0.0.0
API_PORT=8050
HOSTNAME=localhost
POSTGRES_PORT=5432
POSTGRES_DB=test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

## Run API
api:
	tox -e api
.PHONY: api

## Create Database
create-db:
	tox -e manage-db -- 'CREATE'
.PHONY: create-db

## Run alembic init
alembic-init:
	./run.sh "alembicinit"
.PHONY: alembic-init

## Run alembic autogenerate
alembic-auto:
	./run.sh "alembicauto"
.PHONY: alembic-auto

## Run alembic migration
alembic-migrate:
	./run.sh "alembicmigrate"
.PHONY: alembic-migrate

## Verify
verify:
	tox -e verify
.PHONY: verify

## Delete Database
delete-db:
	tox -e manage-db -- 'DROP'
.PHONY: delete-db

## Start API service
up:
	docker-compose up --detach
.PHONY: up

## Logs
logs:
	./run.sh "logs"
.PHONY: logs

## Stop services
stop:
	docker-compose stop
.PHONY: stop

## Remove all containers
down:
	docker-compose down
.PHONY: down

## Remove built images for services
delete-api-image:
	./run.sh "delete"
.PHONY: delete-api-image

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
.PHONY: list
