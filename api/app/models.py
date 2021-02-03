#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# from passlib.hash import bcrypt
import sqlalchemy
from sqlalchemy_utils import PasswordType, URLType, force_auto_coercion

# force_auto_coercion()

# from app.db import (
#     # database,
#     database2 as database_two,
#     # get_db,
#     get_db2,
#     # metadata,
#     metadata2,
# )

# metadata = sqlalchemy.MetaData()
metadata2 = sqlalchemy.MetaData()

predictions = sqlalchemy.Table(
    "predictions",
    metadata2,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("url", URLType),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)
users = sqlalchemy.Table(
    "users",
    metadata2,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password_hash", sqlalchemy.String),
)

# # get_db()
# get_db2()


# class DBPrediction:
#     @classmethod
#     async def get_one(cls, id):
#         query = predictions.select().where(predictions.c.id == id)
#         single_prediction = await database_two.fetch_one(query)
#         return single_prediction

#     @classmethod
#     async def get_all(cls):
#         query = predictions.select()
#         all_predictions = await database_two.fetch_all(query)
#         return all_predictions

#     @classmethod
#     async def create(cls, notes):
#         query = predictions.insert()
#         # print(query)
#         last_prediction_id = await database_two.execute_many(
#             query, values=notes
#         )
#         return last_prediction_id


# class DBUser:
#     @classmethod
#     async def get_one(cls, id):
#         query = users.select().where(users.c.id == id)
#         single_user = await database_two.fetch_one(query)
#         return single_user

#     @classmethod
#     async def get_all(cls):
#         query = users.select()
#         all_users = await database_two.fetch_all(query)
#         return all_users

#     @classmethod
#     async def create(cls, notes):
#         query = users.insert()
#         # print(query)
#         last_user_id = await database_two.execute_many(query, values=notes)
#         return last_user_id

#     @classmethod
#     async def get_one_by_username(cls, username):
#         query = users.select().where(users.c.username == username)
#         single_user = await database_two.fetch_one(query)
#         return single_user
