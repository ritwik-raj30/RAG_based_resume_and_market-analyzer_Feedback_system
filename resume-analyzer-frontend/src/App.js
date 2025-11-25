// App.jsx

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './store/useAuthStore';

// Auth Components
import LoginForm from './components/Auth/LoginForm';
import SignupForm from './components/Auth/SignupForm';
import PreviousResults from './components/Auth/PreviousResults';

// Views
import HomePage from './views/HomePage';
import HRDashboard from './views/HRDashboard';
import UploadView from './views/UploadView';
import ResultView from './views/ResultView';
import MarketAnalysisForm from './views/market-analysis';
import MarketAnalysisResults from './views/marketanalysisResult'; // ✅ Import results page

// PrivateRoute wrapper for auth-protected routes
const PrivateRoute = ({ children }) => {
  const { authUser, isCheckingAuth } = useAuthStore();

  if (isCheckingAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Checking authentication...
      </div>
    );
  }

  return authUser ? children : <Navigate to="/login" replace />;
};

function App() {
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Router>
      <Toaster position="top-center" reverseOrder={false} />
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/signup" element={<SignupForm />} />

        {/* Auth-Protected Routes */}
        <Route
          path="/upload"
          element={
            <PrivateRoute>
              <UploadView />
            </PrivateRoute>
          }
        />
        <Route
          path="/results"
          element={
            <PrivateRoute>
              <ResultView />
            </PrivateRoute>
          }
        />
        <Route
          path="/getme"
          element={
            <PrivateRoute>
              <PreviousResults />
            </PrivateRoute>
          }
        />

        {/* HR Dashboard */}
        <Route path="/hr-dashboard" element={<HRDashboard />} />

        {/* Market Analysis */}
        <Route path="/market-analysis" element={<MarketAnalysisForm />} />
<Route path="/market-analysis-results" element={<MarketAnalysisResults />} />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
