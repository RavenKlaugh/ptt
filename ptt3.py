from flask import Flask, request, send_file, render_template, jsonify, url_for
from flask_cors import CORS
import openai
import asyncio
import re
import whisper
import boto3
import pydub
from pydub import playback
import base64
import io
import os
import uuid

app = Flask(__name__, template_folder='templates')
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

messages = [{"role": "system", "content": "You are a helpful assistant."}]

def synthesize_speech(text, output_filename):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        Engine='neural'
    )

    with open(output_filename, 'wb') as f:
        f.write(response['AudioStream'].read())

@app.route('/get_audio_url', methods=['POST'])
def get_audio_url():
    text = request.form['text']
    output_filename = f"response_{uuid.uuid4()}.mp3"
    synthesize_speech(text, output_filename)
    return url_for('static', filename=output_filename)


@app.route('/submit_audio', methods=['POST'])
def submit_audio():
    global messages

    audio_data = base64.b64decode(request.form['audio_data'])
    with open('audio.wav', 'wb') as f:
        f.write(audio_data)

    model = whisper.load_model("base")
    result = model.transcribe("audio.wav")
    user_input = result["text"]
    print(f"You said: {user_input}")

    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\nUser:"],
    )

    bot_response = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": bot_response})

    print("Bot's response:", bot_response)

    synthesize_speech(bot_response, 'response.mp3')

    with open('response.mp3', 'rb') as f:
        audio_data = f.read()

    base64_audio = base64.b64encode(audio_data).decode('utf-8')

    return jsonify({'audio': base64_audio, 'text': bot_response})

@app.route('/submit_text', methods=['POST'])
def submit_text():
    global messages

    user_input = request.form['text']
    print(f"You said: {user_input}")

    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\nUser:"],
    )

    bot_response = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": bot_response})

    print("Bot's response:", bot_response)

    synthesize_speech(bot_response, 'response.mp3')

    with open('response.mp3', 'rb') as f:
        audio_data = f.read()

    base64_audio = base64.b64encode(audio_data).decode('utf-8')

    return jsonify({'audio': base64_audio, 'text': bot_response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
