FROM python:3.8.8-slim-buster

ARG HOST_ARG=0.0.0.0
ARG API_PORT_ARG=3080
ARG API_NEW_USER_NAME_ARG=abc
ARG API_NEW_USER_PASSWORD_ARG=defg
ARG PY_VERSION=3.8

WORKDIR /api_verify

COPY . /api_verify

RUN python -m pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt \
    && find /usr/local/lib/python$PY_VERSION -name '*.c' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '*.pxd' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '*.pyd' -delete \
    && find /usr/local/lib/python$PY_VERSION -name '__pycache__' | xargs rm -r

ENV HOST=$HOST_ARG \
    API_PORT=$API_PORT_ARG \
    API_NEW_USER_NAME=$API_NEW_USER_NAME_ARG \
    API_NEW_USER_PASSWORD=$API_NEW_USER_PASSWORD_ARG

ENTRYPOINT ["python3"]
CMD ["api_handle_invalid_data.py"]
