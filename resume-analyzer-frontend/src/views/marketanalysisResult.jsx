import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  MapPin, 
  ArrowLeft, 
  Target, 
  DollarSign, 
  Award, 
  Lightbulb,
  Briefcase,
  CheckCircle,
  AlertCircle,
  Loader
} from 'lucide-react';

const MarketAnalysisResults = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('📍 MarketAnalysisResults mounted');
    console.log('📊 Location state:', location.state);
    
    if (location.state?.results) {
      console.log('✅ Results found, setting state');
      setResults(location.state.results);
      setError(null);
      setIsLoading(false);
    } else {
      console.log('❌ No results found in location state');
      const timer = setTimeout(() => {
        if (!location.state?.results) {
          console.log('❌ Still no results after timeout');
          setError('No results found');
          setIsLoading(false);
        }
      }, 1000);
      
      return () => clearTimeout(timer);
    }
  }, [location]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-lime-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-16 h-16 text-green-600 mx-auto mb-4 animate-spin" />
          <p className="text-xl text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  if (error || !results || !results.success) {
    console.log('🚫 Showing error state:', { error, results, success: results?.success });
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-lime-50 flex items-center justify-center p-4">
        <div className="text-center max-w-md">
          <AlertCircle className="w-16 h-16 text-red-400 mx-auto mb-4" />
          <p className="text-xl text-gray-600 mb-2">No results found or analysis failed</p>
          <p className="text-sm text-gray-500 mb-6">
            Error: {error || 'No data received'}
          </p>
          <button
            onClick={() => navigate('/market-analysis')}
            className="px-6 py-3 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-all"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  console.log('✅ Rendering results page with data');

  const report = results.report || {};
  const demandLevel = report.demand_level || 'MEDIUM';
  const demandReasons = Array.isArray(report.demand_reason) 
    ? report.demand_reason 
    : (typeof report.demand_reason === 'string' ? [report.demand_reason] : []);
  
  const recommendations = typeof report.recommendations === 'string'
    ? [report.recommendations]
    : (Array.isArray(report.recommendations) ? report.recommendations : []);

  // Check if salary insights has actual data
  const salaryInsights = report.salary_insights || {};
  const hasSalaryData = salaryInsights && Object.keys(salaryInsights).length > 0;

  const demandConfig = {
    HIGH: {
      color: 'text-green-600 bg-green-50 border-green-200',
      emoji: '🔥',
      badge: 'bg-green-600'
    },
    MEDIUM: {
      color: 'text-yellow-600 bg-yellow-50 border-yellow-200',
      emoji: '⚡',
      badge: 'bg-yellow-600'
    },
    LOW: {
      color: 'text-red-600 bg-red-50 border-red-200',
      emoji: '📉',
      badge: 'bg-red-600'
    },
    UNKNOWN: {
      color: 'text-gray-600 bg-gray-50 border-gray-200',
      emoji: '❓',
      badge: 'bg-gray-600'
    }
  };

  const demandStyle = demandConfig[demandLevel] || demandConfig.UNKNOWN;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-lime-50 to-white">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-green-100 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/market-analysis')}
              className="p-2 hover:bg-green-50 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-green-700" />
            </button>
            <h1 className="text-2xl font-bold text-green-900">Market Analysis Results</h1>
          </div>
          <button
            onClick={() => navigate('/market-analysis')}
            className="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all"
          >
            New Analysis
          </button>
        </div>
      </div>

      {/* Results Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="space-y-6"
        >
          {/* Query Info Card */}
          <div className="bg-white rounded-2xl shadow-lg border border-green-100 p-6">
            <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
              <div className="flex-1">
                <h2 className="text-2xl md:text-3xl font-bold text-green-900 mb-3">
                  {results.query}
                </h2>
                <div className="flex flex-wrap items-center gap-4 text-gray-600">
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4" />
                    <span>{results.location}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Briefcase className="w-4 h-4" />
                    <span>{results.total_results} job matches</span>
                  </div>
                  {results.skills_analyzed && (
                    <div className="flex items-center gap-2">
                      <Award className="w-4 h-4" />
                      <span>{results.skills_analyzed.join(', ')}</span>
                    </div>
                  )}
                </div>
              </div>
              <div className={`flex items-center gap-2 px-5 py-3 rounded-xl font-bold text-lg border-2 ${demandStyle.color}`}>
                <span className="text-2xl">{demandStyle.emoji}</span>
                {demandLevel} DEMAND
              </div>
            </div>
          </div>

          {/* Demand Analysis */}
          {demandReasons.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg border border-green-100 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Target className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-green-900">Market Demand Analysis</h3>
              </div>
              <ul className="space-y-3">
                {demandReasons.map((reason, index) => (
                  <motion.li
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start gap-3 p-4 bg-gradient-to-r from-green-50 to-lime-50 rounded-lg border border-green-100"
                  >
                    <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700 leading-relaxed">{reason}</span>
                  </motion.li>
                ))}
              </ul>
            </div>
          )}

          {/* Top Skills */}
          {report.top_skills && report.top_skills.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg border border-green-100 p-6">
              <div className="flex items-center gap-3 mb-5">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Award className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-green-900">Top Required Skills</h3>
              </div>
              <div className="flex flex-wrap gap-3">
                {report.top_skills.map((skill, index) => (
                  <motion.span
                    key={index}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    className="px-5 py-3 bg-gradient-to-r from-green-100 to-lime-100 text-green-800 rounded-xl font-semibold text-base shadow-sm hover:shadow-md transition-shadow"
                  >
                    {skill}
                  </motion.span>
                ))}
              </div>
            </div>
          )}

          {/* Missing Skill Recommendation */}
          {report.missing_skill && (
            <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-2xl shadow-lg border-2 border-orange-200 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-white rounded-lg shadow-sm">
                  <Lightbulb className="w-6 h-6 text-orange-600" />
                </div>
                <h3 className="text-xl font-bold text-orange-900">💡 Skill Gap Identified</h3>
              </div>
              <div className="bg-white rounded-xl p-5 shadow-sm">
                <p className="text-xl font-bold text-orange-800 mb-2">
                  {report.missing_skill}
                </p>
                <p className="text-gray-700">
                  Learning this skill could significantly boost your marketability and open up new opportunities in this field.
                </p>
              </div>
            </div>
          )}

          {/* Salary Insights - Only show if there's actual data */}
          {hasSalaryData && (
            <div className="bg-white rounded-2xl shadow-lg border border-green-100 p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <DollarSign className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-green-900">Salary Insights</h3>
              </div>
              <div className="bg-gradient-to-r from-green-50 to-lime-50 rounded-xl p-6 border border-green-100">
                <div className="space-y-3">
                  {Object.entries(salaryInsights).map(([key, value]) => (
                    <div key={key} className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 p-3 bg-white rounded-lg">
                      <span className="text-gray-700 font-medium capitalize">
                        {key.replace(/_/g, ' ')}
                      </span>
                      <span className="text-xl sm:text-2xl font-bold text-green-700">
                        {value}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Recommendations */}
          {recommendations.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg border border-green-100 p-6">
              <div className="flex items-center gap-3 mb-5">
                <div className="p-2 bg-green-100 rounded-lg">
                  <TrendingUp className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-green-900">Career Recommendations</h3>
              </div>
              <div className="space-y-3">
                {recommendations.map((rec, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="p-5 bg-gradient-to-r from-green-50 to-lime-50 rounded-xl border border-green-100"
                  >
                    <p className="text-gray-800 leading-relaxed">{rec}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Job Matches */}
          {results.hits && results.hits.length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg border border-green-100 p-6">
              <h3 className="text-xl font-bold text-green-900 mb-5">
                📋 Related Job Postings ({results.hits.length})
              </h3>
              <div className="space-y-4">
                {results.hits.slice(0, 5).map((hit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="p-5 bg-gradient-to-r from-green-50 to-lime-50 rounded-xl border border-green-100 hover:shadow-md transition-all"
                  >
                    <div className="flex items-start justify-between mb-2 flex-wrap gap-2">
                      <h4 className="font-bold text-lg text-green-900">
                        {hit.source_job_title || hit.metadata?.job_title || 'Job Title'}
                      </h4>
                      {hit.score && (
                        <span className="flex items-center gap-1 px-3 py-1 bg-green-600 text-white text-sm font-semibold rounded-full">
                          <CheckCircle className="w-4 h-4" />
                          {(hit.score * 100).toFixed(0)}% match
                        </span>
                      )}
                    </div>
                    {hit.source_company && (
                      <p className="text-sm text-gray-600 mb-3 font-medium">
                        🏢 {hit.source_company}
                      </p>
                    )}
                    {hit.chunk_text && (
                      <p className="text-sm text-gray-700 line-clamp-3">
                        {hit.chunk_text}
                      </p>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 pt-6">
            <button
              onClick={() => navigate('/market-analysis')}
              className="flex-1 bg-gradient-to-r from-green-600 to-lime-600 text-white py-4 rounded-xl font-semibold shadow-lg hover:from-green-700 hover:to-lime-700 transition-all flex items-center justify-center gap-2"
            >
              <TrendingUp className="w-5 h-5" />
              Start New Analysis
            </button>
            <button
              onClick={() => navigate('/')}
              className="flex-1 bg-white text-green-700 border-2 border-green-600 py-4 rounded-xl font-semibold hover:bg-green-50 transition-all"
            >
              Back to Home
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default MarketAnalysisResults;