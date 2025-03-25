import requests
import json
import backend2  # Import the module

# Extract resume text
extracted_data = backend2.extract_resume_text()

if extracted_data is None:
    print("Failed to extract resume data.")
    exit()

# Define API details
API_ENDPOINT = "https://ai-aihackthonhub282549186415.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2025-01-01-preview"
API_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Prepare prompt
rq_data = extracted_data + " Based on the projects mentioned in this resume, list three short questions to ask as an interviewer."

# Payload for the request
payload = {
    "messages": [{"role": "system", "content": "You are an HR assistant"},
                 {"role": "user", "content": rq_data}],
    "temperature": 0.7
}

# Making the request
response = requests.post(API_ENDPOINT, headers=headers, json=payload)

# Extract the JSON response
response_json = response.json()

# Extracting questions from response
if "choices" in response_json and len(response_json["choices"]) > 0:
    questions_text = response_json["choices"][0]["message"]["content"]
    questions_list = questions_text.strip().split("\n")  # Split into list
    print("Extracted Questions:")
    for question in questions_list:
        print(question.strip())  # Print each extracted question
else:
    print("No questions found in the response.")
