import { useState } from "react";
import axios from "axios";

export default function JobPortal() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);
  const [resumeName, setResumeName] = useState("📄 Upload Resume");
  const [jdName, setJdName] = useState("📜 Upload Job Description");

  const handleFileChange = (event, setFile, setFileName) => {
    const file = event.target.files[0];
    if (file) {
      setFile(file);
      setFileName(file.name); // Update the label with the selected file name
    }
  };

  const handleUploadResume = async () => {
    if (!resume) {
      alert("Please select a resume file.");
      return;
    }
    const formData = new FormData();
    formData.append("resume", resume);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload-resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Resume uploaded successfully: " + response.data.filename);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Resume upload failed.");
    }
  };

  const handleUploadJD = async () => {
    if (!jd) {
      alert("Please select a job description file.");
      return;
    }
    const formData = new FormData();
    formData.append("jd", jd); 

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload-jd", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Job Description uploaded successfully: " + response.data.filename);
    } catch (error) {
      console.error("Upload failed", error);
      alert("Job Description upload failed.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-600 p-6">
      <div className="bg-white p-10 rounded-3xl shadow-2xl max-w-md w-full text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          🚀 The Tachyons Job Portal
        </h2>

        <div className="space-y-5">
          {/* Resume Upload */}
          <label className="block cursor-pointer border-2 border-dashed border-gray-400 text-gray-700 font-semibold py-3 rounded-lg hover:bg-gray-100 transition">
            <input 
              type="file"
              onChange={(e) => handleFileChange(e, setResume, setResumeName)}
              className="hidden"
            />
            {resumeName}
          </label>
          <button
            onClick={handleUploadResume}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold py-3 rounded-lg hover:scale-105 transition-transform shadow-md"
          >
            Submit Resume
          </button>

          {/* Job Description Upload */}
          <label className="block cursor-pointer border-2 border-dashed border-gray-400 text-gray-700 font-semibold py-3 rounded-lg hover:bg-gray-100 transition">
            <input 
              type="file"
              onChange={(e) => handleFileChange(e, setJd, setJdName)}
              className="hidden"
            />
            {jdName}
          </label>
          <button
            onClick={handleUploadJD}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white font-semibold py-3 rounded-lg hover:scale-105 transition-transform shadow-md"
          >
            Submit Job Description
          </button>

          {/* Proceed Button */}
          <button className="w-full bg-green-500 text-white font-semibold py-3 rounded-lg hover:bg-green-600 transition-transform shadow-lg">
            ➡️ Proceed to Pre-Interview
          </button>
        </div>
      </div>
    </div>
  );
}
