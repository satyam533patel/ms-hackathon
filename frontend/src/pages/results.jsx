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
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-gray-900 to-black p-6 text-white">
      <h2 className="text-3xl font-bold mb-6">Interview Analysis Results</h2>
      <div className="bg-white/10 backdrop-blur-lg border border-white/20 p-10 rounded-3xl shadow-2xl max-w-md w-full text-center">
        {loading ? (
          <p className="text-lg font-semibold text-gray-300">Calculating Scores... Please Wait</p>
        ) : (
          <div>
            <p className="text-lg font-semibold text-gray-300">Job Fit Score: <span className="text-blue-400">{jobFitScore}</span></p>
            <p className="text-lg font-semibold text-gray-300">HR Evaluation Score: <span className="text-green-400">{hrScore}</span></p>
          </div>
        )}

        <div className="flex flex-col space-y-3 mt-6">
          <button 
            onClick={sendEmail} 
            className="px-3 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition text-m text-bold"
          >
            Send Email to Candidate
          </button>

          {emailSent && <p className="text-green-400 mt-2">Email sent successfully!</p>}
          {emailError && <p className="text-red-400 mt-2">{emailError}</p>}

          <button 
            onClick={() => navigate("/")} 
            className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition text-sm"
          >
            Go to Home
          </button>
        </div>
      </div>
    </div>
  );
}
