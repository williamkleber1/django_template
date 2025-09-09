import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .tasks import add_numbers, long_running_task, process_data


@extend_schema(
    summary="API Home",
    description="Welcome endpoint that provides basic information about the API and available endpoints.",
    responses={
        200: OpenApiResponse(
            description="API information and status",
            examples=[
                {
                    "message": "Django Template with Celery and RabbitMQ",
                    "status": "running",
                    "endpoints": {
                        "tasks": "/tasks/",
                        "health": "/health/",
                        "metrics": "/metrics"
                    }
                }
            ]
        )
    },
    tags=["Core"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    """
    API Home endpoint.
    
    Returns basic information about the API including status and available endpoints.
    This endpoint is publicly accessible and doesn't require authentication.
    """
    return Response(
        {
            "message": "Django Template with Celery and RabbitMQ",
            "status": "running",
            "endpoints": {
                "tasks": "/tasks/",
                "health": "/health/",
                "metrics": "/metrics",
                "docs": "/api/docs/",
                "redoc": "/api/redoc/",
            },
        }
    )


@extend_schema(
    summary="Health Check",
    description="Health check endpoint for monitoring and load balancer status checks.",
    responses={
        200: OpenApiResponse(
            description="Service health status",
            examples=[
                {
                    "status": "healthy",
                    "service": "django-app"
                }
            ]
        )
    },
    tags=["Core"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint.
    
    Used by monitoring systems and load balancers to verify that the service
    is running and responding to requests.
    """
    return Response({"status": "healthy", "service": "django-app"})


@extend_schema(
    summary="Create Celery Task",
    description="Create and execute various types of Celery background tasks.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["add", "long_running", "process_data"],
                    "description": "Type of task to execute"
                },
                "x": {
                    "type": "integer",
                    "description": "First number for addition (used with 'add' type)"
                },
                "y": {
                    "type": "integer", 
                    "description": "Second number for addition (used with 'add' type)"
                },
                "duration": {
                    "type": "integer",
                    "description": "Duration in seconds for long running task"
                },
                "data": {
                    "type": "string",
                    "description": "Data to process (used with 'process_data' type)"
                }
            },
            "required": ["type"]
        }
    },
    responses={
        200: OpenApiResponse(
            description="Task created successfully",
            examples=[
                {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "task_type": "add_numbers",
                    "parameters": {"x": 5, "y": 3}
                }
            ]
        ),
        400: OpenApiResponse(description="Invalid task type or JSON"),
        500: OpenApiResponse(description="Internal server error")
    },
    tags=["Tasks"]
)
@csrf_exempt
@require_http_methods(["POST"])
def create_task(request):
    """
    Create and execute Celery tasks.
    
    This endpoint allows you to create different types of background tasks:
    - 'add': Adds two numbers together
    - 'long_running': Simulates a long-running process
    - 'process_data': Processes arbitrary string data
    
    All tasks are executed asynchronously using Celery and return a task ID
    that can be used to check the task status.
    """
    try:
        data = json.loads(request.body)
        task_type = data.get("type", "add")

        if task_type == "add":
            x = data.get("x", 1)
            y = data.get("y", 2)
            task = add_numbers.delay(x, y)
            return JsonResponse(
                {
                    "task_id": task.id,
                    "task_type": "add_numbers",
                    "parameters": {"x": x, "y": y},
                }
            )

        elif task_type == "long_running":
            duration = data.get("duration", 5)
            task = long_running_task.delay(duration)
            return JsonResponse(
                {
                    "task_id": task.id,
                    "task_type": "long_running_task",
                    "parameters": {"duration": duration},
                }
            )

        elif task_type == "process_data":
            task_data = data.get("data", "sample data")
            task = process_data.delay(task_data)
            return JsonResponse(
                {
                    "task_id": task.id,
                    "task_type": "process_data",
                    "parameters": {"data": task_data},
                }
            )

        else:
            return JsonResponse({"error": "Invalid task type"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@extend_schema(
    summary="Get Task Status",
    description="Check the status and result of a Celery task by its ID.",
    parameters=[
        OpenApiParameter(
            name="task_id",
            description="The UUID of the task to check",
            required=True,
            type=str,
            location=OpenApiParameter.PATH
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Task status information",
            examples=[
                {
                    "task_id": "550e8400-e29b-41d4-a716-446655440000",
                    "status": "SUCCESS",
                    "result": 8,
                    "error": None
                }
            ]
        )
    },
    tags=["Tasks"]
)
@require_http_methods(["GET"])
def task_status(request, task_id):
    """
    Check task status and results.
    
    Retrieves the current status of a Celery task including:
    - PENDING: Task is waiting to be processed
    - STARTED: Task has been started
    - SUCCESS: Task completed successfully 
    - FAILURE: Task failed with an error
    - RETRY: Task is being retried
    - REVOKED: Task was revoked/cancelled
    
    For successful tasks, the result will contain the task output.
    For failed tasks, the error field will contain the error message.
    """
    from celery.result import AsyncResult

    task = AsyncResult(task_id)

    return JsonResponse(
        {
            "task_id": task_id,
            "status": task.status,
            "result": task.result if task.status == "SUCCESS" else None,
            "error": str(task.result) if task.status == "FAILURE" else None,
        }
    )
