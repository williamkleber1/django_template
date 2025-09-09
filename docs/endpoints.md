# API Endpoints Documentation

This document provides comprehensive information about all available API endpoints in the Django Template API.

## Base URL

- **Local Development:** `http://localhost:8000`
- **Production:** `https://api.example.com`

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

Most endpoints require authentication unless explicitly marked as public.

## Core Endpoints

### Home / Welcome

**GET /** 
- **Summary:** API Home and Information
- **Authentication:** None required (Public)
- **Description:** Returns basic information about the API and available endpoints

**Response Example:**
```json
{
  "message": "Django Template with Celery and RabbitMQ",
  "status": "running",
  "endpoints": {
    "tasks": "/tasks/",
    "health": "/health/",
    "metrics": "/metrics",
    "docs": "/api/docs/",
    "redoc": "/api/redoc/"
  }
}
```

### Health Check

**GET /health/**
- **Summary:** Service Health Status
- **Authentication:** None required (Public)
- **Description:** Health check endpoint for monitoring and load balancers

**Response Example:**
```json
{
  "status": "healthy",
  "service": "django-app"
}
```

## Task Management Endpoints

### Create Task

**POST /tasks/**
- **Summary:** Create and Execute Celery Background Tasks
- **Authentication:** None required (Public)
- **Description:** Creates different types of background tasks for asynchronous processing

**Request Body:**
```json
{
  "type": "add|long_running|process_data",
  "x": 5,              // For 'add' type
  "y": 3,              // For 'add' type  
  "duration": 10,      // For 'long_running' type (seconds)
  "data": "sample"     // For 'process_data' type
}
```

**Task Types:**
- **add**: Adds two numbers together
- **long_running**: Simulates a long-running process
- **process_data**: Processes arbitrary string data

**Response Example:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_type": "add_numbers",
  "parameters": {
    "x": 5,
    "y": 3
  }
}
```

### Get Task Status

**GET /tasks/{task_id}/**
- **Summary:** Check Task Status and Results
- **Authentication:** None required (Public)
- **Description:** Retrieves the current status and result of a background task

**Path Parameters:**
- `task_id` (string): UUID of the task to check

**Response Example:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "SUCCESS",
  "result": 8,
  "error": null
}
```

**Task Statuses:**
- `PENDING`: Task is waiting to be processed
- `STARTED`: Task has been started
- `SUCCESS`: Task completed successfully
- `FAILURE`: Task failed with an error
- `RETRY`: Task is being retried
- `REVOKED`: Task was revoked/cancelled

## Authentication Endpoints

### Login

**POST /api/access/auth/login/**
- **Summary:** User Authentication
- **Authentication:** None required (Public)
- **Description:** Authenticates user credentials and returns JWT tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response Example:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "email": "user@example.com",
    "username": "johndoe"
  }
}
```

### Refresh Token

**POST /api/access/auth/refresh/**
- **Summary:** Refresh JWT Token
- **Authentication:** None required (Public)
- **Description:** Exchanges a refresh token for a new access token

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response Example:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## User Management Endpoints

### List Users

**GET /api/access/users/**
- **Summary:** List All Users
- **Authentication:** Required
- **Description:** Retrieves a paginated list of all users (admin functionality)

**Query Parameters:**
- `page` (integer): Page number for pagination

**Response Example:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/access/users/?page=2",
  "previous": null,
  "results": [
    {
      "userId": "user123",
      "username": "johndoe",
      "email": "john@example.com",
      "is_email_confirmed": true,
      "created": "2023-01-15T10:30:00Z"
    }
  ]
}
```

### Create User

**POST /api/access/users/**
- **Summary:** Register New User
- **Authentication:** None required (Public)
- **Description:** Creates a new user account

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secure_password",
  "password_confirm": "secure_password",
  "phone_number": "+1234567890",
  "birth_date": "1990-01-15"
}
```

**Response Example:**
```json
{
  "userId": "user123",
  "username": "johndoe",
  "email": "john@example.com",
  "avatar": null,
  "phone_number": "+1234567890",
  "birth_date": "1990-01-15",
  "dalle_credits": 0,
  "subscription_credits": 0,
  "is_email_confirmed": false,
  "notification_settings": {
    "email": {"updates": false, "tips": false, "payment": false},
    "push": {"updates": false, "tips": false, "payment": false}
  },
  "created": "2023-01-15T10:30:00Z",
  "updated": "2023-01-15T10:30:00Z"
}
```

### Get User Details

**GET /api/access/users/{userId}/**
- **Summary:** Get Specific User Details
- **Authentication:** Required
- **Description:** Retrieves detailed information about a specific user

### Get Current User

**GET /api/access/users/me/**
- **Summary:** Get Current User Profile
- **Authentication:** Required
- **Description:** Retrieves the profile of the currently authenticated user

**Response Example:**
```json
{
  "userId": "user123",
  "username": "johndoe",
  "email": "john@example.com",
  "avatar": "https://example.com/avatars/user123.jpg",
  "phone_number": "+1234567890",
  "birth_date": "1990-01-15",
  "dalle_credits": 50,
  "subscription_credits": 100,
  "is_email_confirmed": true,
  "notification_settings": {
    "email": {"updates": true, "tips": false, "payment": true},
    "push": {"updates": false, "tips": false, "payment": true}
  },
  "created": "2023-01-15T10:30:00Z",
  "updated": "2023-01-20T15:45:00Z"
}
```

### Update Current User

**PUT|PATCH /api/access/users/me/update/**
- **Summary:** Update Current User Profile
- **Authentication:** Required
- **Description:** Updates the profile of the currently authenticated user

**Request Body (Partial):**
```json
{
  "username": "johndoe_updated",
  "phone_number": "+1987654321",
  "notification_settings": {
    "email": {"updates": true, "tips": true, "payment": true}
  }
}
```

## Device Management Endpoints

### List User Devices

**GET /api/access/logged-devices/**
- **Summary:** List Current User's Devices
- **Authentication:** Required
- **Description:** Retrieves all devices associated with the current user

**Response Example:**
```json
{
  "count": 3,
  "results": [
    {
      "id": "device123",
      "user_email": "john@example.com",
      "device_type": "desktop",
      "device_name": "Chrome Browser",
      "last_login_at": "2023-01-20T15:45:00Z",
      "place": "New York",
      "created": "2023-01-15T10:30:00Z",
      "updated": "2023-01-20T15:45:00Z"
    }
  ]
}
```

### Register New Device

**POST /api/access/logged-devices/**
- **Summary:** Register New Device
- **Authentication:** Required
- **Description:** Registers a new device for the current user

**Request Body:**
```json
{
  "device_type": "mobile",
  "device_name": "iPhone Safari",
  "place": "San Francisco"
}
```

### Update Device Login Time

**POST /api/access/logged-devices/{id}/update_login/**
- **Summary:** Update Device Login Time
- **Authentication:** Required
- **Description:** Updates the last login timestamp for a specific device

**Response Example:**
```json
{
  "message": "Login time updated"
}
```

## Password Management Endpoints

### Password Reset Control

**GET /api/access/reset-password-control/**
- **Summary:** List Password Reset Requests
- **Authentication:** Required
- **Description:** Retrieves password reset control records (admin functionality)

**POST /api/access/reset-password-control/**
- **Summary:** Create Password Reset Request
- **Authentication:** Required
- **Description:** Creates a new password reset request

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

### Password Recovery Email Templates

**GET /api/access/password-recovery-email/**
- **Summary:** List Email Templates
- **Authentication:** Required
- **Description:** Retrieves password recovery email templates

**POST /api/access/password-recovery-email/**
- **Summary:** Create Email Template
- **Authentication:** Required
- **Description:** Creates a new password recovery email template

**Request Body:**
```json
{
  "name": "Password Reset Template",
  "subject": "Reset Your Password",
  "body": "Click here to reset your password: {reset_link}",
  "email_address": "admin@example.com"
}
```

## Email Management Endpoints

### Email Confirmation Control

**GET /api/access/email-confirmation-control/**
- **Summary:** List Email Confirmations
- **Authentication:** Required
- **Description:** Retrieves email confirmation control records

**POST /api/access/email-confirmation-control/**
- **Summary:** Create Email Confirmation
- **Authentication:** Required
- **Description:** Creates a new email confirmation request

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

## Pre-Registration Endpoints

### Pre-Registration

**GET /api/access/pre-register/**
- **Summary:** List Pre-Registrations
- **Authentication:** Required
- **Description:** Retrieves pre-registration records (admin functionality)

**POST /api/access/pre-register/**
- **Summary:** Create Pre-Registration
- **Authentication:** None required (Public)
- **Description:** Creates a pre-registration entry for email collection

**Request Body:**
```json
{
  "email": "interested@example.com"
}
```

## Monitoring Endpoints

### Prometheus Metrics

**GET /metrics**
- **Summary:** Application Metrics
- **Authentication:** None required (Public)
- **Description:** Provides application metrics in Prometheus format for monitoring

## API Documentation Endpoints

### OpenAPI Schema

**GET /api/schema/**
- **Summary:** OpenAPI Schema
- **Authentication:** None required (Public)
- **Description:** Downloads the complete OpenAPI 3.0 schema file

### Swagger UI

**GET /api/docs/**
- **Summary:** Interactive API Documentation
- **Authentication:** None required (Public)
- **Description:** Provides interactive Swagger UI for testing API endpoints

### ReDoc Documentation

**GET /api/redoc/**
- **Summary:** API Reference Documentation
- **Authentication:** None required (Public)
- **Description:** Provides clean, readable API documentation using ReDoc

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Invalid input data",
  "details": {
    "field_name": ["This field is required."]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred."
}
```

## Rate Limiting

Currently, there are no explicit rate limits configured, but it's recommended to implement rate limiting in production environments.

## Pagination

List endpoints use Django REST Framework's pagination:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/endpoint/?page=3",
  "previous": "http://localhost:8000/api/endpoint/?page=1",
  "results": [...]
}
```

- `count`: Total number of items
- `next`: URL for the next page (null if last page)
- `previous`: URL for the previous page (null if first page)
- `results`: Array of items for current page

## Best Practices

1. **Always include the Authorization header** for protected endpoints
2. **Use HTTPS in production** to protect sensitive data
3. **Handle token expiration** by implementing refresh token logic
4. **Validate input data** on the client side before sending requests
5. **Implement proper error handling** for all possible response codes
6. **Use appropriate HTTP methods** (GET for reading, POST for creating, etc.)
7. **Monitor task status** when using background task endpoints

## SDK and Integration

The API follows RESTful conventions and can be integrated with any HTTP client library. Consider creating SDK wrappers for common programming languages to simplify integration.