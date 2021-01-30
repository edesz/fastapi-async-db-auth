#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlalchemy
from sqlalchemy_utils import URLType

from app.db import database, get_db, metadata

predictions = sqlalchemy.Table(
    "predictions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("url", URLType),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("added_by_user", sqlalchemy.String),
)

get_db()


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
        # print(query)
        last_prediction_id = await database.execute_many(query, values=notes)
        return last_prediction_id
