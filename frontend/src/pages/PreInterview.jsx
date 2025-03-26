import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function PreInterview() {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(true);
  const [speaking, setSpeaking] = useState(false);
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);
  const navigate = useNavigate();
  const hasFetched = useRef(false);

  // Read text aloud
  const speakText = async (text) => {
    if (!text) return;
    setSpeaking(true);
    try {
      await axios.post("http://127.0.0.1:5000/speak", { text });
    } catch (error) {
      console.error("Speech API error:", error);
    }
    setTimeout(() => setSpeaking(false), 3000);
  };

  // Fetch questions when component mounts
  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;
    setLoading(true);

    axios.post("http://127.0.0.1:5000/generate-questions")
      .then((response) => {
        if (response.data.questions && response.data.questions.length > 0) {
          setQuestions(response.data.questions);
          speakText(response.data.questions[0]);
        }
      })
      .catch((error) => console.error("Error fetching questions:", error))
      .finally(() => setLoading(false));
  }, []);

  const handleSpeechRecognition = () => {
    if (!window.SpeechRecognition && !window.webkitSpeechRecognition) {
      alert("Your browser does not support speech recognition.");
      return;
    }
  
    if (!recognitionRef.current) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = true; // ✅ Keeps listening
      recognition.interimResults = false;
      recognition.lang = "en-US";
  
      recognition.onstart = () => setListening(true);
      recognition.onend = () => setListening(false);
  
      recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript;
        setAnswer((prev) => (prev ? `${prev} ${transcript.trim()}` : transcript.trim())); // ✅ Append properly
      };
  
      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setAnswer("⚠️ Speech recognition error.");
      };
  
      recognitionRef.current = recognition;
    }
  
    if (listening) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
    }
  };
  

  const handleNext = () => {
    if (!answer.trim()) return; // Prevent sending empty responses
  
    axios.post("http://127.0.0.1:5000/save-answer", {
      question: questions[currentIndex],
      answer: answer.trim(),
    })
    .then(() => {
      if (currentIndex < questions.length - 1) {
        setCurrentIndex((prevIndex) => prevIndex + 1);
        setAnswer(""); // ✅ Reset answer for next question
        speakText(questions[currentIndex + 1]);
      } else {
        navigate("/results"); // ✅ Redirect to results page
      }
    })
    .catch((error) => {
      console.error("Error saving answer:", error);
      alert("⚠️ Failed to save answer. Please try again.");
    });
  };

  

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-600 p-6">
      <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-md w-full text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">🎤 Pre-Interview Questions</h2>

        {loading ? (
          <p className="text-lg font-semibold text-gray-700">⏳ Processing Resume... Please Wait</p>
        ) : questions.length > 0 ? (
          <p className="text-lg font-semibold text-gray-700">{questions[currentIndex]}</p>
        ) : (
          <p className="text-lg font-semibold text-red-500">⚠️ No questions available. Please check the backend.</p>
        )}

        <div className="w-full p-3 mt-4 border rounded-lg bg-gray-100 text-gray-800 text-lg min-h-[50px]">
          {answer || "Listening... 🎤"}
        </div>

        <button 
          onClick={handleSpeechRecognition} 
          className={`mt-4 px-4 py-2 text-white rounded ${speaking ? "bg-gray-400 cursor-not-allowed" : listening ? "bg-red-500" : "bg-green-500"}`} 
          disabled={speaking}
        >
          {listening ? "🔴 Stop Listening" : "🎙️ Start Listening"}
        </button>

        <button 
          onClick={handleNext} 
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded" 
          disabled={loading}
          >
          {loading ? "⏳ Please Wait" : currentIndex === questions.length - 1 ? "Analyze 🧠" : "Next ➡️"}
          </button>
      </div>
    </div>
  );
}
