# src/api_client.py
import requests
import logging # Use logging instead of print for better control

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url=None, default_headers=None):
        if base_url is None:
            raise ValueError("base_url must be provided")
        self.base_url = base_url
        self.default_headers = default_headers if default_headers is not None else {}

    def _make_url(self, endpoint):
        # Ensure no double slashes if endpoint starts with /
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"

    def send_request(self, method, endpoint, headers=None, json=None, params=None, data=None):
        """Sends an HTTP request."""
        full_url = self._make_url(endpoint)
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            logger.debug(f"Sending {method} request to {full_url} with params={params}, json={json}, data={data}, headers={request_headers}")
            response = requests.request(
                method=method,
                url=full_url,
                headers=request_headers,
                json=json,
                params=params,
                data=data # Keep data for cases where raw body is needed
            )
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            logger.debug(f"Response Status: {response.status_code}, Body: {response.text[:100]}...") # Log snippet
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"{method} Request to {full_url} failed: {e}", exc_info=True)
            # Re-raise the exception so callers know the request failed
            raise

    def get(self, endpoint, params=None, headers=None):
        return self.send_request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint, json=None, data=None, params=None, headers=None):
        return self.send_request("POST", endpoint, json=json, data=data, params=params, headers=headers)

    def put(self, endpoint, json=None, data=None, params=None, headers=None):
         # Corrected method name
        return self.send_request("PUT", endpoint, json=json, data=data, params=params, headers=headers)

    def patch(self, endpoint, json=None, data=None, params=None, headers=None):
         # Corrected method name
        return self.send_request("PATCH", endpoint, json=json, data=data, params=params, headers=headers)

    def delete(self, endpoint, params=None, headers=None):
         # Corrected method name
        return self.send_request("DELETE", endpoint, params=params, headers=headers)