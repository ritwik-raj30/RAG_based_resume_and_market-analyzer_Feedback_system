import React from 'react';
import { useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Info, 
  CheckCircle, 
  ExternalLink, 
  Sparkles, 
  Building2, 
  Brain, 
  Target 
} from 'lucide-react';

const ResultView = () => {
  const location = useLocation();
  const resultData = location.state;

  const hybridScore = resultData?.hybridScore ?? resultData?.scores?.hybridScore ?? 0;
  const skillScore = resultData?.skillScore ?? resultData?.scores?.skillScore ?? null;
  const bertScore = resultData?.bertScore ?? resultData?.scores?.bertScore ?? null;
  const tfidfScore = resultData?.tfidfScore ?? resultData?.scores?.tfidfScore ?? null;

  // Extract RAG data
  const ragData = resultData?.ragData || {};
  const ragEnabled = ragData?.ragEnabled || false;
  const feedbackType = resultData?.aiFeedback?.feedbackType || 'Rule-Based';
  const companyName = resultData?.companyName || 'N/A';
  const companyUrl = resultData?.companyUrl || null;

  // NEW FIELD → strict validation flag
  const strictValidation = resultData?.strictValidation ?? false;

  // Process AI Feedback
  let aiFeedback = '';
  if (resultData?.aiFeedback) {
    if (typeof resultData.aiFeedback === 'object' && resultData.aiFeedback.feedback) {
      aiFeedback = Array.isArray(resultData.aiFeedback.feedback)
        ? resultData.aiFeedback.feedback.join('. ')
        : resultData.aiFeedback.feedback;
    } else if (Array.isArray(resultData.aiFeedback)) {
      aiFeedback = resultData.aiFeedback.join('. ');
    } else if (typeof resultData.aiFeedback === 'string') {
      aiFeedback = resultData.aiFeedback.trim();
    }
  }

  const aiFeedbackList = aiFeedback
    ? aiFeedback
        .split(/\d+\.\s*\*\*|\*\*\d+\.\s*|\n\d+\.\s*|(?<=\.)\s*\*\*/)
        .map(item => item.replace(/\*\*/g, '').trim())
        .filter(item => item.length > 10)
    : [];

  let feedbackText = '';
  let scoreColor = 'text-gray-600';
  let scoreGradient = 'from-gray-400 to-gray-500';

  if (hybridScore <= 40) {
    feedbackText = 'Poor Match';
    scoreColor = 'text-red-600';
    scoreGradient = 'from-red-500 to-rose-600';
  } else if (hybridScore <= 55) {
    feedbackText = 'Average Match';
    scoreColor = 'text-yellow-600';
    scoreGradient = 'from-yellow-500 to-amber-600';
  } else if (hybridScore <= 80) {
    feedbackText = 'Above Average Match';
    scoreColor = 'text-blue-600';
    scoreGradient = 'from-blue-500 to-indigo-600';
  } else {
    feedbackText = 'Excellent Match';
    scoreColor = 'text-green-700';
    scoreGradient = 'from-emerald-500 to-teal-600';
  }

  if (!resultData) {
    return (
      <div className="text-center text-red-600 font-bold mt-16">
        No result data found.
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-gradient-to-br from-slate-50 via-gray-50 to-zinc-50 font-sans">

      {/* LEFT SIDE - Explanation Panel */}
      <motion.div
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="lg:w-[45%] lg:fixed lg:left-0 lg:top-0 lg:h-screen overflow-y-auto p-8 bg-white/90 backdrop-blur-lg shadow-lg"
      >
        <div className="max-w-xl mx-auto space-y-6">

          <div className="flex items-center gap-3 mb-6">
            <div className="bg-gradient-to-br from-purple-500 to-indigo-600 p-3 rounded-xl shadow-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900">
              How We Evaluate
            </h2>
          </div>

          <div className="space-y-4 text-sm text-gray-800">

            <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded-lg">
              <p className="flex gap-2 items-start">
                <Target className="w-5 h-5 mt-1 text-blue-600" />
                <span>
                  <strong className="text-blue-900">Skill Matching (40%):</strong> 
                  Measures how many job-relevant skills your resume includes.
                </span>
              </p>
            </div>

            <div className="p-4 bg-purple-50 border-l-4 border-purple-500 rounded-lg">
              <p className="flex gap-2 items-start">
                <Info className="w-5 h-5 mt-1 text-purple-600" />
                <span>
                  <strong className="text-purple-900">TF-IDF (30%):</strong> 
                  Identifies important and unique terms relevant to the job.
                </span>
              </p>
            </div>

            <div className="p-4 bg-emerald-50 border-l-4 border-emerald-500 rounded-lg">
              <p className="flex gap-2 items-start">
                <Brain className="w-5 h-5 mt-1 text-emerald-600" />
                <span>
                  <strong className="text-emerald-900">BERT Score (30%):</strong> 
                  Measures semantic meaning match between resume & job.
                </span>
              </p>
            </div>

            {ragEnabled && (
              <div className="p-4 bg-gradient-to-r from-amber-50 to-orange-50 border-l-4 border-amber-500 rounded-lg">
                <p className="flex gap-2 items-start">
                  <Sparkles className="w-5 h-5 mt-1 text-amber-600" />
                  <span>
                    <strong className="text-amber-900">RAG Enhanced:</strong> 
                  rag-ai analysis used Retrieval-Augmented Generation for deeper, context-aware feedback powered by LLM.
                  using the Jd, resume , and company info as context.
                  </span>
                </p>
              </div>
            )}

          </div>

        </div>
      </motion.div>

      {/* RIGHT SIDE - Results */}
      <motion.div
        initial={{ x: 100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="lg:ml-[45%] lg:w-[55%] w-full min-h-screen overflow-y-auto p-8 bg-gradient-to-br from-gray-50 to-white"
      >
        <div className="max-w-2xl mx-auto space-y-6 pb-12">

          {/* Header */}
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Your Resume Match</h2>
            {ragEnabled && (
              <p className="text-sm text-amber-600 font-semibold flex items-center gap-1 mt-1">
                <Sparkles className="w-4 h-4" />
                {feedbackType} Analysis
              </p>
            )}
          </div>

          {/* Company Section */}
          {companyName !== 'N/A' && (
            <div className="p-4 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-xl">
              <div className="flex items-center gap-2 mb-2">
                <Building2 className="w-5 h-5 text-blue-600" />
                <span className="font-semibold text-gray-900">Target Company</span>
              </div>
              <p className="text-gray-800 font-medium">{companyName}</p>

              {companyUrl && companyUrl !== 'N/A' && (
                <a
                  href={companyUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 text-sm mt-1"
                >
                  Visit Website <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>
          )}

          {/* Score Section */}
          <div className="space-y-3">

            <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
              <p className="text-sm text-gray-600 mb-1">Skill Match Score</p>
              <p className="text-3xl font-bold text-blue-700">
                {Math.round(skillScore)}%
              </p>
            </div>

            <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border border-purple-200">
              <p className="text-sm text-gray-600 mb-1">BERT Semantic Score</p>
              <p className="text-3xl font-bold text-purple-700">
                {Math.round(bertScore)}%
              </p>
            </div>

            <div className="p-4 bg-gradient-to-r from-yellow-50 to-amber-50 rounded-xl border border-amber-200">
              <p className="text-sm text-gray-600 mb-1">TF-IDF Score</p>
              <p className="text-3xl font-bold text-amber-700">
                {Math.round(tfidfScore)}%
              </p>
            </div>

            {/* OVERALL SCORE BOX WITH STRICT VALIDATION BADGE */}
            <div className={`p-6 bg-gradient-to-r ${scoreGradient} rounded-xl shadow-lg text-white`}>
              <p className="text-sm opacity-90 mb-1">Overall Match Score</p>

              <div className="flex items-baseline gap-3">
                <p className="text-5xl font-bold">{Math.round(hybridScore)}%</p>
                <p className="text-lg font-semibold opacity-90">– {feedbackText}</p>
              </div>

              {/* ✔️ STRICT VALIDATION BADGE */}
              {strictValidation && (
                <p className="text-sm font-semibold bg-white/20 text-red-200 px-3 py-1 rounded-md inline-block mt-3">
                  ⚠️ Strict Validation Enabled
                </p>
              )}
            </div>

          </div>

          {/* AI FEEDBACK */}
          <div className="bg-white border-2 border-gray-200 rounded-xl p-5 shadow-md">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-amber-500" />
              <strong className="text-gray-900 text-lg">AI-Generated Insights</strong>
            </div>

            <div className="space-y-3">
              {aiFeedbackList.length > 0 ? (
                aiFeedbackList.map((point, index) => (
                  <div
                    key={index}
                    className="flex gap-3 p-4 bg-gradient-to-r from-gray-50 to-slate-50 rounded-lg border border-gray-200 hover:border-blue-300 transition"
                  >
                    <CheckCircle className="w-5 h-5 text-emerald-600 mt-0.5" />
                    <p className="text-sm text-gray-800">{point}</p>
                  </div>
                ))
              ) : (
                <p className="italic text-gray-500 text-center py-4">
                  No AI suggestions available.
                </p>
              )}
            </div>
          </div>

          {/* Resume Source */}
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-xl">
            <strong className="text-gray-700 text-sm">Resume Source:</strong>

            {resultData?.driveUrl && resultData.driveUrl !== 'NULL' ? (
              <a
                href={resultData.driveUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 ml-2 text-sm"
              >
                View on Drive <ExternalLink className="w-4 h-4" />
              </a>
            ) : (
              <span className="text-gray-500 ml-2 text-sm">Uploaded directly</span>
            )}
          </div>

        </div>
      </motion.div>

    </div>
  );
};

export default ResultView;
