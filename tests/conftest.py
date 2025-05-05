# tests/conftest.py
import pytest
import os
import json
from src.api_client import APIClient
from src import config # Import your config module
from src.helpers.auth import authenticate # Import auth helper

# --- Session-Scoped Fixtures (Run Once) ---

@pytest.fixture(scope="session")
def base_url():
    """Fixture to provide the base URL from config."""
    # This ensures the config is loaded and the variable is set
    if not config.BASE_URL:
        pytest.fail("API_BASE_URL environment variable not set or config not loaded.")
    return config.BASE_URL

@pytest.fixture(scope="session")
def api_client(base_url):
    """Fixture to provide a basic, unauthenticated APIClient instance."""
    # Uses the base_url fixture and default headers from config
    return APIClient(base_url=base_url, default_headers=config.DEFAULT_HEADERS)

@pytest.fixture(scope="session")
def sample_booking_data():
    """Fixture to load sample booking data, e.g., from a JSON file."""
    # Construct path relative to this conftest.py file
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'booking_data.json')
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        pytest.fail(f"Test data file not found at: {data_path}")
    except json.JSONDecodeError:
        pytest.fail(f"Error decoding JSON from file: {data_path}")

# --- Function-Scoped Fixtures (Run for Each Test Needing Them) ---

@pytest.fixture(scope="function")
def auth_token(api_client: APIClient):
    """
    Fixture to perform authentication and return the token.
    Runs for each test that requires a fresh token.
    """
    try:
        # Use default credentials from config loaded from .env
        token = authenticate(api_client, config.AUTH_USERNAME, config.AUTH_PASSWORD)
        if not token:
            pytest.fail("Authentication failed - could not retrieve token.")
        return token
    except Exception as e:
        pytest.fail(f"Authentication process failed with an exception: {e}")

# Note: The 'authenticated_api_client' fixture from the previous example
# could also be defined here if needed. It would typically use the 'api_client'
# and 'auth_token' fixtures to return a client instance pre-configured with
# the auth header/cookie. Example:
#
# @pytest.fixture(scope="function")
# def authenticated_api_client(api_client: APIClient, auth_token: str):
#     """ Provides an APIClient instance ready for authenticated requests. """
#     auth_headers = api_client.default_headers.copy()
#     auth_headers["Cookie"] = f"token={auth_token}"
#     # Return a new client instance with these headers, or modify existing one carefully
#     # Depending on whether APIClient instances should be mutable or immutable in tests.
#     # Returning a configured client object:
#     # return APIClient(base_url=api_client.base_url, default_headers=auth_headers)
#     # --- OR ---
#     # Returning the original client and the token (as used in test_booking.py example):
#     return api_client, auth_token