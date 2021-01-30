#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
from typing import Dict, List, Union

import app.schemas as sc
import jwt
import pandas as pd
from app.models import DBPrediction
from auth.utils import oauth2_scheme
from fastapi import APIRouter, Depends, HTTPException, status
from models import User, User_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter()

JWT_SECRET = os.environ.get("JWT_SECRET", "myjwtsecret")


DBPredictionRecord = sc.DBPredictionRecord
DBPredictionRecords = List[DBPredictionRecord]
PredictionRecords = List[sc.PredictionRecord]
NewsArticles = List[sc.NewsArticle]


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return await User_Pydantic.from_tortoise_orm(user)


@router.get("/users/me", response_model=User_Pydantic)
async def get_my_user(user: User_Pydantic = Depends(get_current_user)):
    return user


@router.get(
    "/users",
    response_model=Dict[str, Union[List[User_Pydantic], str]],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_users(user: User_Pydantic = Depends(get_current_user)):
    pydantic_user_objs = await User_Pydantic.from_queryset(User.all())
    return {
        "msg": pydantic_user_objs,
        "current_user": user.username,
    }


@router.get(
    "/user/{user_id}",
    response_model=Dict[str, Union[Dict[str, str], str]],
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_user(
    user_id: int, user: User_Pydantic = Depends(get_current_user)
):
    pydantic_user_obj = await User_Pydantic.from_queryset_single(
        User.get(id=user_id)
    )
    return {
        "msg": {
            "id": user_id,
            "username": pydantic_user_obj.username,
        },
        "current_user": user.username,
    }


@router.post("/predict", response_model=Dict[str, PredictionRecords])
async def predict_species(
    newsarticles: NewsArticles, user: User_Pydantic = Depends(get_current_user)
):
    df_method1 = pd.concat(
        [newsarticle.to_df() for newsarticle in newsarticles]
    ).reset_index(drop=True)
    df_method2 = pd.DataFrame.from_records(
        [dict(newsarticle) for newsarticle in newsarticles]
    )
    assert df_method1.equals(df_method2)
    df_predictions = df_method1.assign(
        added_by_user=[user.username] * len(df_method1)
    ).to_dict("records")
    await DBPrediction.create(df_predictions)
    return {"msg": df_predictions}


@router.get(
    "/read_predictions",
    response_model=Dict[str, Union[DBPredictionRecords, str]],
)
async def read_predictions(user: User_Pydantic = Depends(get_current_user)):
    notes = await DBPrediction.get_all()
    return {
        "msg": [DBPredictionRecord(**note).dict() for note in notes],
        "current_user": user.username,
    }
