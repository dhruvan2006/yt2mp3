from flask import Flask, request, send_file, render_template_string
from pytubefix import YouTube
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
    <form method="POST" action="/download">
        <label for="url">YouTube URL:</label>
        <input type="text" name="url" id="url" required>
        <input type="submit" value="Download Audio">
    </form>
    '''

@app.route('/download', methods=['POST'])
def download_audio():
    url = request.form['url']
    
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()
        
        filename = f"{yt.title}.mp3"
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        
        audio_stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template_string('''
            <h1>Error</h1>
            <p>{{ error_message }}</p>
            <a href="/">Go back</a>
        ''', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
