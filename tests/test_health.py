# tests/test_health.py
import pytest
from src.api_client import APIClient
from src import config # To get the relative health check URL path

# The test function automatically receives the 'api_client' instance
# because 'api_client' is defined as a fixture in conftest.py
def test_health_check(api_client: APIClient):
    """
    Tests the /ping health check endpoint.
    Verifies that the endpoint is reachable and returns an expected successful status code.
    """
    try:
        # Construct the relative path for the health check endpoint
        health_endpoint = config.HEALTHCHECK_URL.replace(config.BASE_URL, '').lstrip('/')

        # Use the APIClient instance (provided by the fixture) to send a GET request
        response = api_client.get(health_endpoint)

        # Assert that the status code indicates success.
        # restful-booker's /ping endpoint returns 201 Created.
        assert response.status_code == 201, \
            f"Expected status code 201 for health check, but got {response.status_code}. Response text: '{response.text}'"

        # Optionally, assert the response body if it's consistent and expected
        # For restful-booker, the body is typically 'Created'
        assert response.text == "Created", \
            f"Expected response body 'Created', but got '{response.text}'"

    except Exception as e:
        # If any exception occurs during the API call (e.g., network error, timeout),
        # fail the test with an informative message.
        pytest.fail(f"Health check request failed unexpectedly: {e}")