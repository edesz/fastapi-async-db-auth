#!/usr/bin/python3
# -*- coding: utf-8 -*-


from typing import Dict, List, Union

import app.schemas as sc
import pandas as pd
from app.db import DBPrediction, DBUser
from auth.utils import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl

router = APIRouter()

DBUserRecord = sc.DBUserRecord
DBUserRecords = List[DBUserRecord]
Users = List[sc.DBUser]
DBPredictionRecord = sc.DBPredictionRecord
DBPredictionRecords = List[DBPredictionRecord]
PredictionRecords = List[sc.PredictionRecord]
NewsArticles = List[sc.NewsArticle]


@router.post(
    "/create", response_model=Dict[str, Union[PredictionRecords, str, List]]
)
async def create(
    newsarticles: NewsArticles, user: sc.DBUser = Depends(get_current_user)
):
    """Add prediction(s) to predictions table."""
    # Convert user input of single/multiple news articles to DataFrame
    df_method1 = pd.concat(
        [newsarticle.to_df() for newsarticle in newsarticles]
    ).reset_index(drop=True)
    df_method2 = pd.DataFrame.from_records(
        [dict(newsarticle) for newsarticle in newsarticles]
    )
    assert df_method1.equals(df_method2)

    # Check if prediction is already entered in predictions table
    errors = []
    for _, row in df_method1.iterrows():
        db_prediction = await DBPrediction.get_one_by_url(row["url"])
        if db_prediction:
            errors.append(row["url"])
    try:
        assert not errors
    except AssertionError:
        duplicate_prediction_err = (
            f"Attempting to re-create prediction for: [{','.join(errors)}] "
            "Please remove these and retry. To retrieve previously created "
            "predictions, see /topics/read_predictions?url=..."
        )
        raise HTTPException(status_code=409, detail=duplicate_prediction_err)
    else:
        ### Add topic prediction columns to DataFrame, if required - START ###
        #
        ### Add topic prediction columns to DataFrame, if required - END ###

        # Get current user by username
        db_user = await DBUser.get_one_by_username(username=user.username)
        # Extract user's user_id
        db_user_id = db_user.get("id")
        # Add column with current user's user_id to DataFrame
        df_predictions = df_method1.assign(
            user_id=[db_user_id] * len(df_method1)
        )

        # Convert DataFrame to list of dicts
        df_predictions = df_predictions.to_dict("records")
        # Add list of dicts to predictions table
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
    """Read all predictions from predictions table."""
    notes = await DBPrediction.get_all()
    return {
        "msg": [DBPredictionRecord(**note).dict() for note in notes],
        "current_user": user.username,
    }


@router.get(
    "/read_prediction",
    response_model=Dict[str, Union[DBPredictionRecord, str]],
)
async def read_prediction(
    url: HttpUrl, user: sc.DBUser = Depends(get_current_user)
):
    """Read single prediction, by URL, from predictions table."""
    db_prediction = await DBPrediction.get_one_by_url(url=url)
    if db_prediction:
        return {
            "msg": DBPredictionRecord(**db_prediction).dict(),
            "current_user": user.username,
        }
    else:
        invalid_url_error_msg = f"Received Invalid news article url: {url}."
        raise HTTPException(status_code=418, detail=invalid_url_error_msg)
