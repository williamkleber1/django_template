from celery import shared_task
import time
import logging

logger = logging.getLogger(__name__)

@shared_task
def add_numbers(x, y):
    """Simple task to add two numbers"""
    logger.info(f"Adding {x} + {y}")
    return x + y

@shared_task
def long_running_task(duration=5):
    """Task that simulates a long running process"""
    logger.info(f"Starting long running task for {duration} seconds")
    time.sleep(duration)
    logger.info("Long running task completed")
    return f"Task completed after {duration} seconds"

@shared_task
def process_data(data):
    """Task to process some data"""
    logger.info(f"Processing data: {data}")
    # Simulate some processing
    time.sleep(2)
    result = {"processed": True, "data": data, "result": len(data) if isinstance(data, (list, str)) else 1}
    logger.info(f"Data processing completed: {result}")
    return result