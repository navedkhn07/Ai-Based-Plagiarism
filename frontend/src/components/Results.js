import React from 'react';

const Results = ({ results }) => {
  const { similarityScore, plagiarismPercentage, matches, analysis } = results;

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-red-600 bg-red-50';
    if (score >= 50) return 'text-orange-600 bg-orange-50';
    if (score >= 20) return 'text-yellow-600 bg-yellow-50';
    return 'text-green-600 bg-green-50';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'High Risk';
    if (score >= 50) return 'Medium Risk';
    if (score >= 20) return 'Low Risk';
    return 'Original';
  };

  return (
    <div className="space-y-6">
      {/* Overall Score Card */}
      <div className="bg-white rounded-lg shadow-xl p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Plagiarism Analysis Results</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className={`p-6 rounded-lg ${getScoreColor(similarityScore)}`}>
            <div className="text-sm font-medium mb-2">Similarity Score</div>
            <div className="text-4xl font-bold mb-1">{similarityScore.toFixed(1)}%</div>
            <div className="text-sm font-semibold">{getScoreLabel(similarityScore)}</div>
          </div>
          
          <div className="p-6 rounded-lg bg-blue-50 text-blue-600">
            <div className="text-sm font-medium mb-2">Plagiarism Percentage</div>
            <div className="text-4xl font-bold mb-1">{plagiarismPercentage.toFixed(1)}%</div>
            <div className="text-sm font-semibold">Detected Similarity</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Originality</span>
            <span>{100 - similarityScore.toFixed(1)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${100 - similarityScore}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Analysis Details */}
      {analysis && (
        <div className="bg-white rounded-lg shadow-xl p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Detailed Analysis</h3>
          <div className="space-y-3">
            {analysis.map((item, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="font-semibold text-gray-800">{item.type}</div>
                <div className="text-gray-600 text-sm">{item.description}</div>
                {item.confidence && (
                  <div className="text-xs text-gray-500 mt-1">
                    Confidence: {item.confidence}%
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Matches */}
      {matches && matches.length > 0 && (
        <div className="bg-white rounded-lg shadow-xl p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Similar Content Matches</h3>
          <div className="space-y-4">
            {matches.map((match, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                <div className="flex justify-between items-start mb-2">
                  <div className="font-semibold text-gray-800">
                    Match {index + 1}
                  </div>
                  <div className="text-sm font-semibold text-red-600">
                    {match.similarity.toFixed(1)}% similar
                  </div>
                </div>
                <div className="text-sm text-gray-600 mb-2">
                  {match.text}
                </div>
                {match.source && (
                  <div className="text-xs text-gray-500">
                    Source: {match.source}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg shadow-xl p-6 border border-blue-200">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Recommendations</h3>
        <ul className="space-y-2 text-gray-700">
          {similarityScore >= 80 && (
            <li className="flex items-start">
              <span className="text-red-500 mr-2">⚠️</span>
              <span>High similarity detected. Consider rewriting significant portions of the text.</span>
            </li>
          )}
          {similarityScore >= 50 && similarityScore < 80 && (
            <li className="flex items-start">
              <span className="text-orange-500 mr-2">⚠️</span>
              <span>Moderate similarity found. Review and cite sources appropriately.</span>
            </li>
          )}
          {similarityScore < 50 && (
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Text appears to be mostly original. Continue to cite sources when using external information.</span>
            </li>
          )}
          <li className="flex items-start">
            <span className="text-blue-500 mr-2">💡</span>
            <span>Always provide proper citations for any referenced material.</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Results;

