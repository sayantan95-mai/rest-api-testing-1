# src/config.py
import os
from dotenv import load_dotenv

# Load variables from .env file into environment variables
load_dotenv()

# It's better to raise an error if critical config is missing
BASE_URL = os.getenv("API_BASE_URL")
if not BASE_URL:
    raise ValueError("API_BASE_URL environment variable not set.")

# Construct endpoints from base URL
AUTH_URL = f"{BASE_URL}/auth"
HEALTHCHECK_URL = f"{BASE_URL}/ping"
BOOKING_URL = f"{BASE_URL}/booking"

# Get credentials from environment variables
AUTH_USERNAME = os.getenv("API_USERNAME", "admin") # Provide default or raise error if needed
AUTH_PASSWORD = os.getenv("API_PASSWORD", "password123") # Provide default or raise error if needed


DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Example of how you might load default test data (optional)
# import json
# DEFAULT_BOOKING_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'tests', 'data', 'booking_data.json')
# try:
#     with open(DEFAULT_BOOKING_DATA_PATH, 'r') as f:
#         DEFAULT_BOOKING_DATA = json.load(f)
# except FileNotFoundError:
#     DEFAULT_BOOKING_DATA = {} # Or handle error