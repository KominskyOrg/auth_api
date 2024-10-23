from flask import Blueprint, request, jsonify
import requests
import logging
import os
from requests.exceptions import (
    HTTPError,
    ConnectionError,
    Timeout,
    RequestException,
)

stack_bp = Blueprint("stack", __name__, url_prefix="/api/stack")

@stack_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint to verify that the stack_api service is running.
    """
    return jsonify({"status": "OK"}), 200
