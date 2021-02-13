#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import json
from urllib.parse import urljoin

import requests


def check_admin_user(username, password_hash):
    is_admin = False
    if isinstance(username, list):
        user_creds = [
            [u, password_hash[k]]
            for k, u in enumerate(username)
            if u != "admin"
        ]
        # print(user_creds)
        if not user_creds:
            # Received single-element list with only admin user
            is_admin = True
            username = username[-1]
            password_hash = password_hash[-1]
        else:
            # Received multi-element list, including non-admin users
            username, password_hash = user_creds[-1]
    else:
        if username == "admin":
            is_admin = True
    os.environ["API_NEW_USER_NAME"] = username
    os.environ["API_NEW_USER_PASSWORD"] = password_hash
    return [username, password_hash, is_admin]


def create_user(username, password_hash, host_port):
    # Create User
    url = urljoin(f"{host_port}/", "create_users").lower()
    headers = {"Content-Type": "application/json"}
    if not isinstance(username, list):
        r = requests.post(
            url,
            data=json.dumps(
                [{"username": username, "password_hash": password_hash}]
            ),
            headers=headers,
        )
    else:
        users_dict = [
            {"username": u, "password_hash": p}
            for u, p in zip(username, password_hash)
        ]
        # print(users_dict)
        r = requests.post(url, data=json.dumps(users_dict), headers=headers)
    # print(r.status_code, json.loads(r.text))
    assert r.status_code == 200
    assert list(json.loads(r.text).keys()) == ["msg"]

    # Get credentials for last user created
    username, password_hash, is_admin = check_admin_user(
        username, password_hash
    )
    # print(username, password_hash, is_admin)

    # Generate Token for user
    url = urljoin(f"{host_port}/", "token").lower()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(
        url,
        data={
            "grant_type": "",
            "username": username,
            "password": password_hash,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers=headers,
    )
    # print(r.status_code)
    # print(json.loads(r.text))
    assert r.status_code == 200
    response_dict = json.loads(r.text)
    assert list(response_dict.keys()) == ["access_token", "token_type"]

    user_auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {response_dict['access_token']}",
    }
    return [user_auth_headers, is_admin]


def get_dummy_url_data(dummy_data_filepath):
    with open(dummy_data_filepath) as json_file:
        d_observations_urls_raw = json.load(json_file)
    d_observations_urls = []
    d_observations_urls_all = []
    for d_observations_url_raw in d_observations_urls_raw:
        d_observation_url_formatted = {
            "data": [
                {
                    k: v
                    for k, v in d_observations_url_raw.items()
                    if k not in ["status_code", "msg"]
                }
            ],
            "status_code": d_observations_url_raw["status_code"],
            "msg": d_observations_url_raw["msg"],
        }
        d_observations_urls.append(d_observation_url_formatted)
        d_observation_all_urls_formatted = {
            k: v
            for k, v in d_observations_url_raw.items()
            if k not in ["status_code", "msg"]
        }
        d_observations_urls_all.append(d_observation_all_urls_formatted)
    return [d_observations_urls, d_observations_urls_all]
