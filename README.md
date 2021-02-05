<div align="center">
  <h1>FastAPI minimal project with PostgreSQL and user authentication</h1>
</div>

<div align="center">
  <a href="https://github.com/psf/black/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-brightgreen.svg"></a>
  <a href="https://github.com/edesz/fastapi-async-db-auth/pulls"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a>
  <a href="https://github.com/edesz/fastapi-async-db-auth/actions">
    <img src="https://github.com/edesz/fastapi-async-db-auth/workflows/CI/badge.svg"/>
  </a>
  <a href="https://github.com/psf/black/blob/master/LICENSE"><img alt="Open Source?: Yes" src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github"></a>
  <a href="https://codecov.io/gh/edesz/fastapi-async-db-auth">
    <img src="https://codecov.io/gh/edesz/fastapi-async-db-auth/branch/main/graph/badge.svg?token=JYERV7HUHM"/>
  </a>
</div>

<div align="center">
<a href="https://www.python.org/">
  <img alt="Made With: Python" src="https://forthebadge.com/images/badges/made-with-python.svg"/>
</a>
<a href="https://html.com/">
  <img alt="Uses: HTML" src="https://forthebadge.com/images/badges/uses-html.svg"/>
</a>
</div>

<div align="center">
<a href="https://codecov.io/gh/edesz/fastapi-async-db-auth">
  <img alt="https://github.com/edesz/fastapi-async-db-auth" src="https://codecov.io/gh/edesz/fastapi-async-db-auth/branch/main/graphs/sunburst.svg"/>
</a>
</div>

## [Table of Contents](#table-of-contents)

- [About](#about)
- [Usage](#usage)
- [Features](#features)
- [Contributions](#contributions)
- [Attributions](#attributions)
- [Future Improvements](#future-improvements)

## [About](#about)
This is a **minimal** [FastAPI](https://fastapi.tiangolo.com/) project, with `fastapi` and external dependencies to facilitate use of a postgres database (controlled by `sqlalchemy` and requiring user authentication) and unit tests (mocking database access, when required) to start using FastAPI with

- an asynchronous database (only create and read) operations controlled by `sqlalchemy`, per [FastAPI async database docs](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
- alembic migrations, per Alembic docs ([configure](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [auto-generate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations))
- OAuth2 with Password (and hashing), Bearer with JWT tokens (follows the [FastAPI authentication docs](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#oauth2-with-password-and-hashing-bearer-with-jwt-tokens))

## [Features](#features)
Included
- API using the [ASGI-based FastAPI](https://fastapi.tiangolo.com/advanced/middleware/#adding-asgi-middlewares) web framework to serve dummy [Machine Learning (ML)](https://en.wikipedia.org/wiki/Machine_learning) predictions
- [PostgreSQL database](https://www.postgresql.org/) support to store records (ML predictions), with migrations facilitated via `alembic`
- mock unit tests using [containerized Postgres database](https://hub.docker.com/_/postgres)
- user-authentication with Oauth2 using password, bearer and JWT
- `Makefile` with tasks to reproducibly run necessary tasks
  - alembic migrations
  - happypath unit tests
  - use `gunicorn` to manage `uvicorn` for a mixture of asynchronous Python and parallelism
  - api verification using Python `requests`
- use `tox`, the `virtualenv` management CLI tool to
  - isolate dependencies from systemwide Python packages
  - run tests locally and in CI
- demo (basic) webpage content (templates, static files)

Not included
- no support for [deployment of the API](https://fastapi.tiangolo.com/deployment/)
- any other sophisticated features; it is up to you to chose how to implement your API
- features specific to ML applications that prevent broader use of this project in other types of applications

## [Usage](#usage)
1. Clone this repo into the desired path eg. `$HOME/Downloads`
   ```bash
   $ git clone https://github.com/edesz/fastapi-async-db-auth.git $HOME/Downloads
   ```
2. Export environment variables
   ```bash
   # Gunicorn
   $ HOST=0.0.0.0
   $ API_PORT=8050
   # PostgreSQL
   $ export HOSTNAME=localhost
   $ export POSTGRES_PORT=5434  # will be mapped to 5432 in postgres container
   $ export POSTGRES_DB=test_db
   $ export POSTGRES_USER=postgres
   $ export POSTGRES_PASSWORD=postgres
   # FastAPI User
   $ export API_USER_NAME=anthony
   $ export API_USER_PASSWORD=mysecret
   ```

## [Contributions](#contributions)
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=edesz&theme=blue-green&repo=fastapi-async-db-auth)](https://github.com/edesz/fastapi-async-db-auth)

Contributions to this project are welcome via pull requests!

Just keep in mind that the goal of this project is to provide a fast method to start using FastAPI with databases and user-authentication. So, it is hoped that this project will remain a "minimal" one.

If you prefer to use an exhaustive pre-made template, with a more complete set of production-ready features, then the official [FastAPI project generation templates](https://fastapi.tiangolo.com/project-generation/) are likely a better fit to your use-case.

Also, note that an officially supported [ML-specific FastAPI `cookiecutter`](https://fastapi.tiangolo.com/project-generation/#machine-learning-models-with-spacy-and-fastapi) already exists and may fit ML applications better than this minimal project.

If you would like to make a change, you can run tests locally from the project's root directory using

```bash
$ make tests
```
in order to test the changes you've made. Also, verify that the CI workflow (github actions) completes successfully.

## [Attributions](#attributions)
This project is primarily based on
- authentication
  - the section from the FastAPI documentation on [OAuth2 with password, bearer and json web token](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
  - [prettyprinted project](https://github.com/PrettyPrinted/youtube_video_code/blob/master/2021/01/05/FastAPI%20Authentication%20Example%20With%20OAuth2%20and%20Tortoise%20ORM/fastapiauth/main.py)
- (for SQLAlchemy model classes) the [`ahmednafies/fastapi_async_db`](https://github.com/ahmednafies/fastapi_async_db) project

Other sources used were documentation for the following Python packages
- [FastAPI](https://fastapi.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#tutorial)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/index.html)
- [Databases](https://www.encode.io/databases/)
- [PyTest](https://docs.pytest.org/en/stable/monkeypatch.html#simple-example-monkeypatching-functions)
- [Coverage (for Pytest)](https://coverage.readthedocs.io/en/coverage-5.4/index.html)
- [Tox](https://tox.readthedocs.io/en/latest/index.html)

## [Future Improvements](#future-improvements)
A preliminary list of ideas to be added is shown below
1. Add *Update* and *Delete* components of [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) to `api/app/topics/routes.py`
2. Add [ReadTheDocs](https://readthedocs.org/) documentation
3. Explore feasibility of including `docker-compose` to streamline interaction between database and api
4. Convert this repository into a [Python `cookiecutter`](https://cookiecutterreadthedocs.io/en/latest/), to allow for more customized re-use when starting new projects
   - offer basic deployment support for Azure, Heroku and other platforms, via GitHub Actions workflow, based on `cookiecutter` input
