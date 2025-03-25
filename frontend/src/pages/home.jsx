export default function JobPortal() {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-600 to-blue-600 p-4">
        <div className="bg-white p-8 rounded-2xl shadow-lg max-w-md w-full text-center">
          <div className="bg-gray-200 text-gray-900 font-bold text-xl py-3 rounded-t-lg">
            The Tachyons Job Portal
          </div>
          <div className="py-6 space-y-4">
            <button className="w-full border-2 border-dashed border-gray-400 text-black font-semibold py-3 rounded-lg hover:bg-gray-100 transition">
              Upload Resume
            </button>
            <button className="w-full border-2 border-dashed border-gray-400 text-black font-semibold py-3 rounded-lg hover:bg-gray-100 transition">
              Upload Job Description
            </button>
            <button className="w-full bg-blue-500 text-white font-semibold py-3 rounded-lg hover:bg-blue-600 transition">
              Proceed to Pre-Interview
            </button>
          </div>
        </div>
      </div>
    );
  }
  