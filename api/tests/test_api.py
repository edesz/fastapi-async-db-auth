#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os

import pytest

API_USER_NAME = os.environ.get("API_USER_NAME")


@pytest.mark.happy
def test_root(test_app):
    """Test root."""
    response = test_app.get("/")
    assert isinstance(response.history, list)
    assert len(response.history) == 0
    assert response.status_code == 200
    assert response.url == "http://testserver/"


@pytest.mark.happy
def test_docs_redirect(test_app):
    """Test documentation route."""
    response = test_app.get("/docs")
    assert type(response.history) == list
    assert len(response.history) == 0
    assert response.status_code == 200
    assert response.url == "http://testserver/docs"


@pytest.mark.happy
def test_create_users(test_app, get_duplicate_user_by_username):
    """Test adding new user to users table."""
    # Verify properly formed input returns valid response
    user_records = [{"username": "anthony", "password_hash": "mysecret"}]
    new_usernames = [user["username"] for user in user_records]
    r = test_app.post(
        "/create_users",
        data=json.dumps(user_records),
    )
    assert r.status_code == 200
    assert r.url == "http://testserver/create_users"
    new_user_created_msg = (
        f"Created {len(user_records)} users: {', '.join(new_usernames)}"
    )
    assert json.loads(r.text)["msg"] == new_user_created_msg


@pytest.mark.happy
def test_get_my_user(test_app, user_auth_headers):
    """Test getting currently logged in user's creds from users table."""
    # Verify input with authentication returns current user from users table
    r = test_app.get("/api/v1/auths/users/me", headers=user_auth_headers)
    assert r.status_code == 200
    assert r.url == "http://testserver/api/v1/auths/users/me"
    assert list(json.loads(r.text)) == ["username", "password_hash"]


@pytest.mark.happy
def test_get_users(test_app, user_auth_headers, get_all_users):
    """Test getting all user creds from users table."""
    # Verify input with authentication returns all users in users table
    r = test_app.get("/api/v1/auths/users", headers=user_auth_headers)
    r_text = json.loads(r.text)
    assert r.status_code == 200
    assert r.url == "http://testserver/api/v1/auths/users"
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"][0].keys()) == ["id", "username", "password_hash"]
    assert len(r_text["msg"]) == 1
    assert r_text["current_user"] == API_USER_NAME


@pytest.mark.happy
def test_get_user(test_app, user_auth_headers, get_single_user_by_username):
    """Test getting single user creds from users table, by user id."""
    # Verify input with authentication returns single user from users table
    user_id = 1
    endpoint = f"/api/v1/auths/user/{user_id}"
    r = test_app.get(endpoint, headers=user_auth_headers)
    r_text = json.loads(r.text)
    assert r.status_code == 200
    assert r.url == f"http://testserver{endpoint}"
    r_text = json.loads(r.text)
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"]) == ["id", "username", "password_hash"]
    assert r_text["msg"]["username"] == API_USER_NAME
    assert r_text["current_user"] == API_USER_NAME


@pytest.mark.happy
def test_read_predictions(
    test_app, user_auth_headers, multiple_new_predictions
):
    """Test getting all predictions from predictions table."""
    # Verify input with authentication returns all predictions in predictions
    # table
    endpoint = "/api/v1/topics/read_predictions"
    r = test_app.get(endpoint, headers=user_auth_headers)
    r_text = json.loads(r.text)
    assert r.status_code == 200
    assert r.url == f"http://testserver{endpoint}"
    assert len(r_text["msg"]) >= len(multiple_new_predictions)
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"][0].keys()) == ["id", "url", "text", "user_id"]
    assert r_text["current_user"] == API_USER_NAME


@pytest.mark.happy
def test_read_prediction(test_app, user_auth_headers, single_new_prediction):
    """Test getting single prediction from predictions table."""
    # Verify properly formed url with authentication returns single prediction
    # from predictions table
    endpoint = (
        f"/api/v1/topics/read_prediction?url={single_new_prediction['url']}"
    )
    r = test_app.get(
        endpoint,
        headers=user_auth_headers,
    )
    r_text = json.loads(r.text)
    assert r.status_code == 200
    assert r.url == f"http://testserver{endpoint}"
    assert list(r_text) == ["msg", "current_user"]
    assert list(r_text["msg"].keys()) == ["id", "url", "text", "user_id"]
    assert r_text["current_user"] == API_USER_NAME


@pytest.mark.happy
@pytest.mark.unhappy
def test_create_predictions(
    test_app, user_auth_headers, create_multiple_new_predictions
):
    """Test adding new prediction to predictions table."""
    endpoint = "/api/v1/topics/create"
    new_records = [
        {
            "url": (
                "https://www.theguardian.com/science/2020/feb/13/not-just-a"
                "-space-potato-nasa-unveils-astonishing-details-of-most-"
                "distant-object-ever-visited-arrokoth"
            ),
            "text": (
                "some basic text must be placed in here of the minimum "
                "required length"
            ),
        }
    ]

    # Verify that no header raises error for invalid authentication creds
    r = test_app.post(endpoint, data=json.dumps(new_records))
    assert r.status_code == 401

    # Verify properly formed input with authentication returns valid response
    r = test_app.post(
        endpoint,
        data=json.dumps(new_records),
        headers=user_auth_headers,
    )
    assert r.status_code == 200
    assert r.url == f"http://testserver{endpoint}"
    r_text = json.loads(r.text)
    assert list(r_text.keys()) == ["msg", "current_user"]
    for response, record in zip(r_text["msg"], new_records):
        for key in ["url", "text"]:
            assert response[key] == record[key]
