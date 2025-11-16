# Installing Web Search for Real-Time Plagiarism Detection

## Quick Install

```bash
cd ai-service
pip install googlesearch-python beautifulsoup4
```

## Verify Installation

Run the test script:
```bash
cd ai-service
python test_web_search.py
```

## What This Does

The web search module:
1. **Searches Google** for similar content (takes 15-30 seconds)
2. **Fetches web pages** to compare against your text
3. **Finds real matches** with actual source URLs
4. **Calculates accurate percentages** based on real matches

## Why It Takes Time

- **Web search**: 5-10 seconds per query
- **Content fetching**: 2-5 seconds per URL
- **Text matching**: 1-2 seconds
- **Total**: 15-30 seconds for accurate results

## Troubleshooting

### "googlesearch library not installed"
**Fix**: 
```bash
pip install googlesearch-python
```

### "No results found" or "Search failed"
**Possible causes**:
- Google rate limiting (too many requests)
- Network connectivity issues
- Firewall blocking requests

**Solutions**:
- Wait 5-10 minutes and try again
- Check internet connection
- Check firewall settings

### Search is too slow
**This is normal!** Real web search takes time:
- Each query: 5-10 seconds
- Each page fetch: 2-5 seconds
- Multiple queries: 15-30 seconds total

**To speed up** (for testing):
- Reduce `max_results` in `web_search.py`
- Reduce number of queries
- Use Google Custom Search API (requires API key)

## Progress Indicators

The system now shows:
- Console logs with progress
- Frontend progress indicator
- Time estimates

## Next Steps

1. Install dependencies: `pip install googlesearch-python beautifulsoup4`
2. Restart AI service
3. Test with sample text
4. Check console for progress logs
5. Wait 15-30 seconds for results

---

**Real plagiarism detection requires web search, which takes time but provides accurate results!**

