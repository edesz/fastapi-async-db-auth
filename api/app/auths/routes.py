from typing import Dict, List, Union

import app.schemas as sc
from app.db import DBUser
from auth.utils import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

DBUserRecord = sc.DBUserRecord
DBUserRecords = List[DBUserRecord]

router = APIRouter()


@router.get("/users/me", response_model=sc.DBUser)
async def get_my_user(user: sc.DBUser = Depends(get_current_user)):
    return user


@router.get(
    "/users",
    response_model=Dict[str, Union[DBUserRecords, str]],
)
async def get_users(user: sc.DBUser = Depends(get_current_user)):
    db_users = await DBUser.get_all()
    return {
        "msg": [DBUserRecord(**db_user).dict() for db_user in db_users],
        "current_user": user.username,
    }


@router.get(
    "/user/{user_id}",
    response_model=Dict[str, Union[DBUserRecord, str]],
)
async def get_user(user_id: int, user: sc.DBUser = Depends(get_current_user)):
    db_user = await DBUser.get_one(user_id)
    if db_user:
        return {
            "msg": DBUserRecord(**db_user).dict(),
            "current_user": user.username,
        }
    else:
        raise HTTPException(
            status_code=418, detail=f"Received Invalid user ID: {user_id}."
        )
