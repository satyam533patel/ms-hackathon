import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Results() {
  const [jobFitScore, setJobFitScore] = useState(null);
  const [hrScore, setHrScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [emailSent, setEmailSent] = useState(false);
  const [emailError, setEmailError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchScores = async () => {
      try {
        const jobFitResponse = await axios.post("http://127.0.0.1:5000/job-fit-score");
        const hrScoreResponse = await axios.post("http://127.0.0.1:5000/hr-score");
        
        setJobFitScore(jobFitResponse.data.job_fit_score);
        setHrScore(hrScoreResponse.data.hr_score);
      } catch (error) {
        console.error("Error fetching scores:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchScores();
  }, []);

  const sendEmail = async () => {
    setEmailError(null);
    setEmailSent(false);
    try {
      const response = await axios.post("http://127.0.0.1:5000/sendMail");
      if (response.status === 200) {
        setEmailSent(true);
      }
    } catch (error) {
      setEmailError("Failed to send email. Please try again.");
      console.error("Email error:", error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-600 p-6">
      <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-md w-full text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">📊 Interview Analysis Results</h2>
        
        {loading ? (
          <p className="text-lg font-semibold text-gray-700">⏳ Calculating Scores... Please Wait</p>
        ) : (
          <div>
            <p className="text-lg font-semibold text-gray-700">💼 Job Fit Score: <span className="text-blue-500">{jobFitScore}</span></p>
            <p className="text-lg font-semibold text-gray-700">🤖 HR Evaluation Score: <span className="text-green-500">{hrScore}</span></p>
          </div>
        )}

        <button 
          onClick={sendEmail} 
          className="mt-6 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
        >
          📧 Send Email to Candidate
        </button>

        {emailSent && <p className="text-green-600 mt-2">✅ Email sent successfully!</p>}
        {emailError && <p className="text-red-600 mt-2">❌ {emailError}</p>}

        <button 
          onClick={() => navigate("/")} 
          className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          🏠 Go to Home
        </button>
      </div>
    </div>
  );
}
