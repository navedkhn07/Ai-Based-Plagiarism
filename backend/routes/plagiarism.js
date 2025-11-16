const express = require('express');
const router = express.Router();
const PlagiarismCheck = require('../models/PlagiarismCheck');

// GET /api/plagiarism/history - Get check history
router.get('/history', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 10;
    const checks = await PlagiarismCheck.find()
      .sort({ timestamp: -1 })
      .limit(limit)
      .select('-__v');

    res.json(checks);
  } catch (error) {
    console.error('History error:', error);
    res.status(500).json({ error: 'An error occurred while fetching history' });
  }
});

// GET /api/plagiarism/stats - Get statistics
router.get('/stats', async (req, res) => {
  try {
    const totalChecks = await PlagiarismCheck.countDocuments();
    const avgSimilarity = await PlagiarismCheck.aggregate([
      {
        $group: {
          _id: null,
          avgSimilarity: { $avg: '$similarityScore' },
        },
      },
    ]);

    res.json({
      totalChecks,
      averageSimilarity: avgSimilarity[0]?.avgSimilarity || 0,
    });
  } catch (error) {
    console.error('Stats error:', error);
    res.status(500).json({ error: 'An error occurred while fetching statistics' });
  }
});

module.exports = router;

