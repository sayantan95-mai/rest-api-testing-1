# src/helpers/auth.py
# Uses the APIClient for consistency

from src.api_client import APIClient
from src import config # Import config module
import logging

logger = logging.getLogger(__name__)

def authenticate(api_client: APIClient, username: str = None, password: str = None) -> str | None:
    """
    Authenticates using the provided API client and credentials.

    Args:
        api_client: The APIClient instance.
        username: API username (defaults to config).
        password: API password (defaults to config).

    Returns:
        The authentication token string if successful, None otherwise.

    Raises:
        requests.exceptions.RequestException: If the authentication request fails.
    """
    auth_username = username or config.AUTH_USERNAME
    auth_password = password or config.AUTH_PASSWORD

    if not auth_username or not auth_password:
        logger.error("Authentication credentials not found in config or arguments.")
        return None # Or raise ValueError

    payload = {
        "username": auth_username,
        "password": auth_password
    }
    try:
        # Use the client's post method, passing the relative endpoint
        response = api_client.post(config.AUTH_URL.replace(config.BASE_URL, ''), json=payload) # Pass relative path
        # Assuming successful auth returns 200 and a token in JSON
        token = response.json().get("token")
        if not token:
            logger.error("Authentication successful but no token found in response.")
            return None
        logger.info("Authentication successful.")
        return token
    except Exception as e: # Catch exceptions raised by send_request or .json()
        logger.error(f"Authentication failed: {e}")
        # Option 1: Return None (as before)
        # return None
        # Option 2: Re-raise the exception for testability
        raise