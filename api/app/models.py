#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlalchemy
from sqlalchemy_utils import PasswordType, URLType

metadata = sqlalchemy.MetaData()

predictions = sqlalchemy.Table(
    "predictions",
    metadata,
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
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password_hash", sqlalchemy.String),
)
