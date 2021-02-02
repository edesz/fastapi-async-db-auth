#!/usr/bin/python3
# -*- coding: utf-8 -*-


import asyncio
import os
from typing import Dict, List, Union

import app.schemas as sc
import jwt
import pandas as pd
from app.models import DBPrediction, DBUser
from app.schemas import DBUser as DBUser_Pydantic
from auth.utils import (
    get_password_hash,
    oauth2_scheme,
    user_pydantic_from_sqlalchemy,
    get_current_user,
)
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

DBUserRecord = sc.DBUserRecord
DBUserRecords = List[DBUserRecord]
Users = List[sc.DBUser]
DBPredictionRecord = sc.DBPredictionRecord
DBPredictionRecords = List[DBPredictionRecord]
PredictionRecords = List[sc.PredictionRecord]
NewsArticles = List[sc.NewsArticle]

# JWT_SECRET = os.environ.get("JWT_SECRET", "myjwtsecret")


# DBPredictionRecord = sc.DBPredictionRecord
# DBPredictionRecords = List[DBPredictionRecord]
# PredictionRecords = List[sc.PredictionRecord]
# NewsArticles = List[sc.NewsArticle]


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
#         db_user = await DBUser.get_one_by_username(payload.get("username"))
#         db_user_pydantic = user_pydantic_from_sqlalchemy(db_user)
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#         )

#     return db_user_pydantic


# @router.get("/users/me", response_model=sc.DBUser)
# async def get_my_user(user: sc.DBUser = Depends(get_current_user)):
#     return user


# @router.get(
#     "/users",
#     response_model=Dict[str, Union[DBUserRecords, str]],
# )
# async def get_users(user: sc.DBUser = Depends(get_current_user)):
#     db_users = await DBUser.get_all()
#     return {
#         "msg": [DBUserRecord(**db_user).dict() for db_user in db_users],
#         "current_user": user.username,
#     }


# @router.get(
#     "/user/{user_id}",
#     response_model=Dict[str, Union[DBUserRecord, str]],
# )
# async def get_user(user_id: int, user: sc.DBUser = Depends(get_current_user)):
#     db_user = await DBUser.get_one(user_id)
#     if db_user:
#         return {
#             "msg": DBUserRecord(**db_user).dict(),
#             "current_user": user.username,
#         }
#     else:
#         raise HTTPException(
#             status_code=418, detail=f"Received Invalid user ID: {user_id}."
#         )


@router.post(
    "/predict", response_model=Dict[str, Union[PredictionRecords, str]]
)
async def predict_species(
    newsarticles: NewsArticles, user: sc.DBUser = Depends(get_current_user)
):
    df_method1 = pd.concat(
        [newsarticle.to_df() for newsarticle in newsarticles]
    ).reset_index(drop=True)
    df_method2 = pd.DataFrame.from_records(
        [dict(newsarticle) for newsarticle in newsarticles]
    )
    assert df_method1.equals(df_method2)
    db_user = await DBUser.get_one_by_username(username=user.username)
    db_user_id = db_user.get("id")
    df_predictions = df_method1.assign(
        user_id=[db_user_id] * len(df_method1)
    ).to_dict("records")
    await DBPrediction.create(df_predictions)
    return {
        "msg": df_predictions,
        "current_user": user.username,
    }


@router.get(
    "/read_predictions",
    response_model=Dict[str, Union[DBPredictionRecords, str]],
)
async def read_predictions(user: sc.DBUser = Depends(get_current_user)):
    notes = await DBPrediction.get_all()
    return {
        "msg": [DBPredictionRecord(**note).dict() for note in notes],
        "current_user": user.username,
    }
