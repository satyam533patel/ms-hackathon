from flask import Flask, request, jsonify
from flask_cors import CORS
import backend2  # Resume processing logic
import requests
import os
import json
from speaker import synthesize_speech
from speech import recognize_from_microphone

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all requests

# Create necessary folders
BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESPONSES_FOLDER = os.path.join(BASE_DIR, "responses")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESPONSES_FOLDER, exist_ok=True)

RESPONSES_FILE = os.path.join(RESPONSES_FOLDER, "answers.json")

# OpenAI API details
API_ENDPOINT = "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview"
API_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

uploaded_resume = None
uploaded_jd = None

@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    global uploaded_resume  
    file = request.files.get("resume")

    if not file or not file.filename:
        return jsonify({"error": "No file uploaded"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Invalid file type. Please upload a PDF file."}), 400

    file_path = os.path.join(UPLOAD_FOLDER, "resume.pdf")
    
    try:
        file.save(file_path)
        uploaded_resume = file_path
        return jsonify({"message": "Resume uploaded successfully", "filename": "resume.pdf"}), 200
    except Exception as e:
        return jsonify({"error": f"File upload failed: {str(e)}"}), 500

@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    global uploaded_resume
    if not uploaded_resume:
        print("❌ No resume uploaded!")  # Debugging
        return jsonify({"error": "No resume uploaded"}), 400

    extracted_data = backend2.extract_resume_text(uploaded_resume)
    if not extracted_data.strip():
        print("❌ Resume extraction failed!")  # Debugging
        return jsonify({"error": "Failed to extract resume data"}), 400

    print("✅ Resume extracted successfully:", extracted_data[:100])  # Print first 100 characters

    prompt = f"{extracted_data} Based on the projects mentioned, list three short questions an interviewer might ask."
    payload = {
        "messages": [
            {"role": "system", "content": "You are an HR assistant"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response_json = response.json()
        print("🔄 OpenAI Response:", response_json)  # Debugging API Response

        if "choices" in response_json and response_json["choices"]:
            content = response_json["choices"][0].get("message", {}).get("content", "").strip()
            questions = [q.strip() for q in content.split("\n") if q.strip()]
            
            if questions:
                return jsonify({"questions": questions}), 200
    except Exception as e:
        print("🔥 OpenAI API Request Failed:", str(e))  # Debugging
        return jsonify({"error": f"OpenAI API request failed: {str(e)}"}), 500

    return jsonify({"error": "No questions found"}), 500

@app.route("/save-answer", methods=["POST"])
def save_answer():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Missing question or answer"}), 400

    try:
        os.makedirs(RESPONSES_FOLDER, exist_ok=True)  # Ensure folder exists

        responses = []
        if os.path.exists(RESPONSES_FILE):
            with open(RESPONSES_FILE, "r") as f:
                try:
                    responses = json.load(f)
                except json.JSONDecodeError:
                    responses = []

        responses.append({"question": question, "answer": answer})

        with open(RESPONSES_FILE, "w") as f:  # Open in write mode after reading
            json.dump(responses, f, indent=4)

        return jsonify({"message": "Answer saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to save answer: {str(e)}"}), 500

@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        synthesize_speech(text)
        return jsonify({"message": "Speech synthesis completed"}), 200
    except Exception as e:
        return jsonify({"error": f"Speech synthesis failed: {str(e)}"}), 500

@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    """Convert speech to text and return the recognized speech"""
    try:
        recognized_text = recognize_from_microphone()
        if not recognized_text:
            return jsonify({"error": "No speech detected"}), 400
        return jsonify({"text": recognized_text}), 200
    except Exception as e:
        return jsonify({"error": f"Speech recognition error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
