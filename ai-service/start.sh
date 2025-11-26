#!/bin/bash
# Start script for Render deployment
# Render automatically sets PORT environment variable

echo "🚀 Starting AI Plagiarism Service..."
echo "📡 PORT environment variable: ${PORT}"

# Use gunicorn with explicit port binding
gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 120

