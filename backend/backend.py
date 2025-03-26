from flask import Flask, request, jsonify
from flask_cors import CORS
import backend2  # Resume processing logic
import requests
import os
import json
import jd
from speaker import synthesize_speech
from speech import recognize_from_microphone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
extracted_resume=""
job_desc=jd.jd
jobScore= 65
hrScore=65
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
    extratracted_resume=extracted_data
    prompt = f"{extracted_data} Based on the projects mentioned, list 2 short questions an interviewer might ask."
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
@app.route("/job-fit-score", methods=["POST"])
def job_fit_score():
    """Calculate job fit score based on the extracted resume and job description."""
    uploaded_resume = os.path.join(UPLOAD_FOLDER, "resume.pdf")
    global extracted_resume, job_desc, jobScore

    if not uploaded_resume:
        return jsonify({"error": "No resume uploaded"}), 400  # Handle missing resume

    extracted_resume = backend2.extract_resume_text(uploaded_resume)
    print(extracted_resume)
    if not extracted_resume.strip():
        return jsonify({"error": "Failed to extract resume data"}), 400  # Handle empty extraction

    prompt = f"Given the following job description: {job_desc} and this resume: {extracted_resume}, rate the resume's fit for the job on a scale from 1 to 100. Only return the score."

    payload = {
        "messages": [
            {"role": "system", "content": "You are an expert HR assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response_json = response.json()

        if "choices" in response_json and response_json["choices"]:
            score_text = response_json["choices"][0].get("message", {}).get("content", "").strip()
            score = int("".join(filter(str.isdigit, score_text)))  # Extract numerical score
            jobScore = score
            return jsonify({"job_fit_score": score}), 200
    except Exception as e:
        return jsonify({"error": f"OpenAI API request failed: {str(e)}"}), 500

    return jsonify({"error": "Failed to retrieve job fit score"}), 500
@app.route("/hr-score", methods=["POST"])
def hr_score():
    global hrScore
    responses_file = os.path.join(os.getcwd(), "responses", "answers.json")
    if not os.path.exists(responses_file):
        return jsonify({"error": "No saved answers found"}), 400
    
    try:
        with open(responses_file, "r") as f:
            responses = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse answers.json"}), 500
    
    if not responses:
        return jsonify({"error": "No answers to evaluate"}), 400
    
    prompt = "Analyze the correctness and relevance of the following answers based on the given questions and rate the overall performance on a scale from 1 to 100. Only return the score.\n\n"
    
    for qa in responses:
        prompt += f"Question: {qa['question']}\nAnswer: {qa['answer']}\n\n"
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are an expert HR evaluator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response_json = response.json()
        
        if "choices" in response_json and response_json["choices"]:
            score_text = response_json["choices"][0].get("message", {}).get("content", "").strip()
            score = int("".join(filter(str.isdigit, score_text)))  # Extract numerical score
            hrScore= score
            return jsonify({"hr_score": score}), 200
    except Exception as e:
        return jsonify({"error": f"OpenAI API request failed: {str(e)}"}), 500
    
    return jsonify({"error": "Failed to retrieve HR score"}), 500

@app.route('/sendMail', methods=['POST'])
def send_email():
    global uploaded_resume
    if not uploaded_resume:
        return jsonify({"error": "No resume uploaded"}), 400

    extracted_data = backend2.extract_resume_text(uploaded_resume)
    rq_data = extracted_data + "From this data, extract and return the candidate email. In response, give me the email only, and not a single word extra."

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

    try:
        # Make request to OpenAI API
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response_json = response.json()
        print(response_json)
        candidate_email = response_json['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({"error": "Failed to extract candidate email", "details": str(e)}), 500

    from_email = "hootiitp@gmail.com"
    password = "lebx hxtc yzag umal"  # Use environment variables for security
    
    subject = "Job Application Received"
    totalScore = (2 * jobScore + hrScore) / 3
    
    if totalScore > 60:
        body = "Dear Candidate, Thank You for submitting your response. We are glad to inform you that you have been shortlisted for interviews.\n\nBest Regards,\nHR Team"
    else:
        body = "Dear Candidate, Thank You for submitting your response. After careful consideration, we have decided not to move forward with your application.\n\nBest Regards,\nHR Team"

    # Set up email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = candidate_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to SMTP server (Gmail SMTP used here)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, candidate_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to send email", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
