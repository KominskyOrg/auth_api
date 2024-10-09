import pytest
from unittest.mock import patch
from app import create_app
from requests.exceptions import ConnectionError
from app.config import get_config
from requests.exceptions import RequestException, HTTPError

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
        
# -------------------- Config Tests -------------------- #

def test_get_config_unknown_env(monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'unknown_env')
    with pytest.raises(ValueError) as exc_info:
        get_config()
    assert 'Unknown environment' in str(exc_info.value)
    
def test_get_config_staging_env(monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'staging')
    config = get_config()
    assert config.ENV == 'staging'
    assert config.DEBUG == False
    
def test_get_config_production_env(monkeypatch):
    monkeypatch.setenv('FLASK_ENV', 'production')
    config = get_config()
    assert config.ENV == 'production'
    assert config.DEBUG == False


# -------------------- Login Route Tests -------------------- #

@patch('app.routes.requests.post')
def test_login_success(mock_post, client):
    # Mock the external POST request response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "message": "Login successful",
        "token": "mock_jwt_token"
    }

    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })

    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'
    assert 'token' in response.json

@patch('app.routes.requests.post')  # Ensure this path is correct
def test_login_invalid_credentials(mock_post, client):
    mock_post.return_value.status_code = 401
    mock_post.return_value.json.return_value = {
        "message": "Invalid credentials"
    }

    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'wrong_password'
    })

    assert response.status_code == 401
    assert response.json['message'] == 'Invalid credentials'

# -------------------- Register Route Tests -------------------- #

@patch('app.routes.requests.post')
def test_register_success(mock_post, client):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "message": "Registration successful",
        "user_id": "mock_user_id"
    }

    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'secure_password',
        'username': 'newuser'
    })

    assert response.status_code == 201
    assert response.json['message'] == 'Registration successful'
    assert 'user_id' in response.json

@patch('app.routes.requests.post')
def test_register_existing_user(mock_post, client):
    mock_post.return_value.status_code = 409
    mock_post.return_value.json.return_value = {
        "message": "User already exists"
    }

    response = client.post('/api/auth/register', json={
        'email': 'existinguser@example.com',
        'password': 'password123',
        'username': 'existinguser'
    })

    assert response.status_code == 409
    assert response.json['message'] == 'User already exists'

# -------------------- Reset Password Route Tests -------------------- #

@patch('app.routes.requests.post')
def test_reset_password_request_success(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "message": "Password reset link sent"
    }

    response = client.post('/api/auth/reset-password', json={
        'email': 'user@example.com'
    })

    assert response.status_code == 200
    assert response.json['message'] == 'Password reset link sent'

@patch('app.routes.requests.post')
def test_reset_password_success(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "message": "Password has been reset successfully"
    }

    reset_token = "mock_reset_token"

    response = client.post(f'/api/auth/reset-password/{reset_token}', json={
        'new_password': 'new_secure_password'
    })

    assert response.status_code == 200
    assert response.json['message'] == 'Password has been reset successfully'

@patch('app.routes.requests.post')
def test_reset_password_invalid_token(mock_post, client):
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {
        "message": "Invalid or expired reset token"
    }

    invalid_token = "invalid_token"

    response = client.post(f'/api/auth/reset-password/{invalid_token}', json={
        'new_password': 'new_password'
    })

    assert response.status_code == 400
    assert response.json['message'] == 'Invalid or expired reset token'

# -------------------- Refresh Token Route Tests -------------------- #

@patch('app.routes.requests.post')
def test_refresh_token_success(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "message": "Token refreshed",
        "token": "new_mock_jwt_token"
    }

    response = client.post('/api/auth/refresh-token', json={
        'refresh_token': 'mock_refresh_token'
    })

    assert response.status_code == 200
    assert response.json['message'] == 'Token refreshed'
    assert 'token' in response.json

@patch('app.routes.requests.post')
def test_refresh_token_invalid(mock_post, client):
    mock_post.return_value.status_code = 401
    mock_post.return_value.json.return_value = {
        "message": "Invalid refresh token"
    }

    response = client.post('/api/auth/refresh-token', json={
        'refresh_token': 'invalid_refresh_token'
    })

    assert response.status_code == 401
    assert response.json['message'] == 'Invalid refresh token'

# -------------------- Deactivate Account Route Tests -------------------- #

@patch('app.routes.requests.post')
def test_deactivate_account_success(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "message": "Account deactivated successfully"
    }

    response = client.post('/api/auth/deactivate-account', json={
        'user_id': 'mock_user_id'
    })

    assert response.status_code == 200
    assert response.json['message'] == 'Account deactivated successfully'

@patch('app.routes.requests.post')
def test_deactivate_account_not_found(mock_post, client):
    mock_post.return_value.status_code = 404
    mock_post.return_value.json.return_value = {
        "message": "User not found"
    }

    response = client.post('/api/auth/deactivate-account', json={
        'user_id': 'nonexistent_user_id'
    })

    assert response.status_code == 404
    assert response.json['message'] == 'User not found'

# -------------------- Health Route Tests -------------------- #

def test_health_endpoint(client):
    response = client.get('/api/auth/health')
    assert response.status_code == 200
    assert response.json['status'] == 'OK'

@patch('app.routes.requests.post')
def test_auth_service_unavailable(mock_post, client):
    mock_post.side_effect = ConnectionError("Unable to connect")

    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })

    assert response.status_code == 503
    assert response.json['message'] == 'Authentication service is unavailable'
    
    
# -------------------- Exception Handling Tests -------------------- #

@patch('app.routes.requests.post')
def test_make_auth_request_http_error(mock_post, client):
    mock_post.side_effect = HTTPError("HTTP error occurred")
    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })
    assert response.status_code == 502
    assert response.json['message'] == 'HTTP error occurred'

@patch('app.routes.requests.post')
def test_make_auth_request_request_exception(mock_post, client):
    mock_post.side_effect = RequestException("Request exception occurred")
    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })
    assert response.status_code == 502
    assert response.json['message'] == 'An error occurred while connecting to authentication service'

@patch('app.routes.requests.post')
def test_make_auth_request_general_exception(mock_post, client):
    mock_post.side_effect = Exception("General exception occurred")
    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })
    assert response.status_code == 500
    assert response.json['message'] == 'Internal server error'

@patch('app.routes.requests.post')
def test_make_auth_request_invalid_json(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.side_effect = ValueError("No JSON object could be decoded")
    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })
    assert response.status_code == 502
    assert response.json['message'] == 'Invalid response from authentication service'

@patch('app.routes.requests.post')
def test_make_auth_request_unexpected_status_code(mock_post, client):
    mock_post.return_value.status_code = 600  # Unexpected status code
    mock_post.return_value.json.return_value = {
        "message": "Unknown error"
    }
    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })
    assert response.status_code == 502
    assert response.json['message'] == 'Unexpected response from authentication service'

@patch('app.routes.requests.post')
def test_make_auth_request_server_error(mock_post, client):
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {
        "message": "Internal server error"
    }
    response = client.post('/api/auth/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })
    assert response.status_code == 503
    assert response.json['message'] == 'Authentication service encountered an error'
