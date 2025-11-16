const mongoose = require('mongoose');

const plagiarismCheckSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: false, // Allow anonymous checks
  },
  text: {
    type: String,
    required: true,
    maxlength: 10000, // Store more text
  },
  textLength: {
    type: Number,
    required: true,
  },
  similarityScore: {
    type: Number,
    required: true,
    min: 0,
    max: 100,
  },
  plagiarismPercentage: {
    type: Number,
    required: true,
    min: 0,
    max: 100,
  },
  exactMatchPercentage: {
    type: Number,
    default: 0,
    min: 0,
    max: 100,
  },
  partialMatchPercentage: {
    type: Number,
    default: 0,
    min: 0,
    max: 100,
  },
  uniqueContentPercentage: {
    type: Number,
    default: 0,
    min: 0,
    max: 100,
  },
  matchesCount: {
    type: Number,
    default: 0,
  },
  matches: [{
    text: String,
    similarity: Number,
    matchType: String,
    source: String,
    url: String,
  }],
  sources: [{
    url: String,
    title: String,
    snippet: String,
  }],
  timestamp: {
    type: Date,
    default: Date.now,
  },
}, {
  timestamps: true,
});

// Index for faster queries
plagiarismCheckSchema.index({ timestamp: -1 });
plagiarismCheckSchema.index({ similarityScore: -1 });
plagiarismCheckSchema.index({ user: 1, timestamp: -1 });

module.exports = mongoose.model('PlagiarismCheck', plagiarismCheckSchema);

