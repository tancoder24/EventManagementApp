# Define variables
DOCKER_COMPOSE := docker-compose
DOCKER_BUILD := docker build
PROJECT_NAME := my_first_django_container

# Docker-related targets
build:
	$(DOCKER_BUILD) -t $(PROJECT_NAME) .

start:
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) logs -f app

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

logs:
	$(DOCKER_COMPOSE) logs -f app

clean:
	docker system prune -f

# Django-related targets
makemigrations:
	$(DOCKER_COMPOSE) up -d app  # Start the "app" service if not running
	$(DOCKER_COMPOSE) exec app python manage.py makemigrations

migrate:
	$(DOCKER_COMPOSE) up -d app  # Start the "app" service if not running
	$(DOCKER_COMPOSE) exec app python manage.py migrate

test:
	$(DOCKER_COMPOSE) up -d app  # Start the "app" service if not running
	$(DOCKER_COMPOSE) exec app python manage.py test

createsuperuser:
	$(DOCKER_COMPOSE) up -d app  # Start the "app" service if not running
	$(DOCKER_COMPOSE) exec app python manage.py createsuperuser
