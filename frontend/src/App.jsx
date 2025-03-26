import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import JobPortal from "./pages/home.jsx"
import PreInterview from "./pages/PreInterview.jsx";
import Results from "./pages/results.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<JobPortal />} />
        <Route path="/pre-interview" element={<PreInterview />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
}

export default App;
