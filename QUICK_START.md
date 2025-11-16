# Quick Start Guide

## Fix: "AI service is currently unavailable" Error

If you're seeing this error, the AI service (Python Flask app) is not running. Follow these steps:

### Step 1: Start the AI Service

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

**Or use the startup script:**
- Windows: Double-click `start-ai-service.bat`
- macOS/Linux: `bash start-ai-service.sh`

### Step 2: Wait for Model to Load

On first run, you'll see:
```
Loading model: all-MiniLM-L6-v2...
```

This may take 1-2 minutes. Wait for:
```
✅ Model loaded successfully
✅ Plagiarism Detector initialized successfully
 * Running on http://0.0.0.0:8000
```

### Step 3: Verify AI Service is Running

Open a new terminal and test:
```bash
curl http://localhost:8000/health
```

Or open in browser: http://localhost:8000/health

You should see:
```json
{
  "status": "ok",
  "message": "AI Plagiarism Detection Service is running",
  "model_loaded": true
}
```

### Step 4: Test the Full System

1. **Start MongoDB** (if not running):
   ```bash
   mongod
   ```

2. **Start Backend** (new terminal):
   ```bash
   cd backend
   npm run dev
   ```

3. **Start Frontend** (new terminal):
   ```bash
   cd frontend
   npm start
   ```

4. **Test in Browser**: http://localhost:3000

## All Services Running?

You need **3 terminals** running:

1. **Terminal 1 - AI Service**:
   ```bash
   cd ai-service
   python app.py
   ```
   Should show: `Running on http://0.0.0.0:8000`

2. **Terminal 2 - Backend**:
   ```bash
   cd backend
   npm run dev
   ```
   Should show: `🚀 Server is running on port 5000`

3. **Terminal 3 - Frontend**:
   ```bash
   cd frontend
   npm start
   ```
   Should open browser at http://localhost:3000

## Quick Test Script

Run the test script to verify everything works:

```bash
python test-ai-service.py
```

This will test:
- ✅ AI service health
- ✅ Plagiarism check functionality

## Common Issues

### "ModuleNotFoundError"
**Fix**: Install Python dependencies
```bash
cd ai-service
pip install -r requirements.txt
```

### "Port 8000 already in use"
**Fix**: Change port in `ai-service/.env`:
```env
PORT=8001
```
Then update `backend/.env`:
```env
AI_SERVICE_URL=http://localhost:8001
```

### Model download fails
**Fix**: 
- Check internet connection
- Wait longer (first download takes time)
- Try again

## Still Not Working?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

