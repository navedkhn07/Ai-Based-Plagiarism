const express = require('express');
const router = express.Router();
const axios = require('axios');
const PlagiarismCheck = require('../models/PlagiarismCheck');

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';

// POST /api/check - Check text for plagiarism
router.post('/', async (req, res) => {
  try {
    const { text } = req.body;

    if (!text || typeof text !== 'string' || text.trim().length === 0) {
      return res.status(400).json({ error: 'Text is required' });
    }

    if (text.length > 10000) {
      return res.status(400).json({ error: 'Text is too long. Maximum 10,000 characters allowed.' });
    }

    // Call Python AI service
    let aiResponse;
    try {
      aiResponse = await axios.post(`${AI_SERVICE_URL}/check`, {
        text: text.trim(),
      }, {
        timeout: 30000, // 30 seconds timeout
      });
    } catch (error) {
      console.error('AI Service Error:', error.message);
      console.error('AI Service URL:', AI_SERVICE_URL);
      if (error.code === 'ECONNREFUSED') {
        return res.status(503).json({
          error: 'AI service is not running. Please start the AI service by running: cd ai-service && python app.py',
          details: `Could not connect to ${AI_SERVICE_URL}. Make sure the AI service is running on port 8000.`,
        });
      }
      return res.status(503).json({
        error: 'AI service is currently unavailable. Please try again later.',
        details: error.message,
      });
    }

    const result = {
      similarityScore: aiResponse.data.similarity_score || 0,
      plagiarismPercentage: aiResponse.data.plagiarism_percentage || 0,
      exact_match_percentage: aiResponse.data.exact_match_percentage || 0,
      partial_match_percentage: aiResponse.data.partial_match_percentage || 0,
      unique_content_percentage: aiResponse.data.unique_content_percentage || 0,
      matches: aiResponse.data.matches || [],
      analysis: aiResponse.data.analysis || [],
      sources: aiResponse.data.sources || [],
      timestamp: new Date(),
    };

    // Save to database with user information
    try {
      const checkRecord = new PlagiarismCheck({
        user: req.user ? req.user._id : null, // Save user if authenticated
        text: text.substring(0, 10000), // Store up to 10k chars
        textLength: text.length,
        similarityScore: result.similarityScore,
        plagiarismPercentage: result.plagiarismPercentage,
        exactMatchPercentage: result.exact_match_percentage,
        partialMatchPercentage: result.partial_match_percentage,
        uniqueContentPercentage: result.unique_content_percentage,
        matchesCount: result.matches.length,
        matches: result.matches.map(m => ({
          text: m.text,
          similarity: m.similarity,
          matchType: m.match_type,
          source: m.source,
          url: m.url,
        })),
        sources: (result.sources || []).map(s => ({
          url: s.url,
          title: s.title,
          snippet: s.snippet || '',
        })),
      });
      await checkRecord.save();
      console.log('✅ Plagiarism check saved to database');
    } catch (dbError) {
      console.error('Database save error:', dbError);
      // Continue even if DB save fails
    }

    res.json(result);
  } catch (error) {
    console.error('Check error:', error);
    res.status(500).json({ error: 'An error occurred while checking plagiarism' });
  }
});

// POST /api/check-url - Check URL for plagiarism
router.post('/url', async (req, res) => {
  try {
    const { url } = req.body;

    if (!url || typeof url !== 'string' || url.trim().length === 0) {
      return res.status(400).json({ error: 'URL is required' });
    }

    // Validate URL
    try {
      new URL(url);
    } catch {
      return res.status(400).json({ error: 'Invalid URL format' });
    }

    // Fetch content from URL
    const axios = require('axios');
    let pageContent;
    try {
      const response = await axios.get(url, {
        timeout: 10000,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      });
      
      // Extract text from HTML
      const cheerio = require('cheerio');
      const $ = cheerio.load(response.data);
      $('script, style, nav, footer, header').remove();
      pageContent = $('body').text().trim();
      
      if (!pageContent || pageContent.length < 50) {
        return res.status(400).json({ error: 'Could not extract meaningful content from URL' });
      }
    } catch (error) {
      return res.status(400).json({ 
        error: 'Failed to fetch content from URL. Please check if the URL is accessible.' 
      });
    }

    // Check plagiarism of the fetched content
    const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8000';
    let aiResponse;
    try {
      aiResponse = await axios.post(`${AI_SERVICE_URL}/check`, {
        text: pageContent,
      }, {
        timeout: 30000,
      });
    } catch (error) {
      console.error('AI Service Error:', error.message);
      return res.status(503).json({
        error: 'AI service is currently unavailable. Please try again later.',
      });
    }

    const result = {
      similarityScore: aiResponse.data.similarity_score || 0,
      plagiarismPercentage: aiResponse.data.plagiarism_percentage || 0,
      exact_match_percentage: aiResponse.data.exact_match_percentage || 0,
      partial_match_percentage: aiResponse.data.partial_match_percentage || 0,
      unique_content_percentage: aiResponse.data.unique_content_percentage || 0,
      matches: aiResponse.data.matches || [],
      analysis: aiResponse.data.analysis || [],
      sourceUrl: url,
      timestamp: new Date(),
    };

    res.json(result);
  } catch (error) {
    console.error('URL check error:', error);
    res.status(500).json({ error: 'An error occurred while checking URL for plagiarism' });
  }
});

module.exports = router;

