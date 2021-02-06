#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from pydantic import BaseModel, HttpUrl, constr, validator


class NewsArticle(BaseModel):
    """Pydantic model to parse & validate news article input from user."""

    url: HttpUrl
    text: constr(min_length=20)

    @validator("url")
    def validate_url(cls, v):
        errors = []
        if "theguardian.com" not in v:
            errors.append("URL not from theguardian.com")
        if "https" not in v:
            errors.append("URL not HTTPs")
        assert not errors, f"{','.join(errors)}"
        return v

    def to_df(self):
        """Convert to pandas dataframe with 1 or more rows."""
        return pd.DataFrame.from_dict(dict(self), orient="index").T

    class Config:
        use_enum_values = True


class DBUser(BaseModel):
    """Pydantic model to parse & validate user."""

    username: str
    password_hash: constr(strip_whitespace=True, min_length=5)

    class Config:
        use_enum_values = True


class DBUserRecord(BaseModel):
    """Pydantic model to parse & validate user record from database."""

    id: int
    username: str
    password_hash: constr(strip_whitespace=True, min_length=5)

    class Config:
        use_enum_values = True


class DBPredictionRecord(BaseModel):
    """Pydantic model to parse & validate prediction from database."""

    id: int
    url: HttpUrl
    text: str
    user_id: int


class PredictionRecord(BaseModel):
    """Pydantic model to parse & validate prediction."""

    url: HttpUrl
    text: str
    user_id: int
