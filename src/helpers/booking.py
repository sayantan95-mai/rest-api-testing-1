# src/helpers/booking.py
from src.api_client import APIClient
from src import config
import logging
# Removed json import as APIClient handles it
# Removed module-level auth import/token generation

logger = logging.getLogger(__name__)

class BookingHelper:
    """
    Provides methods for interacting with the booking endpoints.
    """
    def __init__(self, api_client: APIClient):
        """
        Initializes the BookingHelper with an APIClient instance.

        Args:
            api_client (APIClient): The API client to use for requests.
        """
        if not isinstance(api_client, APIClient):
            raise TypeError("api_client must be an instance of APIClient")
        self.api_client = api_client
        # Use relative path from config
        self.booking_endpoint = config.BOOKING_URL.replace(config.BASE_URL, '').lstrip('/')

    def get_booking_ids(self, params=None):
        """Gets booking IDs, optionally filtered by params."""
        logger.info(f"Getting booking IDs with params: {params}")
        # APIClient's send_request will raise exceptions on failure
        response = self.api_client.get(self.booking_endpoint, params=params)
        # Assuming success returns 200 and JSON list
        return response # Let the caller handle .json() and specific status checks

    def get_booking(self, booking_id):
        """Gets details for a specific booking ID."""
        logger.info(f"Getting booking details for ID: {booking_id}")
        endpoint = f"{self.booking_endpoint}/{booking_id}"
        response = self.api_client.get(endpoint)
        # Caller can check response.status_code (e.g., 404 for not found)
        return response

    def create_booking(self, booking_data):
        """Creates a new booking."""
        logger.info(f"Creating booking with data: {booking_data}")
        # Use json parameter instead of data=json.dumps
        response = self.api_client.post(self.booking_endpoint, json=booking_data)
        # Assuming success returns 200 and booking details + bookingid
        return response

    def _get_auth_headers(self, token: str) -> dict:
        """Helper to create authentication headers."""
        if not token:
             raise ValueError("Authentication token required for this operation.")
        # Create headers based on default, adding the auth token
        headers = self.api_client.default_headers.copy() # Start with client defaults
        headers["Cookie"] = f"token={token}"
        # Note: Some APIs might expect 'Authorization: Bearer <token>' instead
        return headers

    def update_booking(self, booking_id, booking_data, token: str):
        """Updates an existing booking (full update). Requires auth token."""
        logger.info(f"Updating booking ID {booking_id} with data: {booking_data}")
        endpoint = f"{self.booking_endpoint}/{booking_id}"
        headers = self._get_auth_headers(token)
        response = self.api_client.put(endpoint, json=booking_data, headers=headers)
        # Assuming success returns 200 and updated booking details
        return response

    def partial_update_booking(self, booking_id, partial_data, token: str):
        """Partially updates an existing booking. Requires auth token."""
        logger.info(f"Partially updating booking ID {booking_id} with data: {partial_data}")
        endpoint = f"{self.booking_endpoint}/{booking_id}"
        headers = self._get_auth_headers(token)
        # Ensure Accept header is set if API requires it, client defaults should handle this
        response = self.api_client.patch(endpoint, json=partial_data, headers=headers)
        # Assuming success returns 200 and updated booking details
        return response

    def delete_booking(self, booking_id, token: str):
        """Deletes an existing booking. Requires auth token."""
        logger.info(f"Deleting booking ID: {booking_id}")
        endpoint = f"{self.booking_endpoint}/{booking_id}"
        headers = self._get_auth_headers(token)
        response = self.api_client.delete(endpoint, headers=headers)
        # Assuming success returns 201 (Created) status code upon deletion
        return response