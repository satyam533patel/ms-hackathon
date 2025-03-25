import { useState } from "react";
import axios from "axios";
import JobPortal from "./pages/home.jsx"
function App() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/generate-questions");
      setQuestions(response.data.questions);
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
    setLoading(false);
  };

  return (
    <div>
      {/* <h1>Resume Interview Questions</h1>
      <button onClick={fetchQuestions} disabled={loading}>
        {loading ? "Generating..." : "Generate Questions"}
      </button>
      <ul>
        {questions.map((q, index) => (
          <li key={index}>{q}</li>
        ))}
      </ul> */}
      JobPortal
    </div>
  );
}

export default App;
