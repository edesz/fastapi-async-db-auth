#!/usr/bin/python3
# -*- coding: utf-8 -*-


from fastapi import APIRouter

from app.topics import routes as topics
from app.auths import routes as auths

api_router = APIRouter()
api_router.include_router(topics.router, tags=["topics"], prefix="/topics")
api_router.include_router(auths.router, tags=["auths"], prefix="/auths")
