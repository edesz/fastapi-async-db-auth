#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from os import curdir
from typing import Dict, List, Union

import app.schemas as sc
from app.db import DBUser
from auth.utils import check_for_admin_user, get_current_user
from fastapi import APIRouter, Depends, HTTPException

DBUserRecord = sc.DBUserRecord
DBUserRecords = List[DBUserRecord]

router = APIRouter()


@router.get("/users/me", response_model=sc.DBUser)
async def get_my_user(user: sc.DBUser = Depends(get_current_user)):
    """Read current user from users table."""
    return user


@router.get(
    "/users",
    response_model=Dict[str, Union[DBUserRecords, str]],
)
async def get_users(user: sc.DBUser = Depends(get_current_user)):
    """Read all users from users table."""
    current_user_name = check_for_admin_user(user)
    db_users = await DBUser.get_all()
    return {
        "msg": [DBUserRecord(**db_user).dict() for db_user in db_users],
        "current_user": current_user_name,
    }


@router.get(
    "/user/{user_id}",
    response_model=Dict[str, Union[DBUserRecord, str]],
)
async def get_user(user_id: int, user: sc.DBUser = Depends(get_current_user)):
    """Read single user, by user id, from users table."""
    current_user_name = user.username
    db_user = await DBUser.get_one(user_id)
    if not db_user:
        raise HTTPException(
            status_code=418, detail=f"Received Invalid user ID: {user_id}."
        )
    current_user_obj = await DBUser.get_one_by_username(current_user_name)
    # print(current_user_obj.get("id"), db_user.get("id"))
    if not current_user_obj.get("id") == db_user.get("id"):
        raise HTTPException(
            status_code=401,
            detail=f"{current_user_name} is not the admin. No access.",
        )
    return {
        "msg": DBUserRecord(**db_user).dict(),
        "current_user": current_user_name,
    }
