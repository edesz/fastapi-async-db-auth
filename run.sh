#!/bin/bash


API_SERVICE_NAME=api-db
API_VERIFY_SERVICE_NAME=api-verify
DIR_NAME=fastapi-async-db-auth
ACTION=${1:-logs}

if [[ "$ACTION" == 'alembicinit' ]]; then
    cd api/alembic
    alembic init migrations
elif [[ "$ACTION" == 'alembicauto' ]]; then
    cd api/alembic
    alembic revision --autogenerate -m "create user table"
elif [[ "$ACTION" == 'alembicmigrate' ]]; then
    cd api/alembic
    alembic upgrade head
elif [[ "$ACTION" == 'logs' ]]; then
    sleep 5
    docker logs $(docker ps --no-trunc -aqf name="${DIR_NAME}_${API_VERIFY_SERVICE_NAME}")
else
    docker rmi -f "${DIR_NAME}_${API_SERVICE_NAME}"
    docker rmi -f "${DIR_NAME}_${API_VERIFY_SERVICE_NAME}"
    docker rmi $(docker images 'python' -a -q)
    docker rmi $(docker images 'tiangolo/uvicorn-gunicorn-fastapi' -a -q)
fi
