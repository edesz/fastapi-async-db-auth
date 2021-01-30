#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Read contents of SQlite db table with pandas."""


import sqlite3

import pandas as pd

pd.set_option("display.max_columns", 500)


def convert_str_to_list(df):
    df = df.apply(lambda x: x.str.strip("[]").str.split(", "))
    return df


def sql_to_df(sql_query, connection):
    """
    Use Pandas to query SQL database
    """
    lcols = ["term", "term_weight", "entity", "entity_count"]

    # # List all tables
    # c = connection.cursor()
    # q = "SELECT name FROM sqlite_master WHERE type='table';"
    # tables = c.execute(q).fetchall()
    # print(tables)
    # return tables

    # # Read Table into DF - Method 1
    # query = connection.execute(sql_query)
    # cols = [column[0] for column in query.description]
    # df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)

    # Read Table into DF - Method 2
    df = pd.read_sql_query(sql_query, connection, parse_dates=["date"])
    df[lcols] = convert_str_to_list(df[lcols])
    return df


if __name__ == "__main__":
    db_name = "predictions.db"
    db_table_name = "prediction"
    db_query = f"SELECT * FROM {db_table_name}"
    ########################################
    # Begin database check

    cnx = sqlite3.connect(db_name)
    df_preds = sql_to_df(db_query, cnx)
    print(df_preds)
    print(df_preds.dtypes)
    cnx.commit()
    cnx.close()

    # End database check
    ########################################
