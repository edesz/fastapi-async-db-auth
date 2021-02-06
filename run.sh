#!/bin/bash


API_SERVICE_NAME=api-db
API_VERIFY_SERVICE_NAME=api-verify
DIR_NAME=fastapi-minimal-ml
ACTION=${1:-logs}

if [[ "$ACTION" == 'logs' ]]; then
    sleep 5
    docker logs $(docker ps --no-trunc -aqf name="${DIR_NAME}_${API_VERIFY_SERVICE_NAME}")
else
    docker rmi -f "${DIR_NAME}_${API_SERVICE_NAME}"
    docker rmi -f "${DIR_NAME}_${API_VERIFY_SERVICE_NAME}"
    docker rmi $(docker images 'python' -a -q)
    docker rmi $(docker images 'tiangolo/uvicorn-gunicorn-fastapi' -a -q)
fi
