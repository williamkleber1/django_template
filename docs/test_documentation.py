"""
Tests for API documentation functionality
"""

from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.urls import reverse


class DocumentationTests(TestCase):
    """Test API documentation endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_swagger_schema_endpoint(self):
        """Test that OpenAPI schema is accessible"""
        url = reverse("schema")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("application/vnd.oai.openapi", response["Content-Type"])

    def test_swagger_ui_endpoint(self):
        """Test that Swagger UI is accessible"""
        url = reverse("swagger-ui")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Django Template API")

    def test_redoc_ui_endpoint(self):
        """Test that ReDoc UI is accessible"""
        url = reverse("redoc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Django Template API")

    def test_home_endpoint_includes_docs(self):
        """Test that home endpoint includes documentation links"""
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that response includes documentation endpoints
        data = response.json()
        self.assertIn("endpoints", data)
        self.assertIn("docs", data["endpoints"])
        self.assertIn("redoc", data["endpoints"])
        self.assertEqual(data["endpoints"]["docs"], "/api/docs/")
        self.assertEqual(data["endpoints"]["redoc"], "/api/redoc/")


class APIEndpointsDocumentationTests(TestCase):
    """Test that API endpoints have proper documentation"""

    def setUp(self):
        self.client = APIClient()

    def test_home_endpoint_documentation(self):
        """Test home endpoint has proper documentation"""
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("message", data)
        self.assertIn("status", data)
        self.assertIn("endpoints", data)

        # Verify comprehensive endpoint list
        expected_endpoints = ["tasks", "health", "metrics", "docs", "redoc"]
        for endpoint in expected_endpoints:
            self.assertIn(endpoint, data["endpoints"])

    def test_health_endpoint_documentation(self):
        """Test health endpoint has proper response format"""
        url = reverse("health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("status", data)
        self.assertIn("service", data)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "django-app")
