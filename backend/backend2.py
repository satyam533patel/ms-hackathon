import requests
import json
import time

# Azure API Endpoint (Replace with actual key)
endpoint = "https://ai-aihackthonhub282549186415.services.ai.azure.com/"
api_key = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"

# URL for Document Intelligence API
form_recognizer_url = f"{endpoint}formrecognizer/documentModels/prebuilt-layout:analyze?api-version=2023-07-31"

# Headers for authentication
headers = {
    "Content-Type": "application/pdf",
    "Ocp-Apim-Subscription-Key": api_key
}

def extract_resume_text(pdf_path="resume2.pdf"):
    """Extract text from resume PDF using Azure API."""
    with open(pdf_path, "rb") as file:
        pdf_data = file.read()

    response = requests.post(form_recognizer_url, headers=headers, data=pdf_data)

    if response.status_code == 202:
        operation_url = response.headers["Operation-Location"]
        print("Processing document...")

        while True:
            result_response = requests.get(operation_url, headers={"Ocp-Apim-Subscription-Key": api_key})
            result_data = result_response.json()

            if result_data.get("status") == "succeeded":
                print("Processing complete!")
                return result_data["analyzeResult"]["content"]
            elif result_data.get("status") == "failed":
                print("Processing failed!")
                return None
            time.sleep(5)

    else:
        print("Error:", response.json())
        return None
