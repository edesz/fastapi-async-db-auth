#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

import databases
import sqlalchemy

from app.models import metadata, predictions, users

# SQLAlchemy specific code, as with any other app
HOSTNAME = os.environ.get("HOSTNAME", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_DB = os.environ.get("POSTGRES_DB", "test_db")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
DATABASE2_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOSTNAME}:"
    f"{POSTGRES_PORT}/{POSTGRES_DB}"
)

database = databases.Database(DATABASE2_URL)


def get_db():
    engine = sqlalchemy.create_engine(
        DATABASE2_URL,
        # connect_args={"check_same_thread": False}
    )
    metadata.create_all(engine)


class DBPrediction:
    @classmethod
    async def get_one(cls, id):
        query = predictions.select().where(predictions.c.id == id)
        single_prediction = await database.fetch_one(query)
        return single_prediction

    @classmethod
    async def get_all(cls):
        query = predictions.select()
        all_predictions = await database.fetch_all(query)
        return all_predictions

    @classmethod
    async def create(cls, notes):
        query = predictions.insert()
        last_prediction_id = await database.execute_many(query, values=notes)
        return last_prediction_id

    @classmethod
    async def get_one_by_url(cls, url):
        query = predictions.select().where(predictions.c.url == url)
        single_prediction = await database.fetch_one(query)
        return single_prediction


class DBUser:
    @classmethod
    async def get_one(cls, id):
        query = users.select().where(users.c.id == id)
        single_user = await database.fetch_one(query)
        return single_user

    @classmethod
    async def get_all(cls):
        query = users.select()
        all_users = await database.fetch_all(query)
        return all_users

    @classmethod
    async def create(cls, notes):
        query = users.insert()
        last_user_id = await database.execute_many(query, values=notes)
        return last_user_id

    @classmethod
    async def get_one_by_username(cls, username):
        query = users.select().where(users.c.username == username)
        single_user = await database.fetch_one(query)
        return single_user
