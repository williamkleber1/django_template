from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .tasks import add_numbers, long_running_task, process_data
import json


def home(request):
    """Home page view"""
    return JsonResponse({
        'message': 'Django Template with Celery and RabbitMQ',
        'status': 'running',
        'endpoints': {
            'tasks': '/tasks/',
            'health': '/health/',
            'metrics': '/metrics'
        }
    })


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'django-app'
    })


@csrf_exempt
@require_http_methods(["POST"])
def create_task(request):
    """Create and execute Celery tasks"""
    try:
        data = json.loads(request.body)
        task_type = data.get('type', 'add')
        
        if task_type == 'add':
            x = data.get('x', 1)
            y = data.get('y', 2)
            task = add_numbers.delay(x, y)
            return JsonResponse({
                'task_id': task.id,
                'task_type': 'add_numbers',
                'parameters': {'x': x, 'y': y}
            })
        
        elif task_type == 'long_running':
            duration = data.get('duration', 5)
            task = long_running_task.delay(duration)
            return JsonResponse({
                'task_id': task.id,
                'task_type': 'long_running_task',
                'parameters': {'duration': duration}
            })
        
        elif task_type == 'process_data':
            task_data = data.get('data', 'sample data')
            task = process_data.delay(task_data)
            return JsonResponse({
                'task_id': task.id,
                'task_type': 'process_data',
                'parameters': {'data': task_data}
            })
        
        else:
            return JsonResponse({'error': 'Invalid task type'}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def task_status(request, task_id):
    """Check task status"""
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    return JsonResponse({
        'task_id': task_id,
        'status': task.status,
        'result': task.result if task.status == 'SUCCESS' else None,
        'error': str(task.result) if task.status == 'FAILURE' else None
    })
