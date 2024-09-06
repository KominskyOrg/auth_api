from flask import Blueprint, request, jsonify, current_app
import requests 

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

AUTH_SERVICE_URL = f"{current_app.config['BASE_URL']}/service/auth"

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response = requests.post(f'{AUTH_SERVICE_URL}/login', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    response = requests.post(f'{AUTH_SERVICE_URL}/register', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password_request():
    data = request.json
    response = requests.post(f'{AUTH_SERVICE_URL}/reset-password', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.json
    response = requests.post(f'{AUTH_SERVICE_URL}/reset-password/{token}', json=data)
    return jsonify(response.json()), response.status_code

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    data = request.json
    response = requests.post(f'{AUTH_SERVICE_URL}/refresh-token', json=data)
    return jsonify(response.json()), response.status_code