import React, { useState } from 'react';
import { checkPlagiarismFromURL } from '../services/api';

const URLInput = ({ onResults, onLoading, onError }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCheckURL = async () => {
    if (!url.trim()) {
      onError('Please enter a URL');
      return;
    }

    // Validate URL
    try {
      new URL(url);
    } catch {
      onError('Please enter a valid URL (e.g., https://example.com)');
      return;
    }

    setLoading(true);
    onLoading(true);
    onError(null);

    try {
      const data = await checkPlagiarismFromURL(url);
      onResults(data);
    } catch (err) {
      onError(err.response?.data?.error || 'Failed to check URL for plagiarism');
    } finally {
      setLoading(false);
      onLoading(false);
    }
  };

  return (
    <div className="mb-4">
      <label htmlFor="url-input" className="block text-sm font-medium text-gray-700 mb-2">
        Or check a URL
      </label>
      <div className="flex space-x-2">
        <input
          id="url-input"
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/article"
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={loading}
        />
        <button
          onClick={handleCheckURL}
          disabled={loading || !url.trim()}
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Checking...' : 'Check URL'}
        </button>
      </div>
    </div>
  );
};

export default URLInput;

