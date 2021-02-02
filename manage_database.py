#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Manage Postgres databases."""


import argparse
import logging
import os

import psycopg2

if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--db-operation",
        type=str,
        dest="db_operation",
        default="CREATE",
        help="operation to perform on database",
    )
    args = parser.parse_args()

    logger = logging.getLogger(__name__)

    logger.info(f"User-Specified Action = {args.db_operation}")

    HOSTNAME = os.environ.get("HOSTNAME", "localhost")
    PORT = os.environ.get("PORT", 5432)
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "test_db")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

    if args.db_operation == "CREATE":
        logger.info(f"Creating {POSTGRES_DB}")
        sql = f"""{args.db_operation} DATABASE {POSTGRES_DB}"""
    elif args.db_operation == "DROP":
        logger.info(f"Deleting {POSTGRES_DB}")
        sql = f"""{args.db_operation} DATABASE IF EXISTS {POSTGRES_DB}"""
    else:
        logger.info(f"Running SQL `{args.db_operation}`")
        sql = args.db_operation

    # establishing the connection
    conn = psycopg2.connect(
        database="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=HOSTNAME,
        port=PORT,
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Creating a database
    cursor.execute(sql)
    if args.db_operation in ["CREATE", "DROP"]:
        logger.info(
            f"{args.db_operation} {POSTGRES_DB} completed successfully."
        )
        cursor.execute("SELECT datname FROM pg_database")
        databases = [table[0] for table in cursor.fetchall()]

        if args.db_operation == "CREATE":
            try:
                assert POSTGRES_DB in databases
                logger.info(f"{POSTGRES_DB} found in list of databases")
            except AssertionError as _:
                logger.error(f"{POSTGRES_DB} not found in list of databases")
        else:
            try:
                assert POSTGRES_DB not in databases
                logger.info(f"{POSTGRES_DB} not found in list of databases")
            except AssertionError as _:
                logger.error(f"{POSTGRES_DB} found in list of databases")

    # Closing the connection
    conn.close()
