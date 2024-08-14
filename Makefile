include .env
export $(shell sed 's/=.*//' .env)

.PHONY: help up start stop restart status ps clean

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Up all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up $(c)

up-d: ## Up all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up -d $(c)

start: ## Start all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) start $(c)

build: ## Build all or c=<name> containers in background
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build $(c)

build-d: ## Build all or c=<name> containers in foreground
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) up --build -d $(c)

stop: ## Stop all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) stop $(c)

restart: ## Restart all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) restart $(c)

rebuild: ## Rebuild all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) bash -c "down && up --build -d"

logs: ## Show logs for all or c=<name> containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) logs --tail=$(or $(n), 100) -f $(c)

status: ## Show status of containers
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) ps

ps: status ## Alias of status

clean: ## Clean all data
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) down

down: clean ## Alias of clean

prune: ## Prune all unused containers
	docker system prune --all --volumes

images: ## Show all images
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) images

exec: ## Exec container
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) bash

manage: ## Get health-check info
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) python manage.py $(e)

health-check: ## Get health-check info
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) python manage.py health_check

shell: ## Exec shell
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) python manage.py shell_plus

test: ## Run tests
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) pytest $(or $(e), .)

cov:
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) pytest --cov=. --cov-config=../.coveragerc --no-cov-on-fail --cov-fail-under=90 $(or $(e), .)

coverage: ## Run tests
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) coverage run --rcfile=../.coveragerc -m pytest $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) coverage report --fail-under=90 -m

perform: ## Perform code by black, isort and autoflake
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) black $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) isort $(or $(e), .)
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) autoflake --in-place --remove-all-unused-imports --recursive $(or $(e), .)

lint: ## Check code by pylint
	docker-compose -f $(or $(DOCKER_COMPOSE_FILE), docker-compose.yml) exec $(or $(c), web) pylint --load-plugins pylint_django --django-settings-module=settings $(or $(e), ../src)

quality: perform lint test health-check