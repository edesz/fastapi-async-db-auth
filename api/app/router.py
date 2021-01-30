#!/usr/bin/python3
# -*- coding: utf-8 -*-


from fastapi import APIRouter

from app.topics import routes as topics

api_router = APIRouter()
api_router.include_router(topics.router, tags=["topics"], prefix="/topics")
