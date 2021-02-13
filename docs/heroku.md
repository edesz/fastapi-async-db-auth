# [Heroku](#heroku)

This section walks through this project's support for deploying the FastAPI webapp to Heroku, and also how to delete an existing Heroku app. Two deployment options will be discussed here - with and without containerizing the FastAPI app.

## [Table of Contents](#table-of-contents)
-   [System Requirements](#system-requirements)

-   [Deploying with containers](#deploying-with-containers)
    -   [Prerequisites](#prerequisites)

-   [Deploying without containers](#deploying-without-containers)
    -   [Prerequisites](#prerequisites)

-   [Delete Heroku App](#delete-heroku-app)

-   [Notes](#notes)

## [System Requirements](#system-requirements)

In order to

-   delete a pre-existing app
-   deploy a new app (with or without containers)

the following are are required

1.  install the [Heroku CLI](https://devcenter.heroku.com/categories/command-line) locally (use the [**official standalone installation method**](https://devcenter.heroku.com/articles/heroku-cli#standalone-installation))

2.  set these environment variables locally
    ```bash
    # Gunicorn
    export HOST=0.0.0.0
    # FastAPI User Authentication
    export JWT_SECRET=<jwt_secret>
    # Heroku
    export HD_APP_NAME=fastapi-minimal-ml
    ```

A `release_tasks.sh` file is provided to run database migrations - this will be used with or without a containers.

## [Deploying with containers](#deploying-with-containers)

### [Prerequisites](#prerequisites)
-   `heroku.yml`
    -   [Heroku requirement](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)

-   `Dockerfile.heroku`
    -   Dockerfile
        -   copy source code from local host to container
        -   install required Python packages

**To deploy a containerized app**

Quick Use
1.  Commit changes to `git` repo
    ```bash
    git add .
    git commit -m "<msg>"
    ```

2.  Run
    ```bash
    make heroku-docker-run
    ```

## [Deploying without containers](#deploying-without-containers)

### [Prerequisites](#prerequisites)
-   `Procfile`
    -   [Heroku requirement](https://devcenter.heroku.com/articles/procfile#deploying-to-heroku)

-   `runtime.txt`
    -   specify Python version required

**To deploy an app**

Quick Use
1.  Run
    ```bash
    make heroku-run
    ```

Detailed
1.  [Create Heroku app](https://devcenter.heroku.com/articles/creating-apps#creating-a-named-app)
    ```bash
    make heroku-create  # heroku create $(HD_APP_NAME)
    ```

2.  Add Heroku remote to local git repo
    ```bash
    make heroku-add-remote  # heroku git:remote -a $(HD_APP_NAME)
    ```

3.  Add a PostgreSQL database as a [Heroku Add-On](https://elements.heroku.com/addons/heroku-postgresql)
    ```bash
    make heroku-create-postgres-add-on  # heroku addons:create heroku-postgresql:hobby-dev --app $(HD_APP_NAME)
    ```

    **or**, from the app's **Resources** tab, search for the **Heroku Postgres** add-on and add it to the app.

4.  [Set environment variables for Heroku app](https://devcenter.heroku.com/articles/config-vars#set-a-config-var)
    ```bash
    make heroku-set-env-vars  # heroku config:set <ENV_VAR_NAME>=<ENV_VAR_VALUE>
    ```

5.  Deploy sub-directory to Heroku app
    ```bash
    make heroku-deploy-sub-dir  # git subtree push --prefix api heroku main && heroku logs --tail
    ```

6.  (Optional) Get url for postgres database
    ```bash
    DATABASE_URL=$(heroku config:get DATABASE_URL -a $HD_APP_NAME)
    echo $DATABASE_URL
    ```

## [Delete Heroku App](#delete-heroku-app)
In order to delete an app on Heroku, the procedure configured in this project is the same for an app running with or without a container

**To delete an existing app on Heroku**
1.  Detach PostgreSQL database Add-On from app
    ```bash
    make heroku-detach-postgres-add-on  # heroku addons:destroy heroku-postgresql:hobby-dev --confirm $(HD_APP_NAME)
    ```

2.  Delete Heroku app
    ```bash
    make heroku-delete  # heroku apps:destroy --app $(HD_APP_NAME) --confirm $(HD_APP_NAME)
    ``` 

## [Notes](#notes)
1.  Note that all the supported configuration options, offered by Heroku, for managing deployments are not exposed here.
