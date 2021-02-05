#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

import jwt
from app.db import DBUser
from app.schemas import DBUser as DBUser_Pydantic
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = os.environ.get("JWT_SECRET", "myjwtsecret")


def verify_password(unhashed_password_hash, hashed_password_hash):
    """
    Check if unhashed password generates same hash as hashed version stored in
    users table.
    """
    return bcrypt.verify(unhashed_password_hash, hashed_password_hash)


def get_password_hash(unhashed_password_hash):
    """Hash an unhashed password."""
    return bcrypt.hash(unhashed_password_hash)


def user_pydantic_from_sqlalchemy(db_user):
    """Convert single SQLAlchemy model to Pydantic model."""
    creds_keys = ["username", "password_hash"]
    user_creds = dict(
        zip(
            creds_keys,
            [db_user.get(cred_key) for cred_key in creds_keys],
        )
    )
    db_user_pydantic = DBUser_Pydantic(**user_creds)
    return db_user_pydantic


async def authenticate_user(username: str, password: str):
    """Authenticate user's password against password in users table."""
    user = await DBUser.get_one_by_username(username=username)
    db_user_pydantic = user_pydantic_from_sqlalchemy(user)
    if not username:
        return False, False
    if not verify_password(password, db_user_pydantic.password_hash):
        return False, False
    return db_user_pydantic


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get currently logged in user as Pydantic model."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        db_user = await DBUser.get_one_by_username(payload.get("username"))
        db_user_pydantic = user_pydantic_from_sqlalchemy(db_user)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return db_user_pydantic
