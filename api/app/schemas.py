#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from pydantic import BaseModel, Field, HttpUrl, SecretStr, constr, validator


class NewsArticle(BaseModel):
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
    username: str
    password_hash: constr(strip_whitespace=True, min_length=5)

    class Config:
        use_enum_values = True


class DBUserRecord(BaseModel):
    id: int
    username: str
    password_hash: constr(strip_whitespace=True, min_length=5)

    class Config:
        use_enum_values = True


class DBPredictionRecord(BaseModel):
    """Parse & validate records used to populate database."""

    id: int
    url: HttpUrl
    text: str
    user_id: int


class PredictionRecord(BaseModel):
    """Parse & validate predictions to respond to API request."""

    url: HttpUrl
    text: str
    user_id: int


class NewsArticleUrl(BaseModel):
    url: HttpUrl

    @validator("url")
    def validate_url(cls, v):
        errors = []
        if "theguardian.com" not in v:
            errors.append("URL not from theguardian.com")
        if "https" not in v:
            errors.append("URL not HTTPs")
        assert not errors, f"{','.join(errors)}"
        return v

    class Config:
        use_enum_values = True
