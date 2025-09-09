#!/bin/bash

# Deploy script for Kubernetes

set -e

NAMESPACE="django-app"
IMAGE_TAG=${1:-latest}

echo "Deploying Django Template to Kubernetes..."
echo "Namespace: $NAMESPACE"
echo "Image Tag: $IMAGE_TAG"

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply all Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/postgres-deployment -n $NAMESPACE
kubectl wait --for=condition=available --timeout=300s deployment/redis-deployment -n $NAMESPACE
kubectl wait --for=condition=available --timeout=300s deployment/rabbitmq-deployment -n $NAMESPACE
kubectl wait --for=condition=available --timeout=300s deployment/django-deployment -n $NAMESPACE
kubectl wait --for=condition=available --timeout=300s deployment/celery-deployment -n $NAMESPACE
kubectl wait --for=condition=available --timeout=300s deployment/prometheus-deployment -n $NAMESPACE
kubectl wait --for=condition=available --timeout=300s deployment/grafana-deployment -n $NAMESPACE

# Run Django migrations
echo "Running Django migrations..."
kubectl exec -n $NAMESPACE -it deployment/django-deployment -- python manage.py migrate

echo "Deployment completed successfully!"
echo ""
echo "Service endpoints:"
echo "- Django App: kubectl port-forward -n $NAMESPACE service/django-service 8000:80"
echo "- Grafana: kubectl port-forward -n $NAMESPACE service/grafana-service 3000:3000"
echo "- Prometheus: kubectl port-forward -n $NAMESPACE service/prometheus-service 9090:9090"
echo "- RabbitMQ Management: kubectl port-forward -n $NAMESPACE service/rabbitmq-service 15672:15672"
