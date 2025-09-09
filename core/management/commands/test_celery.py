from django.core.management.base import BaseCommand

from core.tasks import add_numbers, long_running_task, process_data


class Command(BaseCommand):
    help = "Test Celery tasks"

    def add_arguments(self, parser):
        parser.add_argument(
            "--task",
            type=str,
            choices=["add", "long_running", "process_data"],
            default="add",
            help="Type of task to run",
        )

    def handle(self, *args, **options):
        task_type = options["task"]

        if task_type == "add":
            self.stdout.write("Starting add task...")
            task = add_numbers.delay(10, 20)
            self.stdout.write(f"Task ID: {task.id}")

        elif task_type == "long_running":
            self.stdout.write("Starting long running task...")
            task = long_running_task.delay(3)
            self.stdout.write(f"Task ID: {task.id}")

        elif task_type == "process_data":
            self.stdout.write("Starting data processing task...")
            task = process_data.delay(["item1", "item2", "item3"])
            self.stdout.write(f"Task ID: {task.id}")

        self.stdout.write(self.style.SUCCESS(f"Successfully started {task_type} task"))
