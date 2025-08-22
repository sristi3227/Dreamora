import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

CORS(app)  # or CORS(app, origins=["https://your-netlify-site.netlify.app"])


load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/generate", methods=["POST"])
def generate_story():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"story": "Prompt is empty"}), 400

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a creative storyteller that writes alternate history stories."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        story = result['choices'][0]['message']['content']
        return jsonify({"story": story})
    else:
        return jsonify({"story": "Failed to generate story"}), 500

@app.route("/")
def home():
    return jsonify({"message": "Groq-powered History Simulator API is running!"})

if __name__ == "__main__":
    app.run(debug=True)
