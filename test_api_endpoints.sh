#!/bin/bash

# Script to test the access app endpoints manually

set -e

echo "Starting Django development server in background..."
cd /home/runner/work/django_template/django_template

# Start Django server
python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!
sleep 3

echo "Server started with PID: $SERVER_PID"

# Test endpoints
echo "Testing API endpoints..."

echo "1. Creating a test user..."
curl -X POST http://localhost:8000/api/access/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }' \
  -s | jq '.'

echo -e "\n2. Logging in..."
LOGIN_RESPONSE=$(curl -X POST http://localhost:8000/api/access/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }' \
  -s)

echo $LOGIN_RESPONSE | jq '.'

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access')

echo -e "\n3. Getting current user details..."
curl -X GET http://localhost:8000/api/access/users/me/ \
  -H "Authorization: Bearer $TOKEN" \
  -s | jq '.'

echo -e "\n4. Creating a pre-registration (no auth needed)..."
curl -X POST http://localhost:8000/api/access/pre-register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "preregister@example.com"
  }' \
  -s | jq '.'

echo -e "\n5. Creating a logged device..."
DEVICE_RESPONSE=$(curl -X POST http://localhost:8000/api/access/logged-devices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "device_type": "desktop",
    "device_name": "Test Browser",
    "place": "Test City"
  }' \
  -s)

echo $DEVICE_RESPONSE | jq '.'

# Extract device ID
DEVICE_ID=$(echo $DEVICE_RESPONSE | jq -r '.id')

echo -e "\n6. Updating device login time..."
curl -X POST http://localhost:8000/api/access/logged-devices/$DEVICE_ID/update_login/ \
  -H "Authorization: Bearer $TOKEN" \
  -s | jq '.'

echo -e "\n7. Creating reset password control..."
curl -X POST http://localhost:8000/api/access/reset-password-control/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "email": "reset@example.com"
  }' \
  -s | jq '.'

echo -e "\n8. Creating email confirmation control..."
curl -X POST http://localhost:8000/api/access/email-confirmation-control/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "email": "confirm@example.com"
  }' \
  -s | jq '.'

echo -e "\nAPI tests completed successfully!"

# Stop the server
echo "Stopping Django server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo "Done!"