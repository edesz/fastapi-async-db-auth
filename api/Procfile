release: alembic upgrade head
web: gunicorn -w 1 --bind ${HOST:0.0.0.0}:${API_PORT:PORT} -k uvicorn.workers.UvicornWorker main:app