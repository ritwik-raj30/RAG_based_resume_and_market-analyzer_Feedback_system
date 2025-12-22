// import React, { useState } from 'react';
// import { useNavigate, Link } from 'react-router-dom';
// import { axiosInstance } from '../lib/axios';
// import { useAuthStore } from '../store/useAuthStore';
// import toast from 'react-hot-toast';
// import { motion } from 'framer-motion';

// const UploadView = () => {
//   const [resumeFile, setResumeFile] = useState(null);
//   const [driveUrl, setDriveUrl] = useState('');
//   const [jobDescription, setJobDescription] = useState('');
//   const [isSubmitting, setIsSubmitting] = useState(false);
//   const navigate = useNavigate();
//   const { logout, authUser } = useAuthStore();

//   const demoJD = `We are looking for a passionate JavaScript Developer Intern to join our front-end engineering team focused on building modern, responsive web applications. You will work with React, REST APIs, and collaborate with designers and product managers to build features users love.`;

//   const handleUseDemo = async () => {
//     try {
//       const res = await fetch('/demoResume.pdf');
//       const blob = await res.blob();
//       const file = new File([blob], 'demo_resume.pdf', { type: 'application/pdf' });
//       setResumeFile(file);
//       setJobDescription(demoJD);
//       toast.success('Demo resume and JD loaded!');
//     } catch (err) {
//       toast.error('Failed to load demo resume.');
//     }
//   };

//   const handleSubmit = async () => {
//     if (!resumeFile && !driveUrl.trim()) {
//       return toast.error('Please upload a resume or provide a Drive link.');
//     }

//     if (!jobDescription) {
//       return toast.error('Please enter a job description.');
//     }

//     const formData = new FormData();
//     if (resumeFile) formData.append('file', resumeFile);
//     formData.append('drive_url', driveUrl.trim());
//     formData.append('jd_text', jobDescription);

//     try {
//       setIsSubmitting(true);
//       const res = await axiosInstance.post('/resume/upload-resume-analyze', formData, {
//         headers: { 'Content-Type': 'multipart/form-data' }
//       });
//       toast.success('Analysis complete!');
//       navigate('/results', { state: res.data });
//     } catch (error) {
//       toast.error(error?.response?.data?.detail || 'Upload failed');
//     } finally {
//       setIsSubmitting(false);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-tr from-lime-100 to-green-50 flex items-center justify-center px-4 py-12">
//       <motion.div
//         initial={{ y: 100, opacity: 0 }}
//         animate={{ y: 0, opacity: 1 }}
//         transition={{
//           type: "spring",
//           stiffness: 70,
//           damping: 14,
//           duration: 0.6,
//         }}
//         className="w-full max-w-2xl bg-white/90 backdrop-blur-md border border-white/30 shadow-xl rounded-2xl px-8 py-10"
//       >
//         <div className="flex items-center justify-between mb-6">
//           <h2 className="text-3xl font-extrabold text-green-900">Upload Resume & JD</h2>
//           {authUser && (
//             <button
//               onClick={logout}
//               className="bg-green-700 text-white px-5 py-2 rounded-md text-sm font-semibold hover:bg-green-800 transition"
//             >
//               Logout
//             </button>
//           )}
//         </div>

//         <p className="text-sm text-gray-700 mb-5">
//           Upload your resume or{' '}
//           <button
//             onClick={handleUseDemo}
//             className="text-green-700 font-semibold underline hover:text-green-900"
//           >
//             use demo resume & JD
//           </button>
//         </p>

//         <div className="space-y-4">
//           <input
//             type="file"
//             accept=".pdf"
//             onChange={(e) => setResumeFile(e.target.files[0])}
//             className="w-full border border-green-300 rounded-lg px-4 py-3 text-sm bg-white shadow-inner focus:outline-none focus:ring-2 focus:ring-green-400"
//           />
//           {resumeFile && (
//             <p className="text-sm text-gray-600">
//               Selected file: <strong>{resumeFile.name}</strong>
//             </p>
//           )}

//           <input
//             type="url"
//             placeholder="Paste Google Drive link"
//             value={driveUrl}
//             onChange={(e) => setDriveUrl(e.target.value)}
//             className="w-full border border-green-300 rounded-lg px-4 py-3 text-sm shadow-inner focus:outline-none focus:ring-2 focus:ring-green-400"
//           />

//           <textarea
//             value={jobDescription}
//             onChange={(e) => setJobDescription(e.target.value)}
//             placeholder="Paste job description here..."
//             rows={6}
//             className="w-full border border-green-300 rounded-lg px-4 py-3 text-sm resize-y shadow-inner focus:outline-none focus:ring-2 focus:ring-green-400"
//           />
//         </div>

//         <button
//           onClick={handleSubmit}
//           disabled={isSubmitting}
//           className={`mt-6 w-full py-3 text-white font-bold rounded-lg transition-all duration-300 ${
//             isSubmitting
//               ? 'bg-green-300 cursor-not-allowed'
//               : 'bg-green-700 hover:bg-green-800 shadow-md'
//           }`}
//         >
//           {isSubmitting ? 'Analyzing...' : 'Submit'}
//         </button>

//         <Link
//           to="/getme"
//           className="block text-center mt-6 text-green-700 underline font-semibold text-sm hover:text-green-900"
//         >
//           View Past Results
//         </Link>
//       </motion.div>
//     </div>
//   );
// };

// export default UploadView;
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { axiosInstance } from '../lib/axios';
import { useAuthStore } from '../store/useAuthStore';
import toast from 'react-hot-toast';
import { motion } from 'framer-motion';
import { Upload, FileText, Building2, Globe, Sparkles } from 'lucide-react';

const UploadView = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [driveUrl, setDriveUrl] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [companyUrl, setCompanyUrl] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  const { logout, authUser } = useAuthStore();

  const demoJD = `We are looking for a passionate JavaScript Developer Intern to join our front-end engineering team focused on building modern, responsive web applications. You will work with React, REST APIs, and collaborate with designers and product managers to build features users love.`;

  const handleUseDemo = async () => {
    try {
      const res = await fetch('/demoResume.pdf');
      const blob = await res.blob();
      const file = new File([blob], 'demo_resume.pdf', { type: 'application/pdf' });
      setResumeFile(file);
      setJobDescription(demoJD);
      setCompanyName('netflix');
      setCompanyUrl('https://explore.jobs.netflix.net/careers');
      toast.success('Demo resume and JD loaded!');
    } catch (err) {
      console.error('demo load error', err);
      toast.error('Failed to load demo resume.');
    }
  };

  const handleSubmit = async () => {
    if (!resumeFile && !driveUrl.trim()) {
      return toast.error('Please upload a resume or provide a Drive link.');
    }

    if (!jobDescription.trim()) {
      return toast.error('Please enter a job description.');
    }

    const formData = new FormData();
    // field names must match your FastAPI signatures
    if (resumeFile) formData.append('file', resumeFile);
    formData.append('drive_url', driveUrl.trim() || '');
    formData.append('jd_text', jobDescription.trim());
    formData.append('company_name', companyName.trim() || '');
    formData.append('company_url', companyUrl.trim() || '');

    try {
      setIsSubmitting(true);

      // POST to the endpoint that your FastAPI router exposes.
      // Your backend route is mounted at /resume/upload-resume-analyze
      const res = await axiosInstance.post('/resume/upload-resume-analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // optional: inspect server response shape
      console.log('Upload response:', res?.data);
      toast.success('Analysis complete!');
      navigate('/results', { state: res.data });
    } catch (error) {
      console.error('Upload error:', error);

      // friendly error resolution
      const serverMessage =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        error?.response?.data ||
        error?.message ||
        'Upload failed';

      toast.error(serverMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 flex items-center justify-center px-4 py-12">
      <motion.div
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{
          type: "spring",
          stiffness: 70,
          damping: 14,
          duration: 0.6,
        }}
        className="w-full max-w-3xl bg-white/95 backdrop-blur-md border border-emerald-200/50 shadow-2xl rounded-3xl px-10 py-12"
      >
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-emerald-500 to-teal-600 p-3 rounded-xl shadow-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-3xl font-extrabold text-gray-900">AI Resume Analyzer</h2>
              <p className="text-sm text-gray-600">Powered by RAG & LLM Technology</p>
            </div>
          </div>
          {authUser && (
            <button
              onClick={logout}
              className="bg-gray-700 text-white px-5 py-2 rounded-lg text-sm font-semibold hover:bg-gray-800 transition shadow-md"
            >
              Logout
            </button>
          )}
        </div>

        <div className="mb-6 p-4 bg-emerald-50 border border-emerald-200 rounded-xl">
          <p className="text-sm text-gray-700 mb-2">
            <span className="font-semibold">New to this?</span> Try our demo to see how it works!
          </p>
          <button
            onClick={handleUseDemo}
            className="text-emerald-700 font-semibold underline hover:text-emerald-900 text-sm"
          >
            Load Demo Resume & JD
          </button>
        </div>

        <div className="space-y-5">
          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
              <Upload className="w-4 h-4 text-emerald-600" />
              Upload Resume (PDF)
            </label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResumeFile(e.target.files[0])}
              className="w-full border-2 border-emerald-200 rounded-xl px-4 py-3 text-sm bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent transition"
            />
            {resumeFile && (
              <p className="text-sm text-emerald-700 mt-2 flex items-center gap-2">
                <FileText className="w-4 h-4" />
                Selected: <strong>{resumeFile.name}</strong>
              </p>
            )}
          </div>

          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
              <Globe className="w-4 h-4 text-blue-600" />
              Or Paste Google Drive Link
            </label>
            <input
              type="url"
              placeholder="https://drive.google.com/file/d/..."
              value={driveUrl}
              onChange={(e) => setDriveUrl(e.target.value)}
              className="w-full border-2 border-emerald-200 rounded-xl px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent transition"
            />
          </div>

          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
              <FileText className="w-4 h-4 text-purple-600" />
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here..."
              rows={6}
              className="w-full border-2 border-emerald-200 rounded-xl px-4 py-3 text-sm resize-y shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent transition"
            />
          </div>

          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
              <Building2 className="w-4 h-4 text-orange-600" />
              Company Name <span className="text-gray-400 font-normal">(Optional - for RAG)</span>
            </label>
            <input
              type="text"
              placeholder="e.g., Google, Microsoft, TechCorp"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="w-full border-2 border-emerald-200 rounded-xl px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent transition"
            />
          </div>

          <div>
            <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
              <Globe className="w-4 h-4 text-teal-600" />
              Company Website URL <span className="text-gray-400 font-normal">(Optional - for RAG)</span>
            </label>
            <input
              type="url"
              placeholder="https://company.com"
              value={companyUrl}
              onChange={(e) => setCompanyUrl(e.target.value)}
              className="w-full border-2 border-emerald-200 rounded-xl px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent transition"
            />
            <p className="text-xs text-gray-500 mt-1">
              💡 Providing company URL enables AI to analyze company culture and provide deeper insights
            </p>
          </div>
        </div>

        <button
          onClick={handleSubmit}
          disabled={isSubmitting}
          className={`mt-8 w-full py-4 text-white font-bold rounded-xl transition-all duration-300 shadow-lg flex items-center justify-center gap-2 ${
            isSubmitting
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 hover:shadow-xl transform hover:-translate-y-0.5'
          }`}
        >
          {isSubmitting ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Analyzing with AI...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Analyze with RAG AI
            </>
          )}
        </button>

        <Link
          to="/getme"
          className="block text-center mt-6 text-emerald-700 underline font-semibold text-sm hover:text-emerald-900 transition"
        >
          View Past Analysis Results
        </Link>
      </motion.div>
    </div>
  );
};

export default UploadView;
