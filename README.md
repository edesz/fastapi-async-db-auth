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
  <a href="https://www.codacy.com/gh/edesz/fastapi-minimal-ml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=edesz/fastapi-minimal-ml&amp;utm_campaign=Badge_Coverage"><img src="https://app.codacy.com/project/badge/Coverage/cc6ccfd808304591a67917cbb48e4183"/></a>
  <a href="https://www.codacy.com/gh/edesz/fastapi-minimal-ml/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=edesz/fastapi-minimal-ml&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/cc6ccfd808304591a67917cbb48e4183"/></a>
  <a href="https://www.codefactor.io/repository/github/edesz/fastapi-minimal-ml/overview/main"><img src="https://www.codefactor.io/repository/github/edesz/fastapi-minimal-ml/badge/main" alt="CodeFactor" /></a>
  <a href="https://codeclimate.com/github/edesz/fastapi-minimal-ml/maintainability"><img src="https://api.codeclimate.com/v1/badges/a754c5464e26da508958/maintainability" /></a>
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
-   [About](#about)

-   [Usage](#usage)
    -   [Local Development](#local-development)
    -   [Testing](#testing)
    -   [Verification](#verification)

-   [Features](#features)

-   [Contributions](#contributions)

-   [Attributions](#attributions)

-   [Future Improvements](#future-improvements)

## [About](#about)
This is a **minimal** [FastAPI](https://fastapi.tiangolo.com/) project, with the python -based web-framework `fastapi` and external dependencies to facilitate use of a postgres database (controlled by `sqlalchemy` and requiring user authentication) and unit tests (mocking database access, when required) to start using FastAPI with

-   an asynchronous database (only create and read) operations controlled by `sqlalchemy`, per [FastAPI async database docs](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
-   alembic migrations, per Alembic docs ([configure](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [auto-generate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#auto-generating-migrations))
-   OAuth2 with Password (and hashing), Bearer with JWT tokens (follows the [FastAPI authentication docs](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#oauth2-with-password-and-hashing-bearer-with-jwt-tokens))

The database table and SQLAlchemy model are name based on using this project to develop a [Machine Learning (ML)](https://en.wikipedia.org/wiki/Machine_learning) application, but no ML-specific requirements have been enforced here.

## [Features](#features)
Included

-   API using the [ASGI-based FastAPI](https://fastapi.tiangolo.com/advanced/middleware/#adding-asgi-middlewares) web framework to serve ML predictions

-   [PostgreSQL database](https://www.postgresql.org/) support to store records (ML predictions), with migrations facilitated via `alembic`

-   async operations on database using the [`encode/databases`](https://www.encode.io/databases/) package in Python

-   mock unit tests using [containerized Postgres database](https://hub.docker.com/_/postgres)

-   user-authentication with Oauth2 using password, bearer and JWT required in order to post new records (predictions) to the database table
    -   a separate table is created to keep track of registered users

-   `Makefile` with tasks to reproducibly run necessary tasks
    -   alembic migrations
    -   happypath unit tests, and one unhappypath test
    -   use `gunicorn` to manage `uvicorn` for a mixture of asynchronous Python and parallelism, when instantiating the API
    -   api route verification using Python `requests`

-   use `tox`, the `virtualenv` management CLI tool to
    -   isolate dependencies from systemwide Python packages
    -   run tests locally and in CI
    -   **all python code runs through a `tox` environment**, to ensure reproducibility

-   demo (basic) HTML content (templates, static files)

-   including `docker-compose` to streamline interaction between the database and the front-end

Not included
-   support for [deployment of the API](https://fastapi.tiangolo.com/deployment/)

-   any other sophisticated features; it is up to you to chose how to further implement your API beyond the basic database operations supported by this project

-   features specific to ML use-cases, that might prevent use of this project in other types of applications
    -   a few comments are added throughout the code in places where ML-specific components may be added but, since this is a minimal project, such code comments have been kept to a minimum and it is the user's responsibility to add these in as required

## [Usage](#usage)
### [Local Development](#local-development)
1.  Clone this repo into the desired path eg. `$HOME/Downloads`
    ```bash
    git clone https://github.com/edesz/fastapi-minimal-ml.git $HOME/Downloads
    ```

2.  Export environment variables
    ```bash
    # Gunicorn
    export HOST=0.0.0.0
    export API_PORT=8050
    # PostgreSQL (needed for api)
    export HOSTNAME=localhost
    export POSTGRES_DB=test_db
    export POSTGRES_USER=postgres
    export POSTGRES_PASSWORD=postgres
    export POSTGRES_PORT=5434
    # FastAPI User Authentication
    export JWT_SECRET=<jwt_secret>
    ```

3.  Run API locally
    -   Without using containers<sup>[1](#myfootnote1)</sup>
        ```bash
        make start-container-db api
        ```
    
        <a name="myfootnote1">1</a>: container will be used for database, not for API

    -   Using containers
        ```bash
        make start-containers
        ```

4.  Stop API server
    -   Without using containers

        -   Initiate `SIGINT` (Press <kbd>CTRL</kbd>+<kbd>C</kbd>)
        -   Clean up python artifacts in `fastapi-minimal-ml/api`
            ```bash
            make clean-py
            ```
        -   (Optional) Shutdown containerized postgres database
            ```bash
            make stop-container-db
            ```
        -   (Optional) Remove any folders mounted as database container volumes
            ```bash
            make delete-db-container-volume
            ```

    -   Using containers
        ```bash
        make stop-containers-clean
        ```

        This will

        -   shutdown the containerized postgres database
        -   delete the database container volume
        -   remove Python artifacts

### [Testing](#testing)
1.  Export environment variables (if not already done)
    ```bash
    # PostgreSQL
    export HOSTNAME=localhost
    export POSTGRES_PORT=5434
    export POSTGRES_DB=test_db
    export POSTGRES_USER=postgres
    export POSTGRES_PASSWORD=postgres
    # FastAPI User Authentication
    export JWT_SECRET=<jwt_secret>
    # FastAPI User
    export API_USER_NAME=<username_for_user_in_mocked_database>
    export API_USER_PASSWORD=<password_for_user_in_mocked_database>
    ```

2.  Run tests using a containerized Postgres database and show reports (test summary and code coverage)
    ```bash
    make tests
    ```

    Note that, before running tests, the above command will first create an empty containerized postgress database. No tables will be created in this database. The container will mount the [path to postgres data files](https://www.postgresql.org/docs/current/storage-file-layout.html) (`/var/lib/pgsql/data`) inside the container to `${PWD}/db_data` on the host (on the host, this path will be created if necessary). After tests are completed

    -   the container is automatically shut down and the postgres image is deleted
    -   (when running tests locally) a test summary and code coverage report are opened in separate browser tabs

3.  Clean up
    -   python artifacts in `fastapi-minimal-ml/api`
    -   testing artifacts, summary reports and coverage reports in `fastapi-minimal-ml/tests`

    by running
    ```bash
    make clean-tests
    ```

4.  Remove any local folders mounted as database container volumes
    ```bash
    make delete-db-container-volume
    ```

### [Verification](#verification)
Verify successful response of calling **all** API routes when queried with correct input API parameters and user-authentication headers, using the Python [`requests`](https://pypi.org/project/requests/) package.

This creates an empty containerized postgress database, and creates empty `users` and `predictions` tables. A new user (with username `API_NEW_USER_NAME` and password `API_NEW_USER_PASSWORD`) will be created and added to the users table.

1.  Export environment variables (if not already done)
    ```bash
    # PostgreSQL
    export HOSTNAME=localhost
    export POSTGRES_DB=test_db
    export POSTGRES_USER=postgres
    export POSTGRES_PASSWORD=postgres
    export POSTGRES_PORT=5434
    # FastAPI User Authentication
    export JWT_SECRET=<jwt_secret>
    ```

2.  Verify successful API responses locally
    -   Using containers
        -   Export environment variables
            ```bash
            # Gunicorn
            export HOST=0.0.0.0
            export API_PORT=8050
            # FastAPI User
            export API_NEW_USER_NAME=<username_for_new_user>
            export API_NEW_USER_PASSWORD=<password_for_new_user>
            ```
        -   Verify
            ```bash
            make start-containers-verify
            ```
    -   Without using containers<sup>[1](#myfootnote1)</sup>
        -   Start containerized postgres database
            ```bash
            make start-container-db
            ```
            <a name="myfootnote1">1</a>: container will be used for database, not for API

        -   Start API
            ```bash
            make api
            ```

        -   In a separate shell
            -   Export environment variables
                ```bash
                # Gunicorn
                export HOST=0.0.0.0
                export API_PORT=8050
                # FastAPI User
                export API_NEW_USER_NAME=<username_for_new_user>
                export API_NEW_USER_PASSWORD=<password_for_new_user>
                ```
            -   Verify
                ```bash
                make verify
                ```
            -   Clean up python artifacts in `fastapi-minimal-ml/api_verify`
                ```bash
                make clean-py-verify
                ```

3. (If not using containers) Stop API server
   -   Initiate `SIGINT` (Press <kbd>CTRL</kbd>+<kbd>C</kbd>)

4. Clean up python artifacts in `fastapi-minimal-ml/api`
    ```bash
    make clean-py
    ```

5.  (If not using containers) Shutdown containerized postgres database
    ```bash
    make stop-container-db
    ```

6.  (If not using containers) Remove any folders mounted as database container volumes
    ```bash
    make delete-db-container-volume
    ```

7.  (If using containers) Shutdown containerized postgres database, Delete database container volume and Remove Python artifacts
    ```bash
    make stop-containers-clean
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

-   authentication
    -   the section from the FastAPI documentation on [OAuth2 with password, bearer and json web token](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
    -   [prettyprinted project](https://github.com/PrettyPrinted/youtube_video_code/blob/master/2021/01/05/FastAPI%20Authentication%20Example%20With%20OAuth2%20and%20Tortoise%20ORM/fastapiauth/main.py)

-   database operations
    -   FastAPI documentation on [async databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/#async-sql-relational-databases)
    -   (for SQLAlchemy model classes) the [`ahmednafies/fastapi_async_db`](https://github.com/ahmednafies/fastapi_async_db) project

-   Unit tests
    -   FastAPI documentation for [testing](https://fastapi.tiangolo.com/tutorial/testing/)

Other sources that were used are documentation for the following Python packages

-   [FastAPI](https://fastapi.tiangolo.com/)
-   [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#tutorial)
-   [SQLAlchemy](https://docs.sqlalchemy.org/en/14/index.html)
-   [Databases](https://www.encode.io/databases/)
-   [PyTest](https://docs.pytest.org/en/stable/monkeypatch.html#simple-example-monkeypatching-functions) (plugins: [1](https://github.com/hackebrot/pytest-md), [2](https://github.com/pytest-dev/pytest-html), [3](https://github.com/hackebrot/pytest-emoji), [4](https://github.com/pytest-dev/pytest-repeat))
-   [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.4/index.html)
-   [Tox](https://tox.readthedocs.io/en/latest/index.html)

as well as [documentation for Python projects using Github Actions](https://docs.github.com/en/actions/guides/building-and-testing-python) and [CodeCov's Github Action](https://github.com/codecov/codecov-action#codecov-github-action).

## [Future Improvements](#future-improvements)
A preliminary list of functionality to be implemented is shown below

1.  Add *Update* and *Delete* components of [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) to `api/app/topics/routes.py`

2.  Add [ReadTheDocs](https://readthedocs.org/) documentation

3.  Convert this repository into a [Python `cookiecutter`](https://cookiecutterreadthedocs.io/en/latest/), to allow for more customized re-use when starting new projects
    -   offer basic deployment support for Azure, Heroku and other platforms, via GitHub Actions workflow, based on user specification in `cookiecutter` input
