from flask import Flask, request, jsonify
from flask_cors import CORS
import backend2  # Import your existing resume processing logic
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

# Define API details
API_ENDPOINT = "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview"
API_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    extracted_data = backend2.extract_resume_text()

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

if __name__ == '__main__':
    app.run(debug=True)
