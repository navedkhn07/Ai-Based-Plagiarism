import React from 'react';

const TextInput = ({ text, setText, onCheck, onClear, disabled }) => {
  const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
  const charCount = text.length;

  return (
    <div>
      <div className="mb-4">
        <label htmlFor="text-input" className="block text-sm font-medium text-gray-700 mb-2">
          Enter or paste your text here
        </label>
        <textarea
          id="text-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste your text here to check for plagiarism..."
          className="w-full h-80 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono text-sm"
          disabled={disabled}
        />
        <div className="flex justify-between items-center mt-2 text-sm text-gray-500">
          <span>{wordCount} words</span>
          <span>{charCount} characters</span>
        </div>
      </div>

      <div className="flex space-x-4">
        <button
          onClick={onCheck}
          disabled={disabled || !text.trim()}
          className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        >
          {disabled ? 'Checking...' : 'Check for Plagiarism'}
        </button>
        <button
          onClick={onClear}
          disabled={disabled}
          className="px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Clear
        </button>
      </div>
    </div>
  );
};

export default TextInput;

