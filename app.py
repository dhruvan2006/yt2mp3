from flask import Flask, request, send_file, render_template
from pytubefix import YouTube
import os
import re

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(filename):
    """
    Sanitize filename by:
    1. Removing invalid filesystem characters
    2. Limiting length
    3. Ensuring it ends with .mp3
    """
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'[\s\W]+', '_', filename)
    filename = ''.join(char for char in filename if ord(char) < 128)
    filename = filename[:240]
    if not filename.lower().endswith('.mp3'):
        filename = filename + '.mp3'
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_audio():
    url = request.form['url']

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()

        filename = sanitize_filename(f"{yt.title}.mp3")
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        if not os.path.abspath(file_path).startswith(os.path.abspath(DOWNLOAD_FOLDER)):
            raise Exception("Invalid file path")

        audio_stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
