# Django Template API Documentation

A comprehensive Django REST API template with authentication, user management, task processing, and monitoring capabilities.

## Overview

This API provides a complete foundation for building scalable web applications with the following features:

- **User Authentication & Management**: JWT-based authentication with comprehensive user profiles
- **Background Task Processing**: Celery integration for asynchronous task execution
- **Device Tracking**: Security monitoring through device login tracking
- **Email Management**: Email confirmation and password recovery workflows
- **Payment Integration**: Stripe integration for subscription and payment handling
- **Monitoring**: Health checks and Prometheus metrics
- **Documentation**: Complete OpenAPI/Swagger documentation

## Quick Start

### 1. Authentication

First, register a new user or login to get JWT tokens:

```bash
# Register a new user
curl -X POST http://localhost:8000/api/access/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe", 
    "password": "secure_password",
    "password_confirm": "secure_password"
  }'

# Login to get tokens
curl -X POST http://localhost:8000/api/access/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password"
  }'
```

### 2. Using the API

Include the JWT token in the Authorization header for protected endpoints:

```bash
curl -X GET http://localhost:8000/api/access/users/me/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Background Tasks

Create and monitor background tasks:

```bash
# Create a task
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "type": "add",
    "x": 5,
    "y": 3
  }'

# Check task status
curl -X GET http://localhost:8000/tasks/TASK_ID/
```

## Architecture

### Technology Stack

- **Framework**: Django 5.2.6 with Django REST Framework
- **Authentication**: JWT tokens with SimpleJWT
- **Database**: PostgreSQL (configurable via environment)
- **Task Queue**: Celery with RabbitMQ
- **Caching**: Redis
- **Monitoring**: Prometheus metrics
- **Documentation**: drf-spectacular (OpenAPI 3.0)
- **File Storage**: Configurable storage backends

### Key Components

#### 1. User Management System
- Custom user model with email-based authentication
- Profile management with avatar uploads
- Credit system for feature usage
- Device tracking for security

#### 2. Authentication System
- JWT-based authentication
- Token refresh mechanisms
- Password recovery workflows
- Email confirmation system

#### 3. Task Processing System
- Celery integration for background tasks
- Task status monitoring
- Multiple task types (math operations, data processing, long-running tasks)

#### 4. Monitoring & Health Checks
- Health check endpoints for load balancers
- Prometheus metrics for monitoring
- Comprehensive logging

## API Structure

### Base URLs

| Environment | URL |
|------------|-----|
| Local Development | `http://localhost:8000` |
| Production | `https://api.example.com` |

### Endpoint Categories

| Category | Base Path | Description |
|----------|-----------|-------------|
| Core | `/` | Home, health checks, tasks |
| Authentication | `/api/access/auth/` | Login, token refresh |
| Users | `/api/access/users/` | User management |
| Devices | `/api/access/logged-devices/` | Device tracking |
| Password Management | `/api/access/reset-password-control/` | Password recovery |
| Email Management | `/api/access/email-confirmation-control/` | Email verification |
| Pre-Registration | `/api/access/pre-register/` | Email collection |
| Documentation | `/api/docs/`, `/api/redoc/` | API documentation |
| Monitoring | `/metrics` | Prometheus metrics |

## Authentication

The API uses JWT (JSON Web Token) authentication with the following workflow:

1. **Registration**: Create account with `POST /api/access/users/`
2. **Login**: Get tokens with `POST /api/access/auth/login/`
3. **API Calls**: Include `Authorization: Bearer <token>` header
4. **Token Refresh**: Refresh expired tokens with `POST /api/access/auth/refresh/`

### Token Configuration

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Rotation**: Refresh tokens are rotated on use
- **Blacklisting**: Old refresh tokens are blacklisted

## Data Models

### User Model Features

The `CustomUserModel` extends Django's built-in user model with:

- Email-based authentication (primary field)
- Avatar/profile picture support
- Credit system integration
- Stripe customer ID for payments
- Phone number and birth date fields
- Email confirmation status
- Notification preferences
- Device tracking relationships

### Security Features

- UUID primary keys (prevents enumeration attacks)
- Password reset request tracking
- Device login monitoring
- Email confirmation workflow
- Secure file upload handling

## Background Tasks

The API includes Celery integration for background task processing:

### Task Types

1. **Math Operations**: Add two numbers
2. **Long-Running Tasks**: Simulate time-intensive operations
3. **Data Processing**: Process arbitrary data

### Task Management

- Create tasks with `POST /tasks/`
- Monitor status with `GET /tasks/{task_id}/`
- Tasks return unique identifiers for tracking
- Status includes: PENDING, STARTED, SUCCESS, FAILURE, RETRY, REVOKED

## File Upload & Storage

### Avatar Management

- Users can upload profile pictures
- Files stored using configurable storage backends
- Support for private media storage
- Automatic file handling in serializers

### Storage Configuration

The system supports multiple storage backends:
- Local file storage (development)
- Cloud storage (production)
- Private media storage for sensitive files

## Monitoring & Observability

### Health Checks

- `GET /health/` - Basic health status
- `GET /` - API information and status

### Metrics

- `GET /metrics` - Prometheus-format metrics
- Request/response metrics
- Database connection metrics
- Celery task metrics

### Logging

Comprehensive logging configuration:
- Console output for development
- Configurable log levels
- Separate loggers for Django and Celery

## Error Handling

### Standardized Error Responses

All endpoints return consistent error formats:

```json
{
  "error": "Error description",
  "details": {
    "field_name": ["Field-specific error message"]
  }
}
```

### HTTP Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

## Security Considerations

### Authentication Security

- JWT tokens with configurable expiration
- Refresh token rotation
- Token blacklisting
- Email-based user identification

### Data Protection

- Password hashing with Django's secure hashers
- UUID primary keys
- Request/response logging
- CORS configuration support

### Input Validation

- Comprehensive serializer validation
- Password strength requirements
- Email format validation
- File upload restrictions

## Environment Configuration

### Required Environment Variables

```bash
# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Celery
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost
```

### Optional Configuration

```bash
# Logging
DJANGO_LOG_LEVEL=INFO

# Static Files
STATIC_ROOT=/path/to/static/files
```

## Deployment

### Docker Support

The project includes Docker configuration:
- `Dockerfile` for the main application
- `Dockerfile.celery` for Celery workers
- `docker-compose.yml` for orchestration
- Kubernetes manifests in `k8s/` directory

### Production Considerations

1. **Database**: Use PostgreSQL in production
2. **Static Files**: Configure proper static file serving
3. **Media Files**: Use cloud storage for user uploads
4. **Monitoring**: Set up Prometheus and Grafana
5. **Logging**: Configure centralized logging
6. **Security**: Enable HTTPS and security headers

## Development

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test access
python manage.py test core
```

### Code Quality

The project includes:
- `.flake8` configuration for linting
- `.pre-commit-config.yaml` for pre-commit hooks
- `pyproject.toml` for project metadata

## API Documentation

### Interactive Documentation

- **Swagger UI**: `/api/docs/` - Interactive API testing interface
- **ReDoc**: `/api/redoc/` - Clean, readable documentation
- **OpenAPI Schema**: `/api/schema/` - Machine-readable API specification

### Documentation Features

- Complete endpoint documentation
- Request/response examples
- Authentication requirements
- Error response formats
- Model schemas and relationships

## Support & Contributing

### Getting Help

1. Check the documentation files in `/docs/`
2. Review the OpenAPI schema at `/api/schema/`
3. Use the interactive documentation at `/api/docs/`

### Development Guidelines

1. Follow Django and DRF best practices
2. Add comprehensive docstrings to new code
3. Include tests for new functionality
4. Update documentation for API changes
5. Use the provided linting and formatting tools

This API template provides a solid foundation for building scalable, secure web applications with comprehensive documentation and monitoring capabilities.