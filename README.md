<div align="center">
  <h1>FastAPI minimal project with PostgreSQL and user authentication</h1>
</div>

<div align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-brightgreen.svg"></a>
  <a href="https://github.com/edesz/fastapi-minimal-ml/pulls"><img alt="PRs Welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square"></a>
  <a href="https://github.com/edesz/fastapi-minimal-ml/actions">
    <img src="https://github.com/edesz/fastapi-minimal-ml/workflows/CI/badge.svg"/>
  </a>
  <a href="https://github.com/edesz/fastapi-minimal-ml/actions">
    <img src="https://github.com/edesz/fastapi-minimal-ml/workflows/CodeQL/badge.svg"/>
  </a>
  <a href="https://en.wikipedia.org/wiki/Open-source_software"><img alt="Open Source?: Yes" src="https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github"></a>
  <a href="https://pyup.io/repos/github/edesz/fastapi-minimal-ml/"><img src="https://pyup.io/repos/github/edesz/fastapi-minimal-ml/shield.svg" alt="Updates" /></a>
</div>
<div align="center">
<a href="https://codecov.io/gh/edesz/fastapi-minimal-ml">
    <img src="https://codecov.io/gh/edesz/fastapi-minimal-ml/branch/main/graph/badge.svg?token=JYERV7HUHM"/>
  </a>
  <a href="https://www.codacy.com/gh/edesz/fastapi-minimal-ml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=edesz/fastapi-minimal-ml&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/cc6ccfd808304591a67917cbb48e4183"/></a>
  <a href="https://wakatime.com/badge/github/edesz/fastapi-minimal-ml.svg"><img alt="wakatime" src="https://wakatime.com/badge/github/edesz/fastapi-minimal-ml.svg"/></a>
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
<a href="https://codecov.io/gh/edesz/fastapi-minimal-ml">
  <img alt="https://github.com/edesz/fastapi-minimal-ml" src="https://codecov.io/gh/edesz/fastapi-minimal-ml/branch/main/graphs/sunburst.svg"/>
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
This is a **minimal** [FastAPI](https://fastapi.tiangolo.com/) project, with the python -based web-framework `fastapi` and external dependencies to facilitate use of a postgres database (controlled by `sqlalchemy` and requiring user authentication) and unit tests (mocking database access, when required) to start using FastAPI with

  - an asynchronous database (only create and read) operations controlled by `sqlalchemy`, per [FastAPI async database docs](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
  - alembic migrations, per Alembic docs ([configure](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [auto-generate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations))
  - OAuth2 with Password (and hashing), Bearer with JWT tokens (follows the [FastAPI authentication docs](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#oauth2-with-password-and-hashing-bearer-with-jwt-tokens))

The database table and SQLAlchemy model are name based on using this project to develop a [Machine Learning (ML)](https://en.wikipedia.org/wiki/Machine_learning) application, but no ML-specific requirements have been enforced here.

## [Features](#features)
Included
  - API using the [ASGI-based FastAPI](https://fastapi.tiangolo.com/advanced/middleware/#adding-asgi-middlewares) web framework to serve ML predictions
  - [PostgreSQL database](https://www.postgresql.org/) support to store records (ML predictions), with migrations facilitated via `alembic`
  - async operations on database using the [`encode/databases`](https://www.encode.io/databases/) package in Python
  - mock unit tests using [containerized Postgres database](https://hub.docker.com/_/postgres)
  - user-authentication with Oauth2 using password, bearer and JWT required in order to post new records (predictions) to the database table
    - a separate table is created to keep track of registered users
  - `Makefile` with tasks to reproducibly run necessary tasks
      - alembic migrations
      - happypath unit tests
      - use `gunicorn` to manage `uvicorn` for a mixture of asynchronous Python and parallelism, when instantiating the API
      - api route verification using Python `requests`
  - use `tox`, the `virtualenv` management CLI tool to
      - isolate dependencies from systemwide Python packages
      - run tests locally and in CI
      - **all python code runs through a `tox` environment**, to ensure reproducibility
  - demo (basic) HTML content (templates, static files)

Not included
  - support for [deployment of the API](https://fastapi.tiangolo.com/deployment/)
  - any other sophisticated features; it is up to you to chose how to further implement your API beyond the basic database operations supported by this project
  - features specific to ML use-cases, that might prevent use of this project in other types of applications
    - a few comments are added throughout the code in places where ML-specific components may be added but, since this is a minimal project, such code comments have been kept to a minimum and it is the user's responsibility to add these in as required

## [Usage](#usage)
1. Clone this repo into the desired path eg. `$HOME/Downloads`
   ```bash
   git clone https://github.com/edesz/fastapi-minimal-ml.git $HOME/Downloads
   ```
2. Export environment variables
   ```bash
   # Gunicorn
   HOST=0.0.0.0
   API_PORT=8050
   # PostgreSQL
   export HOSTNAME=localhost
   export POSTGRES_PORT=5434  # (tests) set to 5434 for containerized postgres in docker-compose.yml
   export POSTGRES_DB=test_db
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=postgres
   # FastAPI User
   export API_USER_NAME=<username>
   export API_USER_PASSWORD=<password>
   ```

## [Contributions](#contributions)
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=edesz&theme=blue-green&repo=fastapi-minimal-ml)](https://github.com/edesz/fastapi-minimal-ml)

Contributions to this project are welcome via pull requests!

The goal of this project is to provide a fast method to start using FastAPI with async database support and user-authentication. So, it is hoped that, through the changes that occur over time, this project will continue to remain a "minimal" one.

If you prefer to use an exhaustive pre-made template, with a more complete set of production-ready features, then the official [FastAPI project generation templates](https://fastapi.tiangolo.com/project-generation/) are likely a better fit to your use-case.

Also, note that an officially supported [ML-specific FastAPI `cookiecutter`](https://fastapi.tiangolo.com/project-generation/#machine-learning-models-with-spacy-and-fastapi) already exists and may fit ML-specific applications better than this minimal starter project.

If you would like to make a change via a pull request, you can use the `Makefile` locally from the project's root directory with

```bash
make tests
```
in order to verify that the changes you've made don't result in failing tests.

## [Attributions](#attributions)
This project is primarily based on
  - authentication
      - the section from the FastAPI documentation on [OAuth2 with password, bearer and json web token](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
      - [prettyprinted project](https://github.com/PrettyPrinted/youtube_video_code/blob/master/2021/01/05/FastAPI%20Authentication%20Example%20With%20OAuth2%20and%20Tortoise%20ORM/fastapiauth/main.py)
  - database operations
      - FastAPI documentation on [async databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/#async-sql-relational-databases)
    - (for SQLAlchemy model classes) the [`ahmednafies/fastapi_async_db`](https://github.com/ahmednafies/fastapi_async_db) project
  - Unit tests
      - FastAPI documentation for [testing](https://fastapi.tiangolo.com/tutorial/testing/)

Other sources that were used are documentation for the following Python packages
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#tutorial)
  - [SQLAlchemy](https://docs.sqlalchemy.org/en/14/index.html)
  - [Databases](https://www.encode.io/databases/)
  - [PyTest](https://docs.pytest.org/en/stable/monkeypatch.html#simple-example-monkeypatching-functions) (plugins: [1](https://github.com/hackebrot/pytest-md), [2](https://github.com/pytest-dev/pytest-html), [3](https://github.com/hackebrot/pytest-emoji), [4](https://github.com/pytest-dev/pytest-repeat))
  - [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.4/index.html)
  - [Tox](https://tox.readthedocs.io/en/latest/index.html)

as well as [documentation for Python projects using Github Actions](https://docs.github.com/en/actions/guides/building-and-testing-python) and [CodeCov's Github Action](https://github.com/codecov/codecov-action#codecov-github-action).

## [Future Improvements](#future-improvements)
A preliminary list of functionality to be implemented is shown below
 1. Add *Update* and *Delete* components of [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) to `api/app/topics/routes.py`
 2. Add [ReadTheDocs](https://readthedocs.org/) documentation
 3. Explore feasibility of including `docker-compose` to streamline interaction between the database and the front-end
 4. Convert this repository into a [Python `cookiecutter`](https://cookiecutterreadthedocs.io/en/latest/), to allow for more customized re-use when starting new projects
    - offer basic deployment support for Azure, Heroku and other platforms, via GitHub Actions workflow, based on user specification in `cookiecutter` input
