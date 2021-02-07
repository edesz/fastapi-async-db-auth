#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from pydantic import BaseModel, HttpUrl, constr, validator


class NewsArticle(BaseModel):
    """Pydantic model to parse & validate news article input from user.

    Parameters
    ----------
    url : HttpUrl
        valid url of news article
    text : constr
        news article text

    Methods
    -------
    validate_url(v)
        Verifies URL
    to_df()
        Gets single-row pandas DataFrame from dictionary
    """

    url: HttpUrl
    text: constr(min_length=20)

    @validator("url")
    def validate_url(cls, v):
        """
        Validates news article URL.

        Parameters
        ----------
        v : HttpUrl
            URL of new article
        """
        errors = []
        if "theguardian.com" not in v:
            errors.append("URL not from theguardian.com")
        if "https" not in v:
            errors.append("URL not HTTPs")
        assert not errors, f"{','.join(errors)}"
        return v

    def to_df(self):
        """
        Convert dict to pandas dataframe with single row.

        Parameters
        ----------
        None
        """
        return pd.DataFrame.from_dict(dict(self), orient="index").T

    class Config:
        """
        Check that valid Enum instances are used.

        Parameters
        ----------
        None
        """

        use_enum_values = True


class DBUser(BaseModel):
    """
    Pydantic model to parse & validate user.

    Parameters
    ----------
    username : str
        name for user
    password_hash : constr
        password for user
    """

    username: str
    password_hash: constr(strip_whitespace=True, min_length=5)

    class Config:
        """
        Check that valid Enum instances are used.

        Parameters
        ----------
        None
        """

        use_enum_values = True


class DBUserRecord(BaseModel):
    """
    Pydantic model to parse & validate user record from database.

    Parameters
    ----------
    id : int
        user id
    username : str
        name for user
    text : constr
        password for user
    """

    id: int
    username: str
    password_hash: constr(strip_whitespace=True, min_length=5)

    class Config:
        """
        Check that valid Enum instances are used.

        Parameters
        ----------
        None
        """

        use_enum_values = True


class DBPredictionRecord(BaseModel):
    """
    Pydantic model to parse & validate prediction from database.

    Parameters
    ----------
    id : int
        user id
    url : HttpUrl
        valid url of news article
    text : constr
        news article text
    user_id : int
        id of user who entered record (prediction) into predictions table
    """

    id: int
    url: HttpUrl
    text: str
    user_id: int


class PredictionRecord(BaseModel):
    """
    Pydantic model to parse & validate prediction.

    Parameters
    ----------
    url : HttpUrl
        valid url of news article
    text : constr
        news article text
    user_id : int
        id of user who entered record (prediction) into predictions table
    """

    url: HttpUrl
    text: str
    user_id: int
