.PHONY: docker-build

manage = python manage.py

docker-build:
	docker build -t freelance-organizer .

test: test-code test-style

test-code:
	py.test

test-style:
	py.test --flake8

migrations_create:
	$(manage) makemigrations

migrations_run:
	$(manage) migrate

run: migrations_run
	$(manage) runserver

shell:
	$(manage) shell