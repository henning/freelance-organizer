.PHONY: docker-build

manage = poetry run python manage.py

ifeq (, $(shell ls /etc/fedora-release))
POETRY_INSTALL_CMD=sudo apt-get -y install python3-poetry
else
POETRY_INSTALL_CMD=sudo dnf install poetry
endif


docker-build:
	cd docker; \
		docker compose build dev-app

docker-run-dev:
	cd docker; \
		docker compose up dev-app

docker-dev-import:
	cd docker; \
		docker compose run dev-import

docker-prod-import:
	echo "TYPE THIS:\n" \
	echo "cd docker;" \
		"docker compose run prod-import"

docker-run-prod:
	cd docker; \
		docker compose up -d prod-app

docker-tag-latest-production:
	docker tag freelance-organizer:latest freelance-organizer:production

db-tmp-backup:
	cp db.sqlite3 tmp/backups/db.sqlite3_$(date +%Y-%m-%d_%s)

test-all: test test-style

test:
	poetry run pytest

test-style:
	poetry run pytest --flake8

migrations_create:
	$(manage) makemigrations

migrations_run:
	$(manage) migrate

run: migrations_run
	$(manage) runserver

shell:
	$(manage) shell

.PHONY: setup-project
setup-project:
	$(POETRY_INSTALL_CMD)
	poetry install

