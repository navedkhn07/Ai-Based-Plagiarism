import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="bg-white rounded-lg shadow-xl p-8 text-center">
      <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
      <p className="text-gray-600">Analyzing text for plagiarism...</p>
      <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
    </div>
  );
};

export default LoadingSpinner;

