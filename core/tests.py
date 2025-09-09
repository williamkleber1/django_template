import json

from django.test import Client, TestCase
from django.urls import reverse


class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        """Test the home endpoint"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "running")
        self.assertIn("endpoints", data)

    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "django-app")

    def test_create_task_invalid_json(self):
        """Test task creation with invalid JSON"""
        response = self.client.post(
            reverse("create_task"), data="invalid json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)

    def test_create_task_invalid_type(self):
        """Test task creation with invalid task type"""
        response = self.client.post(
            reverse("create_task"),
            data=json.dumps({"type": "invalid"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "Invalid task type")
