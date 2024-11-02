from flask import Flask, request, send_file, render_template
from pytubefix import YouTube
import os

app = Flask(__name__)

app.config['DOWNLOAD_FOLDER'] = 'downloads'
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_audio():
    url = request.form['url']
    
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()
        
        filename = f"{yt.title}.mp3"
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
        
        audio_stream.download(output_path=app.config['DOWNLOAD_FOLDER'], filename=filename)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        error_message = str(e)

        if "could not find match" in error_message:
            user_friendly_message = "Invalid YouTube URL provided."
        else:
            user_friendly_message = f"An error occurred: {error_message}"

        return render_template('error.html', error_message=user_friendly_message)

if __name__ == '__main__':
    app.run(debug=True)
