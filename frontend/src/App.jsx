import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import JobPortal from "./pages/home.jsx"
import PreInterview from "./pages/PreInterview.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<JobPortal />} />
        <Route path="/pre-interview" element={<PreInterview />} />
      </Routes>
    </Router>
  );
}

export default App;
