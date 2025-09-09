.PHONY: help dev build test lint clean deploy k8s-deploy docker-build

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development environment
	./dev.sh

build: ## Build Docker images
	docker-compose build

test: ## Run tests
	python manage.py test

lint: ## Run code linting
	python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

clean: ## Clean up development environment
	docker-compose down -v
	docker system prune -f

deploy: ## Deploy to Kubernetes
	./deploy.sh

k8s-deploy: ## Deploy only Kubernetes manifests
	kubectl apply -f k8s/

docker-build: ## Build and tag Docker images
	docker build -t django-app:latest .
	docker build -t django-app-celery:latest -f Dockerfile.celery .

migrate: ## Run Django migrations
	python manage.py migrate

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

superuser: ## Create Django superuser
	python manage.py createsuperuser

celery-worker: ## Start Celery worker
	celery -A django_app worker --loglevel=info

celery-beat: ## Start Celery beat scheduler
	celery -A django_app beat --loglevel=info
