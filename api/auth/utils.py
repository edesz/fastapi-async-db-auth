#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(user, unhashed_password_hash):
    return user.verify_password(unhashed_password_hash)


def get_password_hash(unhashed_password_hash):
    return bcrypt.hash(unhashed_password_hash)


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not verify_password(user, password):
        return False
    return user
