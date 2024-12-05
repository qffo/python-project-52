install:
	poetry install

dev:
	poetry run python manage.py runserver

make lint:
	poetry run flake8 task_manager

build:
	./build.sh

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

start:
	poetry run gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report
	poetry run coverage xml -o coverage.xml