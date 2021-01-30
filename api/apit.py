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

import models as m
from app.db import database
from app.router import api_router
from auth.utils import authenticate_user, get_password_hash

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(api_router, prefix="/api/v1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

JWT_SECRET = os.environ.get("JWT_SECRET", "myjwtsecret")


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    user_obj = await m.User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {"access_token": token, "token_type": "bearer"}


@app.post("/users", response_model=Dict)
async def create_user(users: List[m.UserIn_Pydantic]):
    user_objs = []
    for user in users:
        pwd_hash = get_password_hash(user.password_hash)
        user_obj = m.User(
            **dict(username=user.username, password_hash=pwd_hash)
        )
        user_objs.append(user_obj)

    tasks = [asyncio.create_task(user_obj.save()) for user_obj in user_objs]
    _ = await asyncio.gather(*tasks)
    new_usernames = [user.username for user in users]
    return {"msg": f"Created {len(users)} users: {', '.join(new_usernames)}"}


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
