import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Header from './components/Header';
import Login from './components/Login';
import Signup from './components/Signup';
import TextInput from './components/TextInput';
import URLInput from './components/URLInput';
import HighlightedText from './components/HighlightedText';
import PlagiarismResults from './components/PlagiarismResults';
import ProgressIndicator from './components/ProgressIndicator';
import { checkPlagiarism, getCurrentUser } from './services/api';

function HomePage() {
  const [text, setText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputMode, setInputMode] = useState('text'); // 'text' or 'url'

  const handleCheck = async () => {
    if (!text.trim()) {
      setError('Please enter some text to check');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await checkPlagiarism(text);
      setResults(data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while checking plagiarism');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="container mx-auto px-4 py-6 max-w-7xl">
        {!results ? (
          <>
            <div className="text-center mb-6">
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                AI Plagiarism Checker
              </h1>
              <p className="text-gray-600">
                Detect similarities, copied content, and AI-generated writing using advanced NLP
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
              {/* Input Mode Tabs */}
              <div className="flex space-x-2 mb-4 border-b">
                <button
                  onClick={() => { setInputMode('text'); setText(''); setError(null); }}
                  className={`px-4 py-2 font-semibold transition ${
                    inputMode === 'text'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Paste Text
                </button>
                <button
                  onClick={() => { setInputMode('url'); setText(''); setError(null); }}
                  className={`px-4 py-2 font-semibold transition ${
                    inputMode === 'url'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Check URL
                </button>
              </div>

              {inputMode === 'text' ? (
                <TextInput
                  text={text}
                  setText={setText}
                  onCheck={handleCheck}
                  onClear={handleClear}
                  disabled={loading}
                />
              ) : (
                <URLInput
                  onResults={setResults}
                  onLoading={setLoading}
                  onError={setError}
                />
              )}
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                {error}
              </div>
            )}

            {loading && <ProgressIndicator stage={1} progress={50} />}
          </>
        ) : (
          <>
            <div className="mb-4">
              <button
                onClick={handleClear}
                className="text-blue-600 hover:text-blue-800 font-semibold flex items-center"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Input
              </button>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Panel - Highlighted Text */}
              <div>
                <HighlightedText
                  text={text}
                  matches={results.matches}
                  similarityScore={results.similarityScore}
                />
              </div>

              {/* Right Panel - Results */}
              <div>
                <PlagiarismResults results={results} />
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

function App() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser));
        // Verify token is still valid
        getCurrentUser().catch(() => {
          // Token invalid, clear storage
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          setUser(null);
        });
      } catch (e) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  }, []);

  const handleLogin = (userData, token) => {
    setUser(userData);
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header user={user} onLogout={handleLogout} />
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/signup" element={<Signup onLogin={handleLogin} />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </div>
  );
}

export default App;

