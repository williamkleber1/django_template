#!/bin/bash

# Local development script

set -e

echo "Starting Django Template development environment..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed"
    exit 1
fi

# Start services
echo "Starting services with docker-compose..."
docker-compose up --build -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run migrations
echo "Running Django migrations..."
docker-compose exec web python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating Django superuser (if needed)..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo ""
echo "Development environment is ready!"
echo ""
echo "Available services:"
echo "- Django App: http://localhost:8000"
echo "- Django Admin: http://localhost:8000/admin (admin/admin123)"
echo "- Grafana: http://localhost:3000 (admin/admin)"
echo "- Prometheus: http://localhost:9090"
echo "- RabbitMQ Management: http://localhost:15672 (guest/guest)"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"