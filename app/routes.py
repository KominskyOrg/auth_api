from flask import Blueprint, request, jsonify
import requests
import logging
import os
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

AUTH_SERVICE_URL = os.getenv(
    "AUTH_SERVICE_URL", "http://auth_service:5001/service/auth"
)

logger = logging.getLogger(__name__)

def make_auth_request(endpoint, data):
    url = f"{AUTH_SERVICE_URL}/{endpoint}"
    logger.debug(f"Making request to {url} with data: {data}")
    
    try:
        response = requests.post(url, json=data, timeout=5)  # Set timeout as needed
        logger.debug(f"Received response with status code {response.status_code} from {url}")
        
        # Attempt to parse JSON response
        try:
            response_data = response.json()
        except ValueError:
            logger.error(f"Invalid JSON response from {url}")
            response_data = {"error": "Invalid response from authentication service"}
            return jsonify(response_data), 502  # Bad Gateway
        
        # Check response status code
        if 200 <= response.status_code < 300:
            logger.debug(f"Successful response from {url}: {response_data}")
            return jsonify(response_data), response.status_code
        elif 400 <= response.status_code < 500:
            # Client error; pass through the response
            error_message = response_data.get("error", "Client error")
            logger.warning(f"Client error from {url}: {error_message}")
            return jsonify({"error": error_message}), response.status_code
        elif 500 <= response.status_code < 600:
            # Server error; return 503 Service Unavailable
            logger.error(f"Server error from {url}: {response_data}")
            return jsonify({"error": "Authentication service encountered an error"}), 503
        else:
            # Unexpected status code
            logger.error(f"Unexpected status code {response.status_code} from {url}")
            return jsonify({"error": "Unexpected response from authentication service"}), 502

    except (ConnectionError, Timeout) as e:
        logger.error(f"Connection error when connecting to {url}: {e}")
        return jsonify({"error": "Authentication service is unavailable"}), 503
    except HTTPError as e:
        # This block is optional since HTTPError is handled above
        logger.error(f"HTTP error when connecting to {url}: {e}")
        return jsonify({"error": "HTTP error occurred"}), 502
    except RequestException as e:
        logger.error(f"Request exception when connecting to {url}: {e}")
        return jsonify({"error": "An error occurred while connecting to authentication service"}), 502
    except Exception as e:
        # Catch-all for any other exceptions
        logger.exception(f"Unexpected error when connecting to {url}: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Route definitions remain unchanged
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    logger.info("Login request received")
    return make_auth_request("login", data)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    logger.info("Register request received")
    return make_auth_request("register", data)

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password_request():
    data = request.json
    logger.info("Reset password request received")
    return make_auth_request("reset-password", data)

@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.json
    logger.info(f"Reset password with token request received: {token}")
    return make_auth_request(f"reset-password/{token}", data)

@auth_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    data = request.json
    logger.info("Refresh token request received")
    return make_auth_request("refresh-token", data)

@auth_bp.route("/deactivate-account", methods=["POST"])
def deactivate_account():
    data = request.json
    logger.info("Deactivate account request received")
    return make_auth_request("deactivate-account", data)

@auth_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint to verify that the auth_api service is running.
    """
    return jsonify({"status": "OK"}), 200
