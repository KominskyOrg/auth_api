from flask import Blueprint, request, jsonify
import logging
from kom_python_core import HTTPClient
from .config import get_config

config = get_config()

logger = logging.getLogger(__name__)

auth_client = HTTPClient(base_url=config.AUTH_SERVICE_URL, timeout=5)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    logger.info("Login request received")
    response_data, status_code = auth_client.make_request('POST', '/login', data=data)
    return jsonify(response_data), status_code


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    logger.info("Register request received")
    response_data, status_code = auth_client.make_request('POST', '/register', data=data)
    return jsonify(response_data), status_code


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password_request():
    data = request.json
    logger.info("Reset password request received")
    response_data, status_code = auth_client.make_request('POST', '/reset-password', data=data)
    return jsonify(response_data), status_code


@auth_bp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.json
    logger.info(f"Reset password with token request received:{token}")
    response_data, status_code = auth_client.make_request('POST', f'/reset-password/{token}', data=data)
    return jsonify(response_data), status_code


@auth_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    data = request.json
    logger.info("Refresh token request received")
    response_data, status_code = auth_client.make_request('POST', '/refresh-token', data=data)
    return jsonify(response_data), status_code


@auth_bp.route("/deactivate-account", methods=["POST"])
def deactivate_account():
    data = request.json
    logger.info("Deactivate account request received")
    response_data, status_code = auth_client.make_request('POST', '/deactivate-account', data=data)
    return jsonify(response_data), status_code


@auth_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint to verify that the auth_api service is running.
    """
    return jsonify({"status": "OK"}), 200
