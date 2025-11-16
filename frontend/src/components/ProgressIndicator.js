import React from 'react';

const ProgressIndicator = ({ stage, progress }) => {
  const stages = [
    { name: 'Analyzing text', icon: '📝' },
    { name: 'Searching web', icon: '🔍' },
    { name: 'Finding matches', icon: '🔗' },
    { name: 'Calculating scores', icon: '📊' },
  ];

  return (
    <div className="bg-white rounded-lg shadow-xl p-8">
      <div className="text-center mb-6">
        <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mb-4"></div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Checking for Plagiarism</h3>
        <p className="text-gray-600">This may take 15-30 seconds...</p>
      </div>

      <div className="space-y-3">
        {stages.map((s, index) => {
          const isActive = index === stage;
          const isCompleted = index < stage;
          
          return (
            <div
              key={index}
              className={`flex items-center p-3 rounded-lg transition ${
                isActive
                  ? 'bg-blue-50 border-2 border-blue-500'
                  : isCompleted
                  ? 'bg-green-50 border border-green-300'
                  : 'bg-gray-50 border border-gray-200'
              }`}
            >
              <span className="text-2xl mr-3">{s.icon}</span>
              <span
                className={`font-medium ${
                  isActive ? 'text-blue-700' : isCompleted ? 'text-green-700' : 'text-gray-500'
                }`}
              >
                {s.name}
              </span>
              {isActive && (
                <div className="ml-auto">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                </div>
              )}
              {isCompleted && (
                <span className="ml-auto text-green-600">✓</span>
              )}
            </div>
          );
        })}
      </div>

      <div className="mt-6 text-center text-sm text-gray-500">
        <p>Searching the web for similar content...</p>
        <p className="mt-1">This ensures accurate plagiarism detection</p>
      </div>
    </div>
  );
};

export default ProgressIndicator;

