#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import databases
import sqlalchemy
from app.models import users, predictions, metadata2

# SQLAlchemy specific code, as with any other app
# # DATABASE_URL = "sqlite:///./predictions.db"
# DATABASE2_URL = "sqlite:///./users.db"
# # DATABASE_URL = "postgresql://user:password@postgresserver/db"

HOSTNAME = os.environ.get("HOSTNAME", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_DB = os.environ.get("POSTGRES_DB", "test_db")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
DATABASE2_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOSTNAME}:"
    f"{POSTGRES_PORT}/{POSTGRES_DB}"
)

# database = databases.Database(DATABASE_URL)
database2 = databases.Database(DATABASE2_URL)


# def get_db():
#     engine = sqlalchemy.create_engine(
#         DATABASE_URL, connect_args={"check_same_thread": False}
#     )
#     metadata.create_all(engine)


def get_db2():
    engine2 = sqlalchemy.create_engine(
        DATABASE2_URL,
        # connect_args={"check_same_thread": False}
    )
    metadata2.create_all(engine2)


class DBPrediction:
    @classmethod
    async def get_one(cls, id):
        query = predictions.select().where(predictions.c.id == id)
        single_prediction = await database2.fetch_one(query)
        return single_prediction

    @classmethod
    async def get_all(cls):
        query = predictions.select()
        all_predictions = await database2.fetch_all(query)
        return all_predictions

    @classmethod
    async def create(cls, notes):
        query = predictions.insert()
        # print(query)
        last_prediction_id = await database2.execute_many(query, values=notes)
        return last_prediction_id

    @classmethod
    async def get_one_by_url(cls, url):
        query = predictions.select().where(predictions.c.url == url)
        single_prediction = await database2.fetch_one(query)
        return single_prediction


class DBUser:
    @classmethod
    async def get_one(cls, id):
        query = users.select().where(users.c.id == id)
        single_user = await database2.fetch_one(query)
        return single_user

    @classmethod
    async def get_all(cls):
        query = users.select()
        all_users = await database2.fetch_all(query)
        return all_users

    @classmethod
    async def create(cls, notes):
        query = users.insert()
        # print(query)
        last_user_id = await database2.execute_many(query, values=notes)
        return last_user_id

    @classmethod
    async def get_one_by_username(cls, username):
        query = users.select().where(users.c.username == username)
        single_user = await database2.fetch_one(query)
        return single_user
