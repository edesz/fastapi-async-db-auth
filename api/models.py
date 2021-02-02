#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# from typing import List

# from passlib.hash import bcrypt
# from tortoise import fields
# from tortoise.contrib.pydantic import pydantic_model_creator
# from tortoise.exceptions import ValidationError
# from tortoise.validators import MinLengthValidator
# from tortoise.models import Model
# from tortoise.validators import Validator


# class User(Model):
#     id = fields.IntField(pk=True)
#     username = fields.CharField(50, unique=True)
#     password_hash = fields.CharField(128)

#     def verify_password(self, password):
#         return bcrypt.verify(password, self.password_hash)


# User_Pydantic = pydantic_model_creator(User, name="User")
# UserIn_Pydantic = pydantic_model_creator(
#     User, name="UserIn", exclude_readonly=True
# )


# class NewsArticle(Model):
#     id = fields.IntField(pk=True)
#     url = fields.CharField(128)
#     text = fields.TextField()


# NewsArticle_Pydantic = pydantic_model_creator(NewsArticle, name="NewsArticle")
# NewsArticleIn_Pydantic = pydantic_model_creator(
#     NewsArticle, name="NewsArticleIn", exclude_readonly=True
# )
