import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { UploadOutlined, ArrowRightOutlined, FileTextOutlined } from "@ant-design/icons";

export default function JobPortal() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);
  const [resumeName, setResumeName] = useState("📄 Upload Resume");
  const [jdName, setJdName] = useState("📜 Upload Job Description");
  const navigate = useNavigate();

  const handleFileChange = (event, setFile, setFileName) => {
    const file = event.target.files[0];
    if (file) {
      setFile(file);
      setFileName(file.name);
    }
  };

  const handleUpload = async (file, successMessage, errorMessage) => {
    if (!file) {
      alert("Please select a file before uploading.");
      return;
    }
    const formData = new FormData();
    formData.append("resume", file);

    try {
      await axios.post(`http://127.0.0.1:5000/upload-resume`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert(successMessage);
    } catch (error) {
      console.error("Upload failed", error);
      alert(errorMessage);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-900 text-white">
      {/* Header */}
      <header className="w-full bg-transparent py-4 text-center text-3xl font-semibold text-white">
        The Tachyons Virtual HR
      </header>

      {/* Main Content */}
      <div className="flex-grow flex items-center justify-center p-6">
        <div className="bg-black border border-gray-700 p-10 rounded-xl shadow-lg max-w-3xl w-full text-center">
          <div className="grid grid-cols-2 gap-8 text-left">
            <div>
              <label className="block text-white font-medium mb-2 text-lg">📄 Resume</label>
              <label className="block border-2 border-dashed border-gray-600 text-white/80 py-8 text-lg rounded-lg text-center cursor-pointer hover:border-gray-400 transition">
                <input type="file" onChange={(e) => handleFileChange(e, setResume, setResumeName)} className="hidden" />
                <FileTextOutlined className="mr-2 text-xl" /> {resumeName}
              </label>
              <button onClick={() => handleUpload(resume, "Resume uploaded successfully", "Resume upload failed.")} className="mt-4 w-full bg-gray-800 text-white font-medium py-3 rounded-lg hover:bg-gray-700 transition">
                <UploadOutlined className="mr-2" /> Submit Resume
              </button>
            </div>

            <div>
              <label className="block text-white font-medium mb-2 text-lg">📜 Job Description</label>
              <label className="block border-2 border-dashed border-gray-600 text-white/80 py-8 text-lg rounded-lg text-center cursor-pointer hover:border-gray-400 transition">
                <input type="file" onChange={(e) => handleFileChange(e, setJd, setJdName)} className="hidden" />
                <FileTextOutlined className="mr-2 text-xl" /> {jdName}
              </label>
              <button onClick={() => handleUpload(jd, "upload-jd", "Job Description uploaded successfully", "Job Description upload failed.")} className="mt-4 w-full bg-gray-800 text-white font-medium py-3 rounded-lg hover:bg-gray-700 transition">
                <UploadOutlined className="mr-2" /> Submit Job Description
              </button>
            </div>
          </div>

          <button onClick={() => navigate("/pre-interview")} className="mt-8 w-full bg-green-700 text-white font-medium py-3 rounded-lg hover:bg-green-600 transition">
            ➡️ Proceed to Pre-Interview <ArrowRightOutlined className="ml-2" />
          </button>
        </div>
      </div>
      
      {/* Footer */}
      <footer className="w-full bg-black shadow-md py-4 text-center text-gray-400 text-sm">
        © 2025 Tachyons Job Portal. All Rights Reserved.
      </footer>
    </div>
  );
}