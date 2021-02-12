export HD_APP_NAME=fastapi-minimal-mlh
export HOST=0.0.0.0
export JWT_SECRET=myjwtsecret
export WORKER_CLASS=uvicorn.workers.UvicornWorker
export APP_MODULE=main:app

git add .
git commit -m "modified heroku.yml"

# make heroku-docker-run
make heroku-create
make heroku-add-remote
make heroku-create-postgres-add-on
make heroku-set-env-vars
make heroku-stack-set-container
git push heroku main
heroku logs --tail

make heroku-detach-postgres-add-on
make heroku-delete
