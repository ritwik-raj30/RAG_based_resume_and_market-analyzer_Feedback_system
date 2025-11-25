import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { axiosInstance } from '../lib/axios';
import toast from 'react-hot-toast';
import { motion } from 'framer-motion';
import { TrendingUp, Search, MapPin, Loader } from 'lucide-react';

const MarketAnalysisForm = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [location, setLocation] = useState('United States');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (!query.trim()) {
    toast.error('Please enter a search query');
    return;
  }

  console.log('🚀 Submitting analysis request:', { query, location });

  try {
    setIsAnalyzing(true);

    // API call to backend
    const response = await axiosInstance.post('/market/quick-analyze', {
      query: query.trim(),
      location: location.trim(),
      top_k: 5,
      use_llm: true
    });

    console.log('✅ Analysis response:', response.data);
    console.log('✅ Response success?', response.data.success);
    console.log('✅ Full response structure:', JSON.stringify(response.data, null, 2));

    // Check if successful
    if (response.data.success) {
      toast.success('Analysis complete!');
      
      console.log('🔄 About to navigate with state:', response.data);
      
      // Add a small delay to ensure state is set
      setTimeout(() => {
        navigate('/market-analysis-results', {
          state: { results: response.data },
          replace: false
        });
        console.log('✅ Navigation called');
      }, 100);
    } else {
      toast.error('Analysis failed - no success flag');
      console.error('Response missing success flag:', response.data);
    }

  } catch (error) {
    console.error('❌ Analysis error:', error);
    console.error('❌ Error details:', error.response?.data);
    toast.error(error.response?.data?.detail?.message || 'Analysis failed');
  } finally {
    setIsAnalyzing(false);
  }
};

  const exampleQueries = [
    'Python developer jobs',
    'React frontend engineer positions',
    'AI machine learning engineer',
    'Full stack web developer',
    'DevOps cloud engineer'
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-lime-50 to-white flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-2xl"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-600 to-lime-600 rounded-2xl mb-4">
            <TrendingUp className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-green-900 mb-2">
            Job Market Analysis
          </h1>
          <p className="text-gray-600 text-lg">
            Discover demand trends, required skills, and career insights powered by AI
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-green-100 p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Query Input */}
            <div>
              <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
                <Search className="w-4 h-4 text-green-600" />
                What job market do you want to analyze?
              </label>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., Python developer jobs, AI engineer positions..."
                className="w-full border-2 border-green-200 rounded-xl px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent transition"
                disabled={isAnalyzing}
              />
            </div>

            {/* Location Input */}
            <div>
              <label className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-2">
                <MapPin className="w-4 h-4 text-green-600" />
                Location
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="United States"
                className="w-full border-2 border-green-200 rounded-xl px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent transition"
                disabled={isAnalyzing}
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isAnalyzing}
              className={`w-full py-4 rounded-xl font-bold text-lg transition-all flex items-center justify-center gap-3 ${
                isAnalyzing
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-green-600 to-lime-600 hover:from-green-700 hover:to-lime-700 text-white shadow-lg hover:shadow-xl'
              }`}
            >
              {isAnalyzing ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Analyzing Market...
                </>
              ) : (
                <>
                  <TrendingUp className="w-5 h-5" />
                  Analyze Market
                </>
              )}
            </button>
          </form>

          {/* Example Queries */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-3">Try these examples:</p>
            <div className="flex flex-wrap gap-2">
              {exampleQueries.map((example, index) => (
                <button
                  key={index}
                  onClick={() => setQuery(example)}
                  disabled={isAnalyzing}
                  className="px-3 py-1.5 text-sm bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors border border-green-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Info Note */}
        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Analysis powered by live job market data • Results in ~30-60 seconds</p>
        </div>
      </motion.div>
    </div>
  );
};

export default MarketAnalysisForm;