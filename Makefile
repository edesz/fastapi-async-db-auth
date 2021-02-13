#################################################################################
# GLOBALS                                                                       #
#################################################################################

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Start containerized database
start-container-db:
	@echo "+ $@"
	@docker-compose up -d --build db
	@sleep 5
.PHONY: start-container-db

## Run containerized API
container-api:
	@echo "+ $@"
	@docker-compose up -d --build web
	@sleep 5
	@./run.sh "apilogs"
.PHONY: container-api

## Run containerized API verification
container-api-verify:
	@echo "+ $@"
	@docker-compose up -d --build verify
	@sleep 5
	@./run.sh "verifylogs"
.PHONY: container-api-verify

## Start containerized database and containerized API
.PHONY: start-containers
start-containers: start-container-db alembic-migrate container-api

## Start containerized database, containerized API and perform containerized verification
.PHONY: start-containers-verify
start-containers-verify: start-containers container-api-verify

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

## Stop containers
stop-containers:
	@echo "+ $@"
	@docker-compose down
	@./run.sh "delete"
	@docker images
.PHONY: stop-containers

## Delete database container volume
delete-db-container-volume:
	@echo "+ $@"
	@sudo chown -R $(USER):$(USER) $(PWD)/db_data
	@rm -rf db_data
	@docker volume prune -f
	@docker volume ls
.PHONY: delete-db-container-volume

## Stop containerized database and API, Delete database container volume and Remove Python artifacts
.PHONY: stop-containers-clean
stop-containers-clean: stop-containers delete-db-container-volume clean-py

## Run API
api:
	@echo "+ $@"
	@tox -e api
.PHONY: api

## Run tests using containerized database
run-tests:
	@echo "+ $@"
	@tox -e test
.PHONY: run-tests

## Show test summary reports
test-summary:
	@echo "+ $@"
	@tox -e testsummary
.PHONY: test-summary

## Stop containerized database
stop-container-db:
	@echo "+ $@"
	@docker-compose down --rmi all
	@docker images
	@docker volume ls
.PHONY: stop-container-db

## Run tests using containerized database and show summary reports
.PHONY: tests
tests: start-container-db run-tests stop-container-db test-summary

## Remove Python artifacts
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

## Remove Python artifacts and Remove alembic configuration
.PHONY: clean-api
clean-api: clean-py clean-alembic

## Remove Python artifacts during API verification
clean-py-verify:
	@echo "+ $@"
	@find ./api_verify -type f -name "*.py[co]" -delete
	@find ./api_verify -type d -name "__pycache__" -delete
.PHONY: clean-py-verify

## Create Heroku app
heroku-create:
	@echo "+ $@"
	@heroku create $(HD_APP_NAME)
.PHONY: heroku-create

## Add a remote to local repository of existing app
heroku-add-remote:
	@echo "+ $@"
	@heroku git:remote -a $(HD_APP_NAME)
.PHONY: heroku-add-remote

## Add PostgreSQL add-on to Heroku app
heroku-create-postgres-add-on:
	@echo "+ $@"
	@heroku addons:create heroku-postgresql:hobby-dev --app $(HD_APP_NAME)
.PHONY: heroku-create-postgres-add-on

## Set Heroku ENV vars
heroku-set-env-vars:
	@echo "+ $@"
	@heroku config:set JWT_SECRET=$(JWT_SECRET) --app $(HD_APP_NAME)
	@heroku config:set HOST=$(HOST) --app $(HD_APP_NAME)
.PHONY: heroku-set-env-vars

## Heroku stream logs
heroku-logs:
	@echo "+ $@"
	@heroku logs --tail
.PHONY: heroku-logs

## Deploy app from sub-directory to Heroku
heroku-deploy-sub-dir:
	@echo "+ $@"
	@git subtree push --prefix api heroku main
.PHONY: heroku-deploy-sub-dir

## (Heroku Docker) Set app to Heroku's container stack
heroku-stack-set-container:
	@echo "+ $@"
	@heroku stack:set container
.PHONY: heroku-stack-set-container

## (Heroku Docker) Git push to deploy containerized app from Heroku CLI
heroku-git-push:
	@echo "+ $@"
	@git push heroku main
.PHONY: heroku-git-push

## Heroku baseline setup for containerized and non-containerized apps
.PHONY: heroku-setup
heroku-setup: heroku-create heroku-add-remote heroku-create-postgres-add-on heroku-set-env-vars

## Heroku workflow to deploy app
.PHONY: heroku-run
heroku-run: heroku-setup heroku-deploy-sub-dir heroku-logs

## (Heroku Docker) Heroku workflow to deploy containerized app
.PHONY: heroku-docker-run
heroku-docker-run: heroku-setup heroku-stack-set-container heroku-git-push heroku-logs

## Detach Heroku add-on
heroku-detach-postgres-add-on:
	@echo "+ $@"
	@heroku addons:destroy heroku-postgresql:hobby-dev --confirm $(HD_APP_NAME)
.PHONY: heroku-detach-postgres-add-on

## Delete Heroku app
heroku-delete:
	@echo "+ $@"
	@heroku apps:destroy --app $(HD_APP_NAME) --confirm $(HD_APP_NAME)
.PHONY: heroku-delete

## Heroku workflow to delete app
.PHONY: heroku-stop
heroku-stop: heroku-detach-postgres-add-on heroku-delete

# list:
# 	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
# .PHONY: list

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
