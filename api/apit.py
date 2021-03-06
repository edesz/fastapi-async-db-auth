#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
from typing import Dict, List

import jwt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import app.db as db
import app.schemas as sc
from app.router import api_router
from auth.utils import authenticate_user, get_password_hash

JWT_SECRET = os.environ.get("JWT_SECRET")
Users = List[sc.DBUser]

db.get_db()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")


@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


app.include_router(api_router, prefix="/api/v1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


@app.get("/")
async def home(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("base.html", context=context)


@app.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Generate JWT, use to authenticate user's password and return token."""
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
    """Add user(s) to users table."""
    # Check if username is already entered in users table
    user_records = []
    errors = []
    for _, user in enumerate(users):
        db_user = await db.DBUser.get_one_by_username(user.username)
        if db_user:
            errors.append(user.username)
        else:
            pwd_hash = get_password_hash(user.password_hash)
            user_records.append(
                dict(
                    username=user.username,
                    password_hash=pwd_hash,
                )
            )
    try:
        assert not errors
    except AssertionError:
        duplicate_username_err = (
            f"Usernames [{','.join(errors)}] not available. "
            "Please change and re-register."
        )
        raise HTTPException(status_code=409, detail=duplicate_username_err)

    # Add user(s) to users table
    await db.DBUser.create(user_records)
    new_usernames = [user["username"] for user in user_records]
    return {
        "msg": f"Created {len(user_records)} users: {', '.join(new_usernames)}"
    }
