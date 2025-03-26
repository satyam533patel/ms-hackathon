# Tachyons Virtual HR  
🚀 Built for [Hackathon Name] - [Year]

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

Satyam Patel (2201CS64)
Rahul Chandu Nikhate (2201CS57)
Harsh Kumar (2201AI14)
Saumya Pratap Singh (2201AI35)

