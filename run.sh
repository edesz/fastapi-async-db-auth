#!/bin/bash


API_SERVICE_NAME=web
API_VERIFY_SERVICE_NAME=verify
DIR_NAME=fastapi-minimal-ml
ACTION=${1:-logs}

if [[ "$ACTION" == 'apilogs' ]]; then
    docker logs $(docker ps --filter ancestor=${DIR_NAME}_${API_SERVICE_NAME} --format "{{.ID}}")
elif [[ "$ACTION" == 'verifylogs' ]]; then
    docker logs $(docker ps -a --filter ancestor=${DIR_NAME}_${API_VERIFY_SERVICE_NAME} --format "{{.ID}}")
else
    docker rmi $(docker image ls --filter 'reference=postgres' --filter 'reference=python' --filter 'reference=fastapi*' --filter 'reference=*/*fastapi' --format "{{.ID}}")
fi
