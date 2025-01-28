import pytest

@pytest.mark.parametrize(
    "method, endpoint, data, mock_response, expected_status, expected_json",
    [
        # /login endpoint
        ('POST', '/login', {"username": "user", "password": "pass"}, ({"token": "abc123"}, 200), 200, {"token": "abc123"}),
        ('POST', '/login', {"username": "user", "password": "wrong"}, ({"message": "Invalid credentials"}, 400), 400, {"message": "Invalid credentials"}),
        ('POST', '/login', {"username": "user", "password": "pass"}, ({"message": "Service encountered an error"}, 503), 503, {"message": "Service encountered an error"}),
        
        # /register endpoint
        ('POST', '/register', {"username": "new_user", "password": "new_pass"}, ({"user_id": "user123"}, 201), 201, {"user_id": "user123"}),
        ('POST', '/register', {"username": "existing_user", "password": "new_pass"}, ({"message": "Username already exists"}, 400), 400, {"message": "Username already exists"}),
        
        # /reset-password endpoint
        ('POST', '/reset-password', {"email": "user@example.com"}, ({"message": "Reset email sent"}, 200), 200, {"message": "Reset email sent"}),
        ('POST', '/reset-password', {"email": "invalid_email"}, ({"message": "Invalid email"}, 400), 400, {"message": "Invalid email"}),
        
        # /reset-password/<token> endpoint
        ('POST', '/reset-password/validtoken123', {"new_password": "new_pass"}, ({"message": "Password reset successful"}, 200), 200, {"message": "Password reset successful"}),
        ('POST', '/reset-password/invalidtoken', {"new_password": "new_pass"}, ({"message": "Invalid or expired token"}, 400), 400, {"message": "Invalid or expired token"}),
        
        # /refresh-token endpoint
        ('POST', '/refresh-token', {"refresh_token": "refreshtoken123"}, ({"token": "newtoken123"}, 200), 200, {"token": "newtoken123"}),
        ('POST', '/refresh-token', {"refresh_token": "invalidtoken"}, ({"message": "Invalid refresh token"}, 400), 400, {"message": "Invalid refresh token"}),
        
        # /deactivate-account endpoint
        ('POST', '/deactivate-account', {"user_id": "user123"}, ({"message": "Account deactivated"}, 200), 200, {"message": "Account deactivated"}),
        ('POST', '/deactivate-account', {"user_id": "invalid_user"}, ({"message": "User not found"}, 404), 404, {"message": "User not found"}),
        
        # /health endpoint
        ('GET', '/health', None, ({"status": "healthy"}, 200), 200, {"status": "healthy"}),
        ('GET', '/health', None, ({"status": "unhealthy"}, 503), 503, {"status": "unhealthy"}),
    ]
)
def test_endpoints(client, method, endpoint, data, mock_response, expected_status, expected_json):
    """
    Parameterized test for multiple endpoints covering various scenarios.
    """
    client_app, mock_http_client = client
    mock_http_client.make_request.return_value = mock_response
    
    # Construct the full URL with the blueprint prefix
    full_endpoint = f'/api/auth{endpoint if endpoint.startswith("/") else "/" + endpoint}'
    
    # Execute the request based on the HTTP method
    if method == 'POST':
        response = client_app.post(full_endpoint, json=data)
    elif method == 'GET':
        response = client_app.get(full_endpoint, json=data)
    else:
        pytest.fail(f"HTTP method {method} not supported in tests.")
    
    # Assertions
    assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
    assert response.get_json() == expected_json, f"Expected JSON {expected_json}, got {response.get_json()}"
    
    # Prepare the data to pass to make_request
    request_data = data if data is not None else None
    
    # Assert that make_request was called with correct parameters
    mock_http_client.make_request.assert_called_once_with(
        method,
        endpoint,
        data=request_data,
        headers=None  # Update if headers are used in requests
    )

def test_unexpected_exception(client):
    """
    Test all endpoints when an unexpected exception occurs.
    """
    client_app, mock_http_client = client
    # Setup the mock to raise an exception
    mock_http_client.make_request.side_effect = Exception("Unexpected error")
    
    # Define all endpoints and methods to test exception handling
    endpoints_to_test = [
        ('POST', '/login', {"username": "user", "password": "pass"}),
        ('POST', '/register', {"username": "new_user", "password": "new_pass"}),
        ('POST', '/reset-password', {"email": "user@example.com"}),
        ('POST', '/reset-password/validtoken123', {"new_password": "new_pass"}),
        ('POST', '/refresh-token', {"refresh_token": "refreshtoken123"}),
        ('POST', '/deactivate-account', {"user_id": "user123"}),
        ('GET', '/health', None),
    ]
    
    for method, endpoint, data in endpoints_to_test:
        # Construct the full URL with the blueprint prefix
        full_endpoint = f'/api/auth{endpoint if endpoint.startswith("/") else "/" + endpoint}'
        
        # Execute the request based on the HTTP method
        if method == 'POST':
            response = client_app.post(full_endpoint, json=data)
        elif method == 'GET':
            response = client_app.get(full_endpoint)
        else:
            pytest.fail(f"HTTP method {method} not supported in tests.")
        
        # Assertions for internal server error
        assert response.status_code == 500, f"Expected status 500, got {response.status_code} for {method} {full_endpoint}"
        assert response.get_json() == {"message": "Internal server error"}, f"Unexpected JSON response for {method} {full_endpoint}"
        
        # Assert that make_request was called with correct parameters
        mock_http_client.make_request.assert_called_with(
            method,
            endpoint,
            data=data if data else None,
            headers=None
        )
        
        # Reset mock between iterations
        mock_http_client.make_request.reset_mock()
