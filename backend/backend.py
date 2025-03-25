from flask import Flask, request, jsonify
from flask_cors import CORS
import backend2  # Import your resume processing logic
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all requests

# Define upload folder inside backend/
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# OpenAI API details
API_ENDPOINT = "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview"
API_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

# Store uploaded filenames globally
uploaded_resume = None
uploaded_jd = None


@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    """Endpoint to upload a resume (PDF)."""
    global uploaded_resume  

    if "resume" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".pdf"):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        uploaded_resume = file_path  # ✅ Fixed variable name

        return jsonify({"message": "Resume uploaded successfully", "filename": file.filename}), 200

    return jsonify({"error": "Invalid file type"}), 400


@app.route("/upload-jd", methods=["POST"])
def upload_jd():
    """Endpoint to upload a job description (PDF)."""
    global uploaded_jd  

    if "jd" not in request.files:  # ✅ Fix: Ensure correct key from frontend
        return jsonify({"error": "No file part"}), 400

    file = request.files["jd"]  # ✅ Fix: Use correct key
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".pdf"):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        uploaded_jd = file_path  # ✅ Fixed variable name

        return jsonify({"message": "Job Description uploaded successfully", "filename": file.filename}), 200

    return jsonify({"error": "Invalid file type"}), 400


@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    """Generate interview questions based on extracted resume data."""
    global uploaded_resume
    if not uploaded_resume:
        return jsonify({"error": "No resume uploaded"}), 400

    # Extract resume text from the uploaded file
    extracted_data = backend2.extract_resume_text(uploaded_resume)

    if not extracted_data:
        return jsonify({"error": "Failed to extract resume data"}), 400

    # Prepare prompt
    rq_data = extracted_data + " Based on the projects mentioned in this resume, list three short questions to ask as an interviewer."

    # Prepare API request payload
    payload = {
        "messages": [{"role": "system", "content": "You are an HR assistant"},
                     {"role": "user", "content": rq_data}],
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Make request to OpenAI API
    response = requests.post(API_ENDPOINT, headers=headers, json=payload)
    response_json = response.json()

    if "choices" in response_json and len(response_json["choices"]) > 0:
        questions_text = response_json["choices"][0]["message"]["content"]
        questions_list = questions_text.strip().split("\n")
        return jsonify({"questions": questions_list})

    return jsonify({"error": "No questions found in the response."}), 500


if __name__ == "__main__":
    app.run(debug=True)
