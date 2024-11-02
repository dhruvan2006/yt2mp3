# Flask YouTube Audio Downloader

A simple Flask application to download audio from YouTube videos in MP3 format.

## Usage

Access the live website [here](https://yt2mp3-839554745582.europe-west4.run.app/).

## Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t yt2mp3 .
   ```

2. Run the container:
    ```bash
    docker run -p 5000:5000 yt2mp3
    ```

3. Access the app at `http://127.0.0.1:5000/`.
