.DEFAULT_GOAL := api
.EXPORT_ALL_VARIABLES:
HOST=0.0.0.0
API_PORT=8050

## Run API
api:
	tox -e api
.PHONY: api

## Verify
verify:
	tox -e verify
.PHONY: verify

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
