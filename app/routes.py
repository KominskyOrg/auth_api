from flask import Blueprint, request, jsonify, current_app
import requests

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def get_auth_service_url():
    with current_app.app_context():
        return f"{current_app.config['BASE_URL']}/service/auth"

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response = requests.post(f'{get_auth_service_url()}/login', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    response = requests.post(f'{get_auth_service_url()}/register', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_request():
    data = request.json
    response = requests.post(f'{get_auth_service_url()}/reset-password', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.json
    response = requests.post(f'{get_auth_service_url()}/reset-password/{token}', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    data = request.json
    response = requests.post(f'{get_auth_service_url()}/refresh-token', json=data)
    return jsonify(response.json()), response.status_code