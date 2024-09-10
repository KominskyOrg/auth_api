# Makefile

# Variables
DOCKER_COMPOSE = docker-compose
FLAKE8 = flake8
BLACK = black

# Default target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make build          Build the Docker images"
	@echo "  make up             Start the Docker containers"
	@echo "  make down           Stop the Docker containers"
	@echo "  make logs           Show logs from the Docker containers"
	@echo "  make lint           Run flake8 for linting"
	@echo "  make format         Run black for code formatting"
	@echo "  make test           Run tests"
	@echo "  make clean          Clean up Docker containers and images"

# Build the Docker images
.PHONY: build
build:
	$(DOCKER_COMPOSE) build

# Start the Docker containers
.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

# Stop the Docker containers
.PHONY: down
down:
	$(DOCKER_COMPOSE) down

# Show logs from the Docker containers
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f

# Run flake8 for linting
.PHONY: lint
lint:
	$(FLAKE8) .

# Run black for code formatting
.PHONY: format
format:
	$(BLACK) .

# Run tests
.PHONY: test
test:
	$(DOCKER_COMPOSE) run --rm api pytest

# Clean up Docker containers and images
.PHONY: clean
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
