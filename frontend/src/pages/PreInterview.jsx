import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function PreInterview() {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const navigate = useNavigate();
  const hasFetched = useRef(false); // Prevent multiple calls

  const speakText = (text) => {
    if (!text) return; // Prevent speaking empty text
    axios
      .post("http://127.0.0.1:5000/speak", { text })
      .catch((error) => console.error("Speech API error:", error));
  };

  useEffect(() => {
    if (hasFetched.current) return; // Prevent second API call
    hasFetched.current = true;

    axios
      .post("http://127.0.0.1:5000/generate-questions")
      .then((response) => {
        if (response.data.questions) {
          setQuestions(response.data.questions);
        }
      })
      .catch((error) => {
        console.error("Error fetching questions:", error);
      });
  }, []);

  useEffect(() => {
    if (questions.length > 0 && currentIndex < questions.length) {
      speakText(questions[currentIndex]);
    }
  }, [currentIndex, questions]);

  const handleNext = () => {
    if (currentIndex < questions.length - 2) {
      setCurrentIndex((prevIndex) => prevIndex + 2);
    } else {
      alert("End of questions. Good luck!");
      navigate("/");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-600 p-6">
      <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-md w-full text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">🎤 Pre-Interview Questions</h2>

        {questions.length > 0 ? (
          <>
            <p className="text-lg font-semibold text-gray-700">{questions[currentIndex]}</p>
            <button onClick={handleNext} className="w-full mt-6 bg-blue-500 text-white font-semibold py-3 rounded-lg hover:bg-blue-600">
              Next Question ➡️
            </button>
          </>
        ) : (
          <p className="text-gray-500">Loading questions...</p>
        )}
      </div>
    </div>
  );
}
