# Tachyons Virtual HR  
🚀 Built for Microsoft Azure - 2025

## 📌 Overview
Tachyons Virtual HR is an AI-powered pre-screening system designed to automate the candidate evaluation process. It analyzes resumes, evaluates technical and HR-based responses, generates scores, and sends candidates their results via email. The system also logs all applicant data for future reference.


## 🚀 Features
- 📄 Resume Parsing: Extracts text from uploaded PDF resumes.
- 🎯 Job Fit Analysis: Compares resume content with a Job Description (JD) and assigns a fitness score (out of 100).
- 📝 Questionnaire: Asks 3 project & technical questions and 2 HR-based questions.
- 📊 Evaluation: Calls an AI-powered API to rate answers and generate an HR score (out of 100).
- 📩 Email Notification: Sends automated emails informing candidates of their results.
- 📂 Data Storage: Saves each candidate’s Name, Email, HR Score, Resume Fit Score, and Selection Status in an Excel file for future reference.

## 🏗️ Tech Stack

## Workflow

### Resume Upload
The applicant uploads their resume (PDF format).
The system stores the resume and extracts relevant text data for further analysis.
![image](https://github.com/user-attachments/assets/39f2c3aa-d545-4377-aaab-653b088bf8bd)

### Job Description Input
HR provides the job description (JD) for the role.
The system uses the JD and the extracted resume data to assess the applicant's suitability.
### Question Generation
The system analyzes the resume content and generates interview questions tailored to the applicant’s skills and experience.
HR can review, edit, or approve the generated questions before proceeding.
![image](https://github.com/user-attachments/assets/03c61292-0ca7-4eec-b678-82660ff7dbcf)

### Answer Collection
The applicant provides responses to the generated questions.
Responses are recorded and stored for evaluation.
### Job Fit Score Calculation
The system compares the resume content with the provided JD.
A job fit score (out of 100) is calculated using AI-driven analysis.
### HR Score Evaluation
The system evaluates the applicant’s answers for correctness and relevance.
A final HR score (out of 100) is generated to assess the quality of responses.
### Final Assessment & Email Notification
A final score is computed using the Job Fit Score and HR Score.
If the applicant meets the required threshold, they are shortlisted.
The system extracts the applicant’s email address and notifies them of the results.
![image](https://github.com/user-attachments/assets/bb09e3b3-f4bd-40f5-a2cf-fc76f1fa57fc)


### Backend:

- Flask - Web framework
- OpenAI API (Azure) - AI-based scoring
- Pandas - Data management (Excel handling)
- smtplib - Email notifications
- PyPDF2 - PDF parsing (Resume & JD extraction)

### Frontend:

- React.js (Vite) - UI framework
- Axios - API calls to backend
- Tailwind CSS - Styling

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```
git clone https://github.com/your-repo/tachyons-virtual-hr.git
cd tachyons-virtual-hr

```
### 2️⃣ Backend Setup
```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python backend.py

```

### 3️⃣ Frontend Setup
```
cd frontend
npm install
npm run dev

```

## 📌 Usage

- Upload Resume & JD (PDF format).
- Answer the generated questions.
- Get HR & Resume Fit Scores.
- Receive email confirmation of results.
- Data stored in insights.xlsx for record-keeping.


## 🏆 Team Members

- Satyam Patel (2201CS64)
- Rahul Chandu Nikhate (2201CS57)
- Harsh Kumar (2201AI14)
- Saumya Pratap Singh (2201AI35)

