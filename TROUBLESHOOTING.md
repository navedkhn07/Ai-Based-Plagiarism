# Troubleshooting Guide

## Common Issues and Solutions

### Issue: "AI service is currently unavailable"

**Symptoms:**
- Error message: "AI service is currently unavailable. Please try again later."
- Or: "AI service is not running. Please start the AI service..."

**Cause:**
The Python AI service is not running or not accessible.

**Solution:**

1. **Start the AI Service**:
   
   **Windows:**
   ```bash
   cd ai-service
   python app.py
   ```
   
   **macOS/Linux:**
   ```bash
   cd ai-service
   python3 app.py
   ```

2. **Verify it's running**:
   - Open browser: http://localhost:8000/health
   - You should see: `{"status":"ok","message":"AI Plagiarism Detection Service is running","model_loaded":true}`

3. **Check the port**:
   - Ensure port 8000 is not used by another application
   - Check `ai-service/.env` for custom port

4. **Install Python dependencies**:
   ```bash
   cd ai-service
   pip install -r requirements.txt
   ```

5. **First-time model download**:
   - On first run, the Sentence-Transformers model will download (may take a few minutes)
   - Ensure you have internet connection
   - Wait for "✅ Model loaded successfully" message

### Issue: MongoDB Connection Error

**Symptoms:**
- Backend console shows: "❌ MongoDB connection error"
- Database operations fail

**Solution:**

1. **Start MongoDB**:
   
   **Windows:**
   ```bash
   mongod
   ```
   
   **macOS (Homebrew):**
   ```bash
   brew services start mongodb-community
   ```
   
   **Linux:**
   ```bash
   sudo systemctl start mongod
   ```

2. **Check MongoDB connection string** in `backend/.env`:
   ```env
   MONGODB_URI=mongodb://localhost:27017/plagiarism-checker
   ```

3. **Verify MongoDB is running**:
   ```bash
   mongo --eval "db.version()"
   ```

### Issue: Port Already in Use

**Symptoms:**
- Error: "EADDRINUSE: address already in use"
- Service fails to start

**Solution:**

1. **Find process using the port**:
   
   **Windows:**
   ```bash
   netstat -ano | findstr :5000
   netstat -ano | findstr :8000
   ```
   
   **macOS/Linux:**
   ```bash
   lsof -i :5000
   lsof -i :8000
   ```

2. **Kill the process** or change the port in `.env` files

3. **Change ports**:
   - Backend: Edit `backend/.env` → `PORT=5001`
   - AI Service: Edit `ai-service/.env` → `PORT=8001`
   - Update `backend/.env` → `AI_SERVICE_URL=http://localhost:8001`

### Issue: Python Dependencies Not Found

**Symptoms:**
- `ModuleNotFoundError` when starting AI service
- Import errors

**Solution:**

1. **Install dependencies**:
   ```bash
   cd ai-service
   pip install -r requirements.txt
   ```

2. **Use virtual environment** (recommended):
   ```bash
   cd ai-service
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Check Python version**:
   ```bash
   python --version  # Should be 3.8 or higher
   ```

### Issue: spaCy Model Not Found

**Symptoms:**
- Warning: "spaCy English model not found"
- Still works but with basic tokenization

**Solution:**

1. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Or use without spaCy** (works but less accurate):
   - The service will use basic sentence splitting
   - Still functional but may be less accurate

### Issue: Model Download Fails

**Symptoms:**
- AI service fails to start
- Error downloading Sentence-Transformers model

**Solution:**

1. **Check internet connection**
2. **Retry** - model download may take a few minutes
3. **Manual download**:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   ```

### Issue: Frontend Not Connecting to Backend

**Symptoms:**
- Frontend shows network errors
- API calls fail

**Solution:**

1. **Verify backend is running**:
   - Check: http://localhost:5000/api/health
   - Should return: `{"status":"ok","message":"Plagiarism Checker API is running"}`

2. **Check CORS settings** in `backend/server.js`

3. **Verify API URL** in `frontend/src/services/api.js`:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
   ```

4. **Check browser console** for specific errors

### Issue: "Text is required" Error

**Symptoms:**
- Error when submitting empty text

**Solution:**
- This is expected behavior
- Enter some text before checking

### Issue: Slow Response

**Symptoms:**
- Plagiarism check takes a long time

**Solution:**

1. **First run**: Model download takes time (one-time)
2. **Long texts**: Processing may take 10-30 seconds
3. **Check AI service console** for progress
4. **Consider using faster model** in `plagiarism_detector.py`

## Quick Diagnostic Commands

### Check All Services

**Windows:**
```bash
# Check if services are running
netstat -ano | findstr :3000  # Frontend
netstat -ano | findstr :5000  # Backend
netstat -ano | findstr :8000  # AI Service
```

**macOS/Linux:**
```bash
lsof -i :3000  # Frontend
lsof -i :5000  # Backend
lsof -i :8000  # AI Service
```

### Test API Endpoints

**Backend Health:**
```bash
curl http://localhost:5000/api/health
```

**AI Service Health:**
```bash
curl http://localhost:8000/health
```

**Test Plagiarism Check:**
```bash
curl -X POST http://localhost:5000/api/check \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"This is a test text.\"}"
```

## Still Having Issues?

1. **Check all console outputs** for error messages
2. **Verify all services are running**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000/api/health
   - AI Service: http://localhost:8000/health
3. **Check environment variables** in `.env` files
4. **Review logs** in each service's console
5. **Ensure all dependencies are installed**

