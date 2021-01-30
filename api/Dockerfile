FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ARG AZURE_STORAGE_KEY_ARG=abcd
ARG ENDPOINT_SUFFIX_ARG=abcd
ARG AZURE_STORAGE_ACCOUNT_ARG=abcd
ARG APP_MODULE_ARG=main:app
ARG BIND_ARG=0.0.0.0:3080
ARG PORT_ARG=3080
ARG WORKER_CLASS_ARG=gunicorn.workers.ggevent.GeventWorker
ARG PY_VERSION=3.8

WORKDIR /api

COPY . /api
# RUN ls -la /api/*

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && find /usr/local/lib/python$PY_VERSION -name '*.c' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '*.pxd' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '*.pyd' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '__pycache__' | xargs rm -r
# RUN pip freeze

ENV APP_MODULE=$APP_MODULE_ARG \
    PORT=$PORT_ARG \
    BIND=$BIND_ARG \
    WORKER_CLASS=$WORKER_CLASS_ARG

CMD gunicorn --workers 1 --bind $BIND --worker-class $WORKER_CLASS $APP_MODULE
