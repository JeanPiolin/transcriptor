from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Pon aquí tu API Key de OpenAI (mantenla secreta)
OPENAI_API_KEY = "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"

@app.route('/')
def index():
    return 'Servidor API Whisper activo'

@app.route('/transcribir', methods=['POST'])
def transcribir():
    if 'audio' not in request.files:
        return jsonify({"error": "No se encontró archivo de audio"}), 400

    audio_file = request.files['audio']

    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        },
        files={
            "file": (audio_file.filename, audio_file, audio_file.content_type)
        },
        data={
            "model": "whisper-1",
            "language": "es"
        }
    )

    if response.status_code != 200:
        return jsonify({"error": "Error en la transcripción", "detalle": response.text}), 500

    text = response.json().get("text", "")

    return jsonify({"transcripcion": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
