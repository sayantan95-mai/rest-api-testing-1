# tests/test_booking.py
import pytest
from src.api_client import APIClient
from src.helpers.booking import BookingHelper


# Fixture to provide BookingHelper instance
@pytest.fixture(scope="module")  # Use module scope if client doesn't change per test
def booking_helper(api_client: APIClient):
    return BookingHelper(api_client)


# Test class to group booking tests
class TestBookingWorkflow:
    created_booking_id = None  # Store ID for cleanup

    def test_create_booking(self, booking_helper: BookingHelper, sample_booking_data):
        """Tests creating a new booking."""
        response = booking_helper.create_booking(sample_booking_data)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )
        response_data = response.json()
        assert "bookingid" in response_data
        assert response_data["booking"]["firstname"] == sample_booking_data["firstname"]
        # Store the ID for later tests/cleanup
        TestBookingWorkflow.created_booking_id = response_data["bookingid"]
        print(
            f"Created booking ID: {self.created_booking_id}"
        )  # For visibility during test run

    def test_get_booking(self, booking_helper: BookingHelper, sample_booking_data):
        """Tests retrieving the created booking."""
        assert TestBookingWorkflow.created_booking_id is not None, (
            "Booking ID not created"
        )
        response = booking_helper.get_booking(TestBookingWorkflow.created_booking_id)
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )
        response_data = response.json()
        assert response_data["firstname"] == sample_booking_data["firstname"]
        assert response_data["lastname"] == sample_booking_data["lastname"]

    def test_update_booking(
        self, booking_helper: BookingHelper, authenticated_api_client
    ):
        """Tests updating the created booking (requires auth)."""
        # Use the authenticated client and token provided by the fixture
        client, token = authenticated_api_client
        # Re-initialize helper IF the fixture returns a client with modified headers
        # Otherwise, just use the token with the existing helper instance
        # booking_helper_auth = BookingHelper(client) # If client headers were modified by fixture

        assert TestBookingWorkflow.created_booking_id is not None, (
            "Booking ID not created"
        )
        updated_data = {
            "firstname": "Pytest-Updated",
            "lastname": "User-Updated",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {"checkin": "2025-02-01", "checkout": "2025-02-05"},
            "additionalneeds": "Dinner",
        }
        # Use the token with the helper method
        response = booking_helper.update_booking(
            TestBookingWorkflow.created_booking_id, updated_data, token
        )
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )
        response_data = response.json()
        assert response_data["firstname"] == "Pytest-Updated"
        assert response_data["totalprice"] == 200

    def test_partial_update_booking(
        self, booking_helper: BookingHelper, authenticated_api_client
    ):
        """Tests partially updating the booking (requires auth)."""
        client, token = authenticated_api_client
        assert TestBookingWorkflow.created_booking_id is not None, (
            "Booking ID not created"
        )
        partial_data = {
            "firstname": "Pytest-Patched",
            "additionalneeds": "Late Checkout",
        }

        response = booking_helper.partial_update_booking(
            TestBookingWorkflow.created_booking_id, partial_data, token
        )
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )
        response_data = response.json()
        assert response_data["firstname"] == "Pytest-Patched"
        assert response_data["additionalneeds"] == "Late Checkout"
        # Verify other fields remain unchanged from the previous update step
        assert response_data["lastname"] == "User-Updated"

    def test_delete_booking(
        self, booking_helper: BookingHelper, authenticated_api_client
    ):
        """Tests deleting the created booking (requires auth)."""
        client, token = authenticated_api_client
        assert TestBookingWorkflow.created_booking_id is not None, (
            "Booking ID not created"
        )

        response = booking_helper.delete_booking(
            TestBookingWorkflow.created_booking_id, token
        )
        # restful-booker returns 201 Created on successful delete
        assert response.status_code == 201, (
            f"Expected 201, got {response.status_code}. Body: {response.text}"
        )

        # Verify deletion by trying to GET the booking again
        verify_response = booking_helper.get_booking(
            TestBookingWorkflow.created_booking_id
        )
        assert verify_response.status_code == 404, (
            f"Expected 404 after deletion, got {verify_response.status_code}"
        )
        # Mark as cleaned up
        TestBookingWorkflow.created_booking_id = None

    # Optional: Add a cleanup fixture if tests might fail before deletion
    # def test_cleanup(self, booking_helper: BookingHelper, authenticated_api_client):
    #     """ Ensures cleanup even if a test fails mid-way (requires careful implementation) """
    #     client, token = authenticated_api_client
    #     if TestBookingWorkflow.created_booking_id:
    #         try:
    #             print(f"Running cleanup: Deleting booking ID {TestBookingWorkflow.created_booking_id}")
    #             booking_helper.delete_booking(TestBookingWorkflow.created_booking_id, token)
    #         except Exception as e:
    #             print(f"Error during cleanup: {e}")
    #         TestBookingWorkflow.created_booking_id = None


def test_get_nonexistent_booking(booking_helper: BookingHelper):
    """Tests getting a booking ID that does not exist."""
    response = booking_helper.get_booking(9999999)  # Use an unlikely ID
    assert response.status_code == 404, (
        f"Expected 404, got {response.status_code}. Body: {response.text}"
    )


# Add more tests for filtering get_booking_ids, edge cases, invalid data, etc.
