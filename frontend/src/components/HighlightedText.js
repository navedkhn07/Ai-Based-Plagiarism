import React from 'react';

// Helper to find text position in original text (case-insensitive)
const findTextPosition = (text, searchText) => {
  const textLower = text.toLowerCase();
  const searchLower = searchText.toLowerCase();
  return textLower.indexOf(searchLower);
};

const HighlightedText = ({ text, matches, similarityScore }) => {
  // Calculate word and character counts
  const wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
  const charCount = text.length;

  // Determine which parts are plagiarized based on matches
  const getHighlightedText = () => {
    if (!matches || matches.length === 0 || similarityScore < 5) {
      // All text is unique
      return text.split('').map((char, index) => (
        <span key={index} className="bg-green-100 text-green-800">{char}</span>
      ));
    }

    // Create a map of text positions that are plagiarized
    const plagiarizedRanges = [];
    matches.forEach(match => {
      const matchText = match.text.trim();
      if (!matchText) return;
      
      // Try multiple strategies to find the text
      let startIndex = findTextPosition(text, matchText);
      
      // Strategy 1: Try exact match
      if (startIndex === -1) {
        // Strategy 2: Try matching first 5 words
        const words = matchText.split();
        if (words.length >= 5) {
          const searchPhrase = words.slice(0, 5).join(' ');
          startIndex = findTextPosition(text, searchPhrase);
        }
      }
      
      // Strategy 3: Try matching first 3 words
      if (startIndex === -1 && matchText.length > 10) {
        const words = matchText.split();
        if (words.length >= 3) {
          const searchPhrase = words.slice(0, 3).join(' ');
          startIndex = findTextPosition(text, searchPhrase);
        }
      }
      
      // Strategy 4: Try matching individual words (at least 3 consecutive words)
      if (startIndex === -1) {
        const words = matchText.split();
        if (words.length >= 3) {
          // Try to find any 3 consecutive words from the match
          for (let i = 0; i <= words.length - 3; i++) {
            const phrase = words.slice(i, i + 3).join(' ');
            const pos = findTextPosition(text, phrase);
            if (pos !== -1) {
              startIndex = pos;
              break;
            }
          }
        }
      }
      
      if (startIndex !== -1) {
        const endIndex = Math.min(startIndex + matchText.length, text.length);
        plagiarizedRanges.push({
          start: startIndex,
          end: endIndex,
          similarity: match.similarity,
          match_type: match.match_type || 'partial'
        });
      }
    });

    // Sort ranges by start position
    plagiarizedRanges.sort((a, b) => a.start - b.start);

    // Merge overlapping ranges
    const mergedRanges = [];
    plagiarizedRanges.forEach(range => {
      if (mergedRanges.length === 0) {
        mergedRanges.push(range);
      } else {
        const last = mergedRanges[mergedRanges.length - 1];
        if (range.start <= last.end) {
          last.end = Math.max(last.end, range.end);
          last.similarity = Math.max(last.similarity, range.similarity);
        } else {
          mergedRanges.push(range);
        }
      }
    });

    // Highlight text based on ranges
    const result = [];
    let lastIndex = 0;

    mergedRanges.forEach((range, index) => {
      // Add unique text before this range
      if (range.start > lastIndex) {
        result.push(
          <span key={`unique-${index}`} className="bg-green-100 text-green-800">
            {text.substring(lastIndex, range.start)}
          </span>
        );
      }

      // Add plagiarized text (red for exact, orange for partial - but same underline color)
      const isExact = range.match_type === 'exact';
      result.push(
        <span 
          key={`plag-${index}`} 
          className={
            isExact 
              ? "bg-red-100 text-red-800 font-medium border-b-2 border-orange-400" 
              : "bg-orange-100 text-orange-800 font-medium border-b-2 border-orange-400"
          }
        >
          {text.substring(range.start, range.end)}
        </span>
      );

      lastIndex = range.end;
    });

    // Add remaining unique text
    if (lastIndex < text.length) {
      result.push(
        <span key="unique-end" className="bg-green-100 text-green-800">
          {text.substring(lastIndex)}
        </span>
      );
    }

    return result.length > 0 ? result : (
      <span className="bg-green-100 text-green-800">{text}</span>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 h-full flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-gray-800">Uploaded Text</h3>
        <div className="text-sm text-gray-600">
          <span className="mr-4">Words: {wordCount}</span>
          <span>Characters: {charCount}</span>
        </div>
      </div>

      {/* Color Legend */}
      <div className="flex gap-4 mb-3 text-xs">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-red-500 rounded mr-2"></div>
          <span className="text-gray-700 font-medium">Exact Match</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-orange-500 rounded mr-2"></div>
          <span className="text-gray-700 font-medium">Partial Match</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-green-500 rounded mr-2"></div>
          <span className="text-gray-700 font-medium">Unique</span>
        </div>
      </div>
      
      <div className="border border-gray-200 rounded-lg p-4 bg-gray-50 flex-1 overflow-y-auto min-h-[400px] max-h-[600px]">
        <div className="text-base leading-relaxed whitespace-pre-wrap">
          {getHighlightedText()}
        </div>
      </div>

      <div className="mt-4 flex justify-end">
        <button
          onClick={() => {
            const blob = new Blob([text], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'plagiarism-check-text.txt';
            a.click();
            URL.revokeObjectURL(url);
          }}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-semibold"
        >
          Download Report
        </button>
      </div>
    </div>
  );
};

export default HighlightedText;

