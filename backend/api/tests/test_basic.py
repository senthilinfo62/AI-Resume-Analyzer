"""
Basic tests for the API.
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_health_check():
    """Test that the health check endpoint returns 200."""
    client = APIClient()
    url = reverse('api-root')
    response = client.get(url)
    assert response.status_code == 200
