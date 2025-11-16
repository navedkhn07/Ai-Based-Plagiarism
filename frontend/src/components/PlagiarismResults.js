import React, { useState } from 'react';

const PlagiarismResults = ({ results }) => {
  const { 
    similarityScore, 
    plagiarismPercentage, 
    exact_match_percentage = 0,
    partial_match_percentage = 0,
    unique_content_percentage = 0,
    matches, 
    analysis 
  } = results;
  const [expandedSources, setExpandedSources] = useState({});

  // Use actual percentages from backend, or calculate if not available
  const exactMatch = exact_match_percentage || Math.round(similarityScore * 0.8);
  const partialMatch = partial_match_percentage || Math.round(similarityScore * 0.2);
  const uniqueContent = unique_content_percentage || (100 - similarityScore);

  const toggleSource = (index) => {
    setExpandedSources(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 h-full flex flex-col">
      <h3 className="text-xl font-bold text-gray-800 mb-6">Plagiarism Results</h3>

      {/* Circular Percentage Display */}
      <div className="flex justify-center mb-8">
        <div className="relative w-48 h-48">
          <svg className="transform -rotate-90 w-48 h-48">
            <circle
              cx="96"
              cy="96"
              r="80"
              stroke="#e5e7eb"
              strokeWidth="16"
              fill="none"
            />
            <circle
              cx="96"
              cy="96"
              r="80"
              stroke={similarityScore >= 50 ? "#ef4444" : similarityScore >= 20 ? "#f59e0b" : "#10b981"}
              strokeWidth="16"
              fill="none"
              strokeDasharray={`${2 * Math.PI * 80}`}
              strokeDashoffset={`${2 * Math.PI * 80 * (1 - similarityScore / 100)}`}
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className={`text-4xl font-bold ${similarityScore >= 50 ? 'text-red-600' : similarityScore >= 20 ? 'text-orange-600' : 'text-green-600'}`}>
              {similarityScore.toFixed(0)}%
            </div>
            <div className="text-sm font-semibold text-gray-600 mt-1">Plagiarized</div>
          </div>
        </div>
      </div>

      {/* Breakdown */}
      <div className="space-y-4 mb-6">
        <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-200">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-red-500 rounded mr-3"></div>
            <span className="font-semibold text-gray-800">Exact Match</span>
          </div>
          <span className="text-lg font-bold text-red-600">{exactMatch.toFixed(1)}%</span>
        </div>

        <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg border border-orange-200">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-orange-500 rounded mr-3"></div>
            <span className="font-semibold text-gray-800">Partial Match</span>
          </div>
          <span className="text-lg font-bold text-orange-600">{partialMatch.toFixed(1)}%</span>
        </div>

        <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-green-500 rounded mr-3"></div>
            <span className="font-semibold text-gray-800">Unique Content</span>
          </div>
          <span className="text-lg font-bold text-green-600">{uniqueContent.toFixed(0)}%</span>
        </div>
      </div>

      {/* Plagiarized Sources */}
      {matches && matches.length > 0 && (
        <div className="mt-6 flex-1 overflow-y-auto">
          <h4 className="font-bold text-gray-800 mb-3">Plagiarized Scores</h4>
          <div className="space-y-2">
            {matches.map((match, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg overflow-hidden"
              >
                <button
                  onClick={() => toggleSource(index)}
                  className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 transition text-left"
                >
                  <div className="flex items-center flex-1 min-w-0">
                    <div className="w-2 h-2 bg-red-500 rounded-full mr-2 flex-shrink-0"></div>
                    <span className="font-medium text-gray-800 text-sm truncate">
                      {match.source || `Match ${match.match_number || index + 1}`}
                    </span>
                    {match.url && (
                      <a
                        href={match.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="ml-2 text-blue-600 hover:text-blue-800 flex-shrink-0"
                        title={match.url}
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </a>
                    )}
                  </div>
                  <span className="text-red-600 font-semibold ml-2 flex-shrink-0">
                    {match.similarity.toFixed(0)}%
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-500 ml-2 transform transition-transform flex-shrink-0 ${
                      expandedSources[index] ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {expandedSources[index] && (
                  <div className="p-3 bg-white border-t border-gray-200">
                    <p className="text-sm text-gray-700 mb-2 font-medium">Matching Text:</p>
                    <p className="text-sm text-gray-600 mb-3 bg-gray-50 p-2 rounded">{match.text}</p>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <div className="text-gray-500">
                          <span className="font-semibold">Type:</span> {match.match_type || 'partial'} match
                          <span className="ml-2 font-semibold">Similarity:</span> {match.similarity.toFixed(0)}%
                        </div>
                      </div>
                      {match.url ? (
                        <div className="pt-2 border-t border-gray-200">
                          <p className="text-xs text-gray-600 mb-1 font-semibold">Reference Link:</p>
                          <a
                            href={match.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 underline text-xs break-all flex items-start"
                          >
                            <svg className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                            </svg>
                            <span className="break-all">{match.url}</span>
                          </a>
                        </div>
                      ) : (
                        <div className="pt-2 border-t border-gray-200">
                          <p className="text-xs text-gray-500 italic">No reference link available for this match</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Analysis Summary */}
      {analysis && analysis.length > 0 && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-bold text-gray-800 mb-2 text-sm">Analysis Summary</h4>
          <div className="space-y-1">
            {analysis.slice(0, 2).map((item, index) => (
              <div key={index} className="text-sm text-gray-700">
                • {item.type}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PlagiarismResults;

