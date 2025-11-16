# AI-Based Plagiarism Checker

An AI-powered plagiarism checker that uses Natural Language Processing (NLP) and Machine Learning to detect similarities between texts. It can identify copied content, paraphrased sections, and even AI-generated writing.

## 🚀 Features

- **Semantic Similarity Detection**: Uses Sentence-Transformers (BERT-based models) to detect semantic similarities
- **AI-Generated Content Detection**: Identifies patterns typical of AI-generated text
- **Paraphrasing Detection**: Detects paraphrased content that may need citation
- **Modern UI/UX**: Beautiful, responsive interface built with React and Tailwind CSS
- **Modular Architecture**: Separated frontend, backend, and AI service for easy maintenance and scaling

## 🛠️ Technology Stack

### Frontend
- **React.js** - Component-based, fast UI rendering
- **Tailwind CSS** - Modern, utility-first CSS framework

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web application framework
- **MongoDB** - NoSQL database for storing check history

### AI & NLP
- **Python** - AI and NLP processing
- **Sentence-Transformers** - Semantic similarity using pre-trained BERT models
- **spaCy** - Natural language processing
- **TextBlob** - Text processing library
- **scikit-learn** - Machine learning utilities

## 📁 Project Structure

```
ai-plagiarism-checker/
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   └── App.js         # Main app component
│   └── package.json
├── backend/               # Express.js backend API
│   ├── routes/            # API routes
│   ├── models/            # MongoDB models
│   └── server.js          # Server entry point
├── ai-service/            # Python AI service
│   ├── app.py             # Flask API
│   └── plagiarism_detector.py  # Core detection logic
└── README.md
```

## 🚀 Getting Started

> **⚠️ Having issues?** See [QUICK_START.md](QUICK_START.md) for immediate help with common errors.

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (v4.4 or higher)
- **npm** or **yarn**

### Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Install all dependencies**:
   ```bash
   # Install root dependencies
   npm install
   
   # Install frontend dependencies
   cd frontend
   npm install
   cd ..
   
   # Install backend dependencies
   cd backend
   npm install
   cd ..
   
   # Install Python AI service dependencies
   cd ai-service
   pip install -r requirements.txt
   cd ..
   ```

   Or use the convenience script:
   ```bash
   npm run install-all
   ```

3. **Set up environment variables**:

   **Backend** (`backend/.env`):
   ```env
   PORT=5000
   MONGODB_URI=mongodb://localhost:27017/plagiarism-checker
   AI_SERVICE_URL=http://localhost:8000
   ```

   **AI Service** (`ai-service/.env`):
   ```env
   PORT=8000
   DEBUG=False
   ```

4. **Download spaCy English model** (optional but recommended):
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Start MongoDB**:
   ```bash
   # On Windows
   mongod
   
   # On macOS/Linux
   sudo systemctl start mongod
   # or
   mongod --dbpath /path/to/data
   ```

### Running the Application

#### Option 1: Run all services together (recommended for development)

From the root directory:
```bash
npm run dev
```

This will start:
- Frontend on `http://localhost:3000`
- Backend on `http://localhost:5000`
- AI Service on `http://localhost:8000`

#### Option 2: Run services individually

**Terminal 1 - AI Service**:
```bash
cd ai-service
python app.py
```

**Terminal 2 - Backend**:
```bash
cd backend
npm run dev
```

**Terminal 3 - Frontend**:
```bash
cd frontend
npm start
```

## 📖 Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Paste or type the text you want to check in the text area
3. Click "Check for Plagiarism"
4. View the results, including:
   - Similarity score
   - Plagiarism percentage
   - Detailed analysis
   - Matched content (if any)
   - Recommendations

## 🔧 Configuration

### Changing the AI Model

The default model is `all-MiniLM-L6-v2`. To use a different model, edit `ai-service/plagiarism_detector.py`:

```python
def __init__(self, model_name='all-MiniLM-L6-v2'):
    # Change model_name to your preferred model
    # Popular options:
    # - 'all-mpnet-base-v2' (more accurate, slower)
    # - 'paraphrase-MiniLM-L6-v2' (good for paraphrasing)
```

### Adjusting Similarity Thresholds

Edit `ai-service/plagiarism_detector.py` to adjust detection thresholds:

```python
# In detect_plagiarism method
if similarity_score > 20:  # Change threshold here
    # Generate matches
```

## 🎯 Goals & Future Enhancements

- ✅ Build the entire plagiarism checker
- ✅ Modularization of the codebase for wide use case
- ✅ Initial UI/UX design
- 🔄 More research on other wide case applications of the system

### Potential Enhancements

1. **Database Integration**: Compare against a database of known texts
2. **User Authentication**: Add user accounts and history
3. **File Upload**: Support document upload (PDF, Word, etc.)
4. **Batch Processing**: Check multiple texts at once
5. **API Rate Limiting**: Implement rate limiting for production
6. **Advanced AI Models**: Integrate more sophisticated models
7. **Citation Suggestions**: Automatically suggest citations for matched content
8. **Multi-language Support**: Support for multiple languages

## 🤝 Contributing

This is a modular project designed for easy extension. Key areas for contribution:

- **Frontend**: UI/UX improvements, new features
- **Backend**: API enhancements, database optimizations
- **AI Service**: Better detection algorithms, new models

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🐛 Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongod`
- Check the connection string in `backend/.env`

### AI Service Not Responding
- Verify Python dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is available
- Ensure the model downloads successfully on first run

### Frontend Not Connecting to Backend
- Verify backend is running on port 5000
- Check CORS settings in `backend/server.js`
- Ensure `frontend/src/services/api.js` has correct API URL

## 📚 Resources

- [Sentence-Transformers Documentation](https://www.sbert.net/)
- [React Documentation](https://react.dev/)
- [Express.js Documentation](https://expressjs.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)

---

**Note**: This is a demonstration project. For production use, consider:
- Adding authentication and authorization
- Implementing rate limiting
- Using a production-grade database
- Adding comprehensive error handling
- Implementing logging and monitoring
- Adding unit and integration tests

