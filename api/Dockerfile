FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ARG HOST_ARG=0.0.0.0
ARG API_PORT_ARG=8050
ARG HOSTNAME_ARG=db
ARG POSTGRES_PORT_ARG=5432
ARG POSTGRES_DB_ARG=test_db
ARG POSTGRES_USER_ARG=postgres
ARG POSTGRES_PASSWORD_ARG=postgres
ARG JWT_SECRET_ARG=myjwtsecret
ARG APP_MODULE_ARG=main:app
ARG WORKER_CLASS_ARG=gunicorn.workers.ggevent.GeventWorker
ARG PY_VERSION=3.8

WORKDIR /api

COPY . /api

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && find /usr/local/lib/python$PY_VERSION -name '*.c' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '*.pxd' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '*.pyd' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '__pycache__' | xargs rm -r

ENV HOST=$HOST_ARG \
    API_PORT=$API_PORT_ARG \
    HOSTNAME=$HOSTNAME_ARG \
    POSTGRES_PORT=$POSTGRES_PORT_ARG \
    POSTGRES_DB=$POSTGRES_DB_ARG \
    POSTGRES_USER=$POSTGRES_USER_ARG \
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD_ARG \
    JWT_SECRET=$JWT_SECRET_ARG \
    APP_MODULE=$APP_MODULE_ARG \
    WORKER_CLASS=$WORKER_CLASS_ARG

EXPOSE $API_PORT $POSTGRES_PORT

CMD gunicorn --workers 1 --bind $HOST:$API_PORT --worker-class $WORKER_CLASS $APP_MODULE
