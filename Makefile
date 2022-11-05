.PHONY: docker-build

manage = python manage.py

docker-build:
	cd docker; \
		docker-compose build freelance-organizer-dev

docker-run-dev:
	cd docker; \
		docker-compose up freelance-organizer-dev

docker-run-prod:
	cd docker; \
		docker-compose up -d freelance-organizer-prod

docker-tag-latest-production:
	docker tag freelance-organizer:latest freelance-organizer:production

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
