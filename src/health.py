import config as cfg  # Imports configuration like the health check URL
from src.api_client import APIClient  # Imports the client used to make API requests

def check_api_health(api_client):
    """
    Checks the health of the API using the configured endpoint.

    Args:
        api_client: An instance of APIClient used to make the request.

    Returns:
        bool: True if the API responds with status 200 or 201, False otherwise.
    """
    try:
        # Use the provided API client to make a GET request to the health check URL
        response = api_client.get(cfg.healthcheck_url) #

        # Check if we got a response and the status code is 200 (OK) or 201 (Created)
        if response and response.status_code in [200, 201]:
            print(f"Health check successful (Status: {response.status_code}).")
            return True
        else:
            # If the response exists but the status code is wrong, print the details
            status_code = response.status_code if response else 'N/A'
            text = response.text if response else 'N/A'
            print(f"Health check failed. Status: {status_code}, Response: {text}")
            return False

    except Exception as e:
        # If any error occurs during the request (like network issues), print it
        print(f"An error occurred during health check: {e}")
        return False

# This part only runs when you execute this script directly
if __name__ == "__main__":
    # Create an instance of the APIClient, using the base URL from config
    client = APIClient(base_url=cfg.base_url) #

    # Call the function to perform the health check
    is_healthy = check_api_health(client)

    # Print a simple message indicating the final result
    if is_healthy:
        print("API status: Healthy")
    else:
        print("API status: Unhealthy")