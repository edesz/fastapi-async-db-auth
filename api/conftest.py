#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os

import pytest
from passlib.hash import bcrypt
from starlette.testclient import TestClient

from apit import app
from app.db import DBPrediction, DBUser

client = TestClient(app)

API_USER_NAME = os.environ.get("API_USER_NAME")
API_USER_PASSWORD = os.environ.get("API_USER_PASSWORD")


@pytest.fixture(scope="module")
def test_app():
    """Instantiate FastAPI app."""
    client = TestClient(app)
    yield client


@pytest.fixture
def user_auth_headers(test_app, monkeypatch):
    """Return JWT-authentication request headers for authenticated routes.

    Parameters
    ----------
    test_app : fastapi.app
        fastapi app object
    monkeypatch : _pytest.monkeypatch
        fixture to mock single-user existence, authenticate and return header
    """
    # Mock existence of single user in users table
    @classmethod
    async def mock_get_one_by_username(cls, username):
        hashed_pwd = bcrypt.hash(API_USER_PASSWORD)
        d = {"id": 1, "username": API_USER_NAME, "password_hash": hashed_pwd}
        return d

    monkeypatch.setattr(DBUser, "get_one_by_username", mock_get_one_by_username)

    # Authenticate user with JWT, and retrieve generated JWT for use in
    # headers with routes that require user authentication
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = test_app.post(
        "/token",
        data={
            "grant_type": "",
            "username": API_USER_NAME,
            "password": API_USER_PASSWORD,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers=headers,
    )
    assert r.status_code == 200
    response_dict = json.loads(r.text)
    assert list(response_dict) == ["access_token", "token_type"]

    # Create header with JWT generated above and return header for use with
    # routes that require user authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {response_dict['access_token']}",
    }
    return headers


@pytest.fixture
def get_duplicate_user_by_username(monkeypatch):
    """Mock user model method to ensure no duplicate user in users table."""

    @classmethod
    async def mock_get_one_by_username(cls, username):
        """
        Return user whose username is already in the users table.

        Attributes
        ----------
        username : str
            name for user

        Returns
        -------
        user : dict
            databases object, None means no matching user in users table
        """
        database_user = None
        return database_user

    @classmethod
    async def mock_create(cls, notes):
        """Add user to users table."""
        pass

    monkeypatch.setattr(DBUser, "get_one_by_username", mock_get_one_by_username)
    monkeypatch.setattr(DBUser, "create", mock_create)


@pytest.fixture
def get_all_users(monkeypatch):
    """Mock existence of multiple users in users table."""

    @classmethod
    async def mock_get_all(cls):
        """Return all users from the users table."""
        hashed_pwd = bcrypt.hash(API_USER_PASSWORD)
        d = [{"id": 1, "username": API_USER_NAME, "password_hash": hashed_pwd}]
        return d

    monkeypatch.setattr(DBUser, "get_all", mock_get_all)


@pytest.fixture
def get_single_user_by_username(monkeypatch):
    """Mock existence of single user in users table."""

    @classmethod
    async def mock_get_one(cls, id):
        """Return single user, by user id, from the users table."""
        hashed_pwd = bcrypt.hash(API_USER_PASSWORD)
        d = {"id": 1, "username": API_USER_NAME, "password_hash": hashed_pwd}
        return d

    monkeypatch.setattr(DBUser, "get_one", mock_get_one)


@pytest.fixture
def multiple_new_predictions(monkeypatch):
    """Mock existence of multiple predictions in predictions table."""
    multiple_new_predictions = [
        {
            "id": 1,
            "url": (
                "https://www.theguardian.com/science/2020/feb/13/not-just-a-"
                "space-potato-nasa-unveils-astonishing-details-of-most-"
                "distant-object-ever-visited-arrokoth"
            ),
            "text": "some text here",
            "user_id": 1,
        }
    ]

    @classmethod
    async def mock_get_all(cls):
        """Return all predictions from the predictions table."""
        d = multiple_new_predictions
        return d

    monkeypatch.setattr(DBPrediction, "get_all", mock_get_all)
    return multiple_new_predictions


@pytest.fixture
def single_new_prediction(monkeypatch):
    """Mock existence of single prediction in predictions table."""
    single_new_prediction = {
        "id": 1,
        "url": (
            "https://www.theguardian.com/science/2020/feb/13/not-just-a"
            "-space-potato-nasa-unveils-astonishing-details-of-most-"
            "distant-object-ever-visited-arrokoth"
        ),
        "text": "some text here",
        "user_id": 1,
    }

    @classmethod
    async def mock_get_one_by_url(cls, url):
        """Return a single prediction, by url, from the predictions table."""
        return single_new_prediction

    monkeypatch.setattr(DBPrediction, "get_one_by_url", mock_get_one_by_url)
    return single_new_prediction


@pytest.fixture
def create_multiple_new_predictions(monkeypatch):
    """
    Mock prediction model method to ensure no duplicate prediction in
    predictions table.
    """

    @classmethod
    async def mockfunc_get_one_by_username(cls, username):
        """Return a user record from the users table."""
        hashed_pwd = bcrypt.hash(API_USER_PASSWORD)
        d = {"id": 1, "username": API_USER_NAME, "password_hash": hashed_pwd}
        return d

    @classmethod
    async def mock_get_one_by_url(cls, url):
        """
        Return None to indicate no pre-existing prediction with specified url
        in the predictions table.
        """
        return None

    @classmethod
    async def mock_create_new_record(cls, notes):
        """
        Do nothing, to allow new prediction to be added to predictions table.
        """
        pass

    monkeypatch.setattr(
        DBUser, "get_one_by_username", mockfunc_get_one_by_username
    )
    monkeypatch.setattr(DBPrediction, "get_one_by_url", mock_get_one_by_url)
    monkeypatch.setattr(DBPrediction, "create", mock_create_new_record)
