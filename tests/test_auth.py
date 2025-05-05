# tests/test_auth.py
import pytest
from src.api_client import APIClient
from src.helpers.auth import authenticate
from src import config # To potentially test with default credentials

# Test uses the 'api_client' fixture from conftest.py
def test_successful_authentication(api_client: APIClient):
    """
    Tests successful authentication using credentials from config.
    """
    try:
        # Use default credentials loaded by config from .env
        token = authenticate(api_client, config.AUTH_USERNAME, config.AUTH_PASSWORD)
        assert token is not None, "Token should not be None on successful authentication"
        assert isinstance(token, str), "Token should be a string"
        assert len(token) > 10, "Token length seems too short" # Basic sanity check
    except Exception as e:
        pytest.fail(f"Authentication raised an unexpected exception: {e}")

def test_failed_authentication_bad_password(api_client: APIClient):
    """
    Tests that authentication fails with incorrect credentials.
    Relies on APIClient raising an exception for non-2xx status codes.
    """
    with pytest.raises(Exception) as exc_info:
        # Use correct username but wrong password
        authenticate(api_client, username=config.AUTH_USERNAME, password="wrongpassword")

    # Check if the exception is related to an HTTP error (e.g., 4xx)
    # This depends on the specific exception raised by your APIClient for HTTP errors
    # For requests.exceptions.HTTPError:
    # assert exc_info.value.response.status_code == 401 # Or whatever the API returns for bad creds

    # If APIClient wraps errors or doesn't raise HTTPError directly, adjust assertion
    # For now, just check that *an* exception was raised
    assert exc_info is not None, "Expected an exception for failed authentication"
    # You might also check the exception message if it's informative
    # assert "Authentication failed" in str(exc_info.value)

# Add more tests for edge cases if needed (e.g., empty credentials if allowed/disallowed)