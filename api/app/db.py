#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import databases
import sqlalchemy

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

# metadata = sqlalchemy.MetaData()
metadata2 = sqlalchemy.MetaData()


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
