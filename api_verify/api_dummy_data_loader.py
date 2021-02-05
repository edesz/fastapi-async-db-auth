#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from urllib.parse import urljoin

import requests


def create_user(username, password_hash, host_port):
    # Create User
    url = urljoin(f"{host_port}/", "create_users").lower()
    headers = {"Content-Type": "application/json"}
    r = requests.post(
        url,
        data=json.dumps(
            [{"username": username, "password_hash": password_hash}]
        ),
        headers=headers,
    )
    # print(r.status_code)
    # print(json.loads(r.text))
    assert r.status_code == 200
    assert list(json.loads(r.text)) == ["msg"]

    # Generate Token
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
    assert list(response_dict) == ["access_token", "token_type"]

    user_auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {response_dict['access_token']}",
    }
    return user_auth_headers


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
