# Setup Guide - Enhanced Plagiarism Checker with Authentication

## Overview

This application now includes:
1. **Enhanced Plagiarism Detection** using web search and advanced matching
2. **User Authentication** with login/signup
3. **MongoDB Atlas** integration for storing user data and plagiarism checks
4. **Reference Links** in plagiarism results (like plagiarismchecker.ai)
5. **Improved Detection** with more accurate percentages

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB)

## Installation Steps

### 1. Backend Setup

```bash
cd backend
npm install
```

Create a `.env` file in the `backend` directory:

```env
MONGODB_URI=mongodb+srv://navedkhn07_db_user:yO6dHEhQaprZPDRm@aibasedplagiarism.nevziui.mongodb.net/
JWT_SECRET=your-secret-key-change-in-production
PORT=5000
AI_SERVICE_URL=http://localhost:8000
```

### 2. AI Service Setup

```bash
cd ai-service
pip install -r requirements.txt
```

Create a `.env` file in the `ai-service` directory (optional):

```env
PORT=8000
DEBUG=False
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Terminal 1: Start Backend Server

```bash
cd backend
npm start
```

The backend will run on `http://localhost:5000`

### Terminal 2: Start AI Service

```bash
cd ai-service
python app.py
```

The AI service will run on `http://localhost:8000`

### Terminal 3: Start Frontend

```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:3000`

## Features

### 1. User Authentication

- **Sign Up**: Create a new account with name, email, and password
- **Login**: Sign in with email and password
- **Protected Routes**: User data is saved with plagiarism checks
- **JWT Tokens**: Secure authentication using JSON Web Tokens

### 2. Enhanced Plagiarism Detection

- **Web Search**: Searches the internet for similar content using Google search
- **Advanced Matching**: Uses multiple search strategies and better matching algorithms
- **Accurate Percentages**: 
  - Exact Match: 95%+ similarity
  - Partial Match: 70%+ similarity
  - Better detection of copied content
- **Reference Links**: Each match includes clickable source URLs
- **Detailed Results**: Shows exact match %, partial match %, and unique content %

### 3. Database Storage

- **User Data**: Stored in MongoDB with encrypted passwords
- **Plagiarism Checks**: All checks are saved with:
  - User information (if logged in)
  - Full text (up to 10,000 characters)
  - Match details with URLs
  - Source information
  - Timestamps

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (requires token)

### Plagiarism Check

- `POST /api/check` - Check text for plagiarism (optional auth)
- `POST /api/check/url` - Check URL content for plagiarism

## Testing

Test with the provided text:
```
Anatomically modern humans first arrived on the Indian subcontinent between 73,000 and 55,000 years ago.[1] The earliest known human remains in South Asia date to 30,000 years ago. Sedentariness began in South Asia around 7000 BCE; by 4500 BCE, settled life had spread,[2] and gradually evolved into the Indus Valley Civilisation, one of three early cradles of civilisation in the Old World,[3][4] which flourished between 2500 BCE and 1900 BCE in present-day Pakistan and north-western India.
```

Expected result: ~96% plagiarism (matching plagiarismchecker.ai)

## Troubleshooting

### AI Service Not Starting

1. Install dependencies: `pip install -r requirements.txt`
2. Check Python version: `python --version` (should be 3.8+)
3. Ensure googlesearch-python is installed: `pip install googlesearch-python`

### MongoDB Connection Issues

1. Verify MongoDB URI is correct
2. Check if IP is whitelisted in MongoDB Atlas
3. Ensure network access is enabled

### Frontend Not Connecting

1. Verify backend is running on port 5000
2. Verify AI service is running on port 8000
3. Check browser console for errors

## Security Notes

1. **Change JWT_SECRET** in production
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** in production
4. **Rate limiting** recommended for production use

## Next Steps

1. Add user dashboard to view past checks
2. Add export functionality for reports
3. Add batch checking for multiple documents
4. Implement rate limiting
5. Add email verification


