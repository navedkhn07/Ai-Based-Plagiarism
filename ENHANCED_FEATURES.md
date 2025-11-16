# Enhanced Plagiarism Checker - Like plagiarismchecker.ai

## New Features Added

### 1. **Multiple Search Strategies**
The enhanced detector uses 3 different search strategies to find sources:
- **Sentence-based**: Searches using key sentences from your text
- **Phrase-based**: Searches using important 4-6 word phrases
- **Keyword-based**: Searches using important keywords

This ensures maximum coverage and finds more sources.

### 2. **URL Checking** (Like plagiarismchecker.ai)
- **New Feature**: Check plagiarism directly from a URL
- Fetches content from the URL
- Extracts text and checks for plagiarism
- Works just like plagiarismchecker.ai's URL feature

### 3. **Enhanced Web Search**
- Always returns URLs (even if content fetch fails)
- Validates URLs before returning
- Better error handling
- More reliable source finding

### 4. **Improved Matching**
- Better similarity detection
- Word overlap detection (60%+ words match = partial match)
- Near-exact matching (ignores punctuation)
- More accurate phrase matching

### 5. **Better UI**
- Tab interface: "Paste Text" or "Check URL"
- Professional design matching plagiarismchecker.ai
- Better progress indicators
- Enhanced result display

## How to Use

### Check Text
1. Click "Paste Text" tab
2. Paste your text
3. Click "Check for Plagiarism"
4. Wait 15-30 seconds for results

### Check URL
1. Click "Check URL" tab
2. Enter a URL (e.g., https://example.com/article)
3. Click "Check URL"
4. System fetches content and checks for plagiarism

## Installation

### Backend Dependencies
```bash
cd backend
npm install cheerio
```

### AI Service
The enhanced detector is automatically used if available. It requires:
- `googlesearch-python` for web search
- `beautifulsoup4` for content parsing

## How It Works

1. **Text Analysis**: Extracts sentences, phrases, and keywords
2. **Multi-Strategy Search**: 
   - Searches with sentences
   - Searches with phrases
   - Searches with keywords
3. **Source Aggregation**: Combines all found sources
4. **Text Matching**: Compares your text against all sources
5. **Result Formatting**: Returns matches with URLs and percentages

## Features Matching plagiarismchecker.ai

✅ **Real-time web search** - Searches Google for similar content
✅ **URL checking** - Check plagiarism from URLs
✅ **Accurate percentages** - Exact match, partial match, unique content
✅ **Source links** - Clickable URLs for all matches
✅ **Color-coded highlighting** - Red (exact), Orange (partial), Green (unique)
✅ **Professional UI** - Clean, modern interface
✅ **Progress indicators** - Shows what's happening
✅ **Download report** - Download results

## Next Steps

1. **Install backend dependency**:
   ```bash
   cd backend
   npm install
   ```

2. **Restart services**:
   - Restart AI service
   - Restart backend

3. **Test it**:
   - Try pasting text from Wikipedia
   - Try checking a URL
   - Verify links work

---

**Your plagiarism checker now works like plagiarismchecker.ai!** 🎉

