#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from pydantic import BaseModel, HttpUrl, constr, validator


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


class DBPredictionRecord(BaseModel):
    """Parse & validate records used to populate database."""

    id: int
    url: HttpUrl
    text: str
    added_by_user: str


class PredictionRecord(BaseModel):
    """Parse & validate predictions to respond to API request."""

    url: HttpUrl
    text: str
    added_by_user: str
