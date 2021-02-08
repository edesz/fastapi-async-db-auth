#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Verification of handling valid requests."""


import json
import logging
import os
from urllib.parse import urljoin

import pandas as pd
import requests

import api_dummy_data_loader as adl

pd.set_option("display.max_columns", 5000)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    ENV_PORT = int(os.environ.get("PORT", 8050))
    # # inside container
    # SERVICE_NAME = os.environ.get("SERVICE_NAME", "api-db")
    HOST_URL = os.getenv("HOST")
    # not inside container
    HOST_PORT = f"http://{HOST_URL}:{ENV_PORT}"
    # # inside container
    # HOST_PORT = f"http://{SERVICE_NAME}:{ENV_PORT}"

    PROJ_ROOT_DIR = os.path.abspath(os.getcwd())
    dummy_data_filepath = os.path.join(PROJ_ROOT_DIR, "dummy_url_inputs.json")
    _, multi_obs_list = adl.get_dummy_url_data(dummy_data_filepath)

    # Create user and retrieve headers with JWT for using with authenticated
    # routes
    API_USER_NAME = os.getenv("API_NEW_USER_NAME")
    API_USER_PASSWORD = os.getenv("API_NEW_USER_PASSWORD")
    headers = adl.create_user(API_USER_NAME, API_USER_PASSWORD, HOST_PORT)

    # Add predictions to predictions table
    url = urljoin(f"{HOST_PORT}/api/v1/topics/", "predict").lower()
    r = requests.post(
        url,
        data=json.dumps(multi_obs_list),
        headers=headers,
    )
    assert r.status_code == 200
    r_text = json.loads(r.text)
    returned_keys = ["msg", "duplicate_urls_ignored", "current_user"]
    # assert list(r_text) == returned_keys
    assert list(r_text.keys()) == returned_keys
    assert r_text["current_user"] == API_USER_NAME

    # Read Predictions from predictions table
    url = urljoin(f"{HOST_PORT}/api/v1/topics/", "read_predictions").lower()
    r = requests.get(url, headers=headers)
    r_text = json.loads(r.text)
    assert r.status_code == 200
    assert len(r_text["msg"]) >= len(multi_obs_list)
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"][0].keys()) == ["id", "url", "text", "user_id"]
    assert r_text["current_user"] == API_USER_NAME

    # Read single prediction from predictions table
    url = urljoin(
        f"{HOST_PORT}/api/v1/topics/",
        f"read_prediction?url={multi_obs_list[0]['url']}",
    ).lower()
    r = requests.get(url, headers=headers)
    r_text = json.loads(r.text)
    assert r.status_code == 200
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"].keys()) == ["id", "url", "text", "user_id"]
    assert r_text["current_user"] == API_USER_NAME

    # Verify response of authenticated /auths/users/me GET endpoint
    url = urljoin(f"{HOST_PORT}/api/v1/auths/users/", "me").lower()
    r = requests.get(url, headers=headers)
    assert r.status_code == 200
    assert list(json.loads(r.text)) == ["username", "password_hash"]

    # Verify response of authenticated /auths/user/{user_id} GET endpoint
    # - assumes a single user, not named tom, exists in the users table
    user_id = 2
    url = urljoin(f"{HOST_PORT}/api/v1/auths/user/", str(user_id)).lower()
    r = requests.get(url, headers=headers)
    assert r.status_code == 200
    r_text = json.loads(r.text)
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"]) == ["id", "username", "password_hash"]
    assert r_text["msg"]["username"] == API_USER_NAME
    assert r_text["current_user"] == API_USER_NAME

    # Verify response of authenticated /users GET endpoint
    url = urljoin(f"{HOST_PORT}/api/v1/auths/", "users").lower()
    r = requests.get(url, headers=headers)
    r_text = json.loads(r.text)
    assert r.status_code == 200
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"][0].keys()) == ["id", "username", "password_hash"]
    assert len(r_text["msg"]) == user_id
    assert r_text["current_user"] == API_USER_NAME
