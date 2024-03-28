import requests, chardet
from flask import Flask, render_template, request, send_file, redirect

app = Flask(__name__)
app.config['use_x_filesend'] = True

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/upload')
def upload_file():
    return render_template('voice-converter.html')
#
#
@app.route('/uploader', methods=['GET', 'POST'])
def convert():
    text = ''
    data = {}
    if request.method == 'POST':
        f = request.files['file']
        text = f.stream.read().decode("utf-8")

    if text != '':
        # An API key is defined here. You'd normally get this from the service you're accessing. It's a form of authentication.
        XI_API_KEY = "b2a0cbf2074ef2970512c2a783041bdb"

        # This is the URL for the API endpoint we'll be making a GET request to.
        url = "https://api.elevenlabs.io/v1/voices"

        # Here, headers for the HTTP request are being set up.
        # Headers provide metadata about the request. In this case, we're specifying the content type and including our API key for authentication.
        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY,
            "Content-Type": "application/json"
        }

        # A GET request is sent to the API endpoint. The URL and the headers are passed into the request.
        response = requests.get(url, headers=headers)

        # The JSON response from the API is parsed using the built-in .json() method from the 'requests' library.
        # This transforms the JSON data into a Python dictionary for further processing.
        data = response.json()

        voice_id = data["voices"][0]["voice_id"]

        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": XI_API_KEY
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=headers)

        with open('output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        return send_file("output.mp3", download_name='output.mp3', as_attachment=True)

    return redirect("/upload")

if __name__ == '__main__':
    app.run()
