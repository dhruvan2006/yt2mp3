import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page_loads(client):
    """Test that the index page loads with a 200 status code."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'YouTube URL:' in response.data
