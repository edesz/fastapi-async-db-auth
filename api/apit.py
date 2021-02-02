#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import os
from typing import Dict, List

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise

import app.schemas as sc
from app.db import database2 as databasetwo  # , database
from app.models import DBUser
from app.router import api_router
from auth.utils import authenticate_user, get_password_hash

JWT_SECRET = os.environ.get("JWT_SECRET", "myjwtsecret")
Users = List[sc.DBUser]

app = FastAPI()


@app.on_event("startup")
async def startup():
    # await database.connect()
    await databasetwo.connect()


@app.on_event("shutdown")
async def shutdown():
    # await database.disconnect()
    await databasetwo.disconnect()


app.include_router(api_router, prefix="/api/v1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_obj = await authenticate_user(form_data.username, form_data.password)

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {"access_token": token, "token_type": "bearer"}


@app.post("/create_users", response_model=Dict)
async def create_users(users: Users):
    user_records = []
    for _, user in enumerate(users):
        # print(user, type(user))
        pwd_hash = get_password_hash(user.password_hash)
        user_records.append(
            dict(
                username=user.username,
                password_hash=pwd_hash,
            )
        )
    await DBUser.create(user_records)
    new_usernames = [user["username"] for user in user_records]
    return {
        "msg": f"Created {len(user_records)} users: {', '.join(new_usernames)}"
    }
