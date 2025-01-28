import pytest
from unittest.mock import MagicMock
from app import create_app

@pytest.fixture
def client(mocker):
    """
    Pytest fixture to create a test client with a mocked HTTPClient using pytest-mock.
    
    Yields:
        client (FlaskClient): The Flask test client.
        mock_http_client (MagicMock): The mocked HTTPClient instance.
    """
    app = create_app()
    app.config["TESTING"] = True

    # **Corrected Patch Path**
    # Replace 'app.routes.HTTPClient' with the actual module where HTTPClient is used
    mock_http_client_class = mocker.patch('app.routes.HTTPClient', autospec=True)
    mock_http_client_instance = mock_http_client_class.return_value
    
    # Define default mock behavior (can be overridden in individual tests)
    mock_http_client_instance.make_request.return_value = ({"message": "Success"}, 200)
    
    with app.test_client() as client:
        yield client, mock_http_client_instance
        