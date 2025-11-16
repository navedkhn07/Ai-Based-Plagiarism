# Project Structure

## Overview

This project follows a modular architecture with three main components:

1. **Frontend** - React.js application with Tailwind CSS
2. **Backend** - Express.js API server with MongoDB
3. **AI Service** - Python Flask service for plagiarism detection

## Directory Structure

```
ai-plagiarism-checker/
│
├── frontend/                    # React frontend application
│   ├── public/
│   │   └── index.html          # HTML template
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Header.js        # Navigation header
│   │   │   ├── TextInput.js     # Text input component
│   │   │   ├── Results.js       # Results display component
│   │   │   └── LoadingSpinner.js # Loading indicator
│   │   ├── services/
│   │   │   └── api.js           # API service layer
│   │   ├── App.js               # Main app component
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Global styles with Tailwind
│   ├── package.json             # Frontend dependencies
│   ├── tailwind.config.js       # Tailwind configuration
│   └── postcss.config.js        # PostCSS configuration
│
├── backend/                     # Express.js backend API
│   ├── routes/
│   │   ├── check.js             # Plagiarism check endpoint
│   │   └── plagiarism.js        # History and stats endpoints
│   ├── models/
│   │   └── PlagiarismCheck.js   # MongoDB model
│   ├── server.js                # Express server entry point
│   ├── package.json             # Backend dependencies
│   └── .env.example             # Environment variables template
│
├── ai-service/                  # Python AI service
│   ├── app.py                   # Flask API application
│   ├── plagiarism_detector.py   # Core detection logic
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment variables template
│   └── README.md                # AI service documentation
│
├── package.json                 # Root package.json for scripts
├── .gitignore                   # Git ignore rules
├── README.md                    # Main project documentation
├── SETUP.md                     # Quick setup guide
└── PROJECT_STRUCTURE.md         # This file

```

## Component Responsibilities

### Frontend (`frontend/`)

**Purpose**: User interface for the plagiarism checker

**Key Files**:
- `App.js` - Main application component, manages state and routing
- `components/TextInput.js` - Text input area with word/character count
- `components/Results.js` - Displays plagiarism detection results
- `services/api.js` - Handles API communication with backend

**Technologies**:
- React.js for UI components
- Tailwind CSS for styling
- Axios for HTTP requests

### Backend (`backend/`)

**Purpose**: API server that coordinates between frontend and AI service

**Key Files**:
- `server.js` - Express server setup and middleware
- `routes/check.js` - Main plagiarism check endpoint
- `routes/plagiarism.js` - History and statistics endpoints
- `models/PlagiarismCheck.js` - MongoDB schema for check history

**Technologies**:
- Express.js for API routing
- MongoDB for data storage
- Axios for calling AI service

**API Endpoints**:
- `POST /api/check` - Check text for plagiarism
- `GET /api/plagiarism/history` - Get check history
- `GET /api/plagiarism/stats` - Get statistics
- `GET /api/health` - Health check

### AI Service (`ai-service/`)

**Purpose**: Core plagiarism detection using NLP and ML

**Key Files**:
- `app.py` - Flask API application
- `plagiarism_detector.py` - Main detection logic with Sentence-Transformers

**Technologies**:
- Flask for API framework
- Sentence-Transformers for semantic similarity
- spaCy for NLP processing
- scikit-learn for ML utilities

**AI Endpoints**:
- `POST /check` - Detect plagiarism in text
- `GET /health` - Service health check

## Data Flow

1. **User Input** → Frontend (`TextInput.js`)
2. **API Request** → Backend (`routes/check.js`)
3. **AI Processing** → AI Service (`plagiarism_detector.py`)
4. **Results** → Backend → Frontend (`Results.js`)
5. **Storage** → MongoDB (via `PlagiarismCheck` model)

## Extension Points

### Adding New Features

1. **Frontend**: Add new components in `frontend/src/components/`
2. **Backend**: Add new routes in `backend/routes/`
3. **AI Service**: Extend `plagiarism_detector.py` with new detection methods

### Database Schema

The `PlagiarismCheck` model stores:
- Text snippet (first 500 chars)
- Text length
- Similarity score
- Plagiarism percentage
- Matches count
- Timestamp

### Configuration

- **Frontend**: `frontend/tailwind.config.js` for styling
- **Backend**: `backend/.env` for server configuration
- **AI Service**: `ai-service/.env` for service configuration

## Modularity Benefits

1. **Independent Development**: Each component can be developed separately
2. **Technology Flexibility**: Use best tool for each layer
3. **Scalability**: Scale components independently
4. **Testing**: Test each component in isolation
5. **Deployment**: Deploy components separately if needed

