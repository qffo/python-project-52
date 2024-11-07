install:
	poetry install

dev:
	poetry run python manage.py runserver

make lint:
	poetry run flake8 task_manager

build:
	./build.sh