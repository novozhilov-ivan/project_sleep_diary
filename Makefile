export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1
export COMPOSE_IGNORE_ORPHANS=1


build:
	docker compose -f app.yml -f postgres.yml build
pgadmin:
	docker compose -f pgadmin.yml up -d --no-recreate
up: build pgadmin
	docker compose -f app.yml -f postgres.yml up -d
down:
	docker compose -f app.yml -f postgres.yml down
down-all:
	docker compose -f app.yml -f postgres.yml down --remove-orphans

unit: up
		docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest tests/unit" api
integration: up
		docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest tests/integration" api
e2e: up
		docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest tests/e2e" api
all: up
		docker compose -f app.yml -f postgres.yml run --rm --entrypoint="pytest tests/unit tests/integration tests/e2e" api

logs:
		docker compose -f app.yml -f postgres.yml logs --tail=25 api postgres pgadmin
sh:
		docker run -it api bash

bi:
		black . && isort .