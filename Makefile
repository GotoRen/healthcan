DOCKER=docker
COMPOSE=docker-compose
UP=$(COMPOSE) up -d
BUILD=$(COMPOSE) build --no-cache
EXEC=$(COMPOSE) exec
LOGS=$(COMPOSE) logs -f
APP=app
DB=db

all: build up

build: ## docker build
	$(BUILD)

up: ## docker up
	$(UP)

stop: ## docker stop
	$(COMPOSE) stop

down: ## docker down
	$(COMPOSE) down

down/data: ## delete persistent volume
	rm -r ./db/data

down/all: ## delete images, network, containers
	$(DOCKER) system prune --all

down/vol: ## delete volumes
	$(DOCKER) volume prune

app/healthcan: ## app container bash
	$(EXEC) $(APP) bash

app/db: ## db container bash
	$(EXEC) $(DB) bash

mysql: ## db(MySQL) container's MySQL access
	$(EXEC) $(DB) mysql --defaults-extra-file=/home/access.cnf

logs: ## docker logs 
	$(LOGS)

logs/app: ## app container logs
	$(LOGS) $(APP)

logs/db: ## db container logs
	$(LOGS) $(DB)

help: ## display this help screen
	@grep -E '^[a-zA-Z/_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
