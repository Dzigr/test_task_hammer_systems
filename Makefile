install: .env
	poetry install

check:
	poetry check

start:
	poetry run python manage.py runserver 0.0.0.0:8000

env:
	cp .env.template .env

commit-i:
	poetry run pre-commit install

commit:
	poetry run pre-commit run -a

req:
	poetry export --without-hashes --format=requirements.txt > requirements.txt