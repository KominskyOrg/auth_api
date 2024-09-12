from flask import Blueprint, request, jsonify, current_app
import requests
import logging
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth_service:5001/service/auth')

def make_auth_request(endpoint, data):
    url = f"{AUTH_SERVICE_URL}/{endpoint}"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
        return jsonify({"error": "Service unavailable"}), 503

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return make_auth_request('login', data)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    return make_auth_request('register', data)

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_request():
    data = request.json
    return make_auth_request('reset-password', data)

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.json
    return make_auth_request(f'reset-password/{token}', data)

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    data = request.json
    return make_auth_request('refresh-token', data)