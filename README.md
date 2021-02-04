# fastapi-async-db-auth

![CI](https://github.com/edesz/fastapi-async-db-auth/workflows/CI/badge.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/mit)

## About
A simple repo to demonstrate FastAPI with

- an asynchronous database (create and read) operations controlled by `sqlalchemy`, per [FastAPI async database docs](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
- alembic migrations, per Alembic docs ([configure](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [auto-generate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations))
- OAuth2 with Password (and hashing), Bearer with JWT tokens (follows the [FastAPI authentication docs](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#oauth2-with-password-and-hashing-bearer-with-jwt-tokens))