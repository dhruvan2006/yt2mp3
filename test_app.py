import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


## UNIT TESTS ##

def test_index_page_loads(client):
    """Test that the index page loads with a 200 status code."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'YouTube URL:' in response.data

def test_download_audio_success(client, mocker):
    """Test the download audio functionality with a mock."""
    mock_yt = mocker.patch('app.YouTube')
    mock_audio_stream = mocker.Mock()
    mock_audio_stream.download.return_value = None
    
    # Configure mock YouTube object
    mock_yt.return_value.streams.get_audio_only.return_value = mock_audio_stream
    mock_yt.return_value.title = "sample_audio"

    response = client.post('/download', data={'url': 'https://www.youtube.com/watch?v=example'})
    
    assert response.status_code == 200
    assert b'sample_audio.mp3' in response.data

def test_download_audio_failure(client, mocker):
    """Test the download audio route with an invalid URL."""
    # Mock YouTube to raise an exception
    mocker.patch('app.YouTube', side_effect=Exception("Invalid URL"))

    response = client.post('/download', data={'url': 'invalid_url'})
    
    assert response.status_code == 200
    assert b'An error occurred' in response.data


## INTEGRATION TESTS ##

@pytest.mark.parametrize("youtube_url, expected_title", [
    ("https://www.youtube.com/watch?v=jNQXAC9IVRw", "Me at the zoo"),
    ("https://www.youtube.com/watch?v=cZz1oamNbng", "Chinese Beaver With Original Cantonese"),
])
def test_download_integration_success(client, youtube_url, expected_title):
    """Integration test for downloading audio successes."""
    response = client.post('/download', data={'url': youtube_url})
    
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == f'attachment; filename="{expected_title}.mp3"'

@pytest.mark.parametrize("youtube_url, expected_error_message", [
    ("invalid_url", "Invalid YouTube URL"),
    ("https://www.youtube.com/watch?v=nonexistent_video", "nonexistent is unavailable")
])
def test_download_audio_failure(client, youtube_url, expected_error_message):
    """Integration test for downloading audio failures."""
    response = client.post('/download', data={'url': youtube_url})

    assert response.status_code == 200
    assert expected_error_message.encode() in response.data