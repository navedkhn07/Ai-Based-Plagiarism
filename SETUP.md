# Quick Setup Guide

## Prerequisites Checklist

- [ ] Node.js (v16+) installed
- [ ] Python (v3.8+) installed
- [ ] MongoDB installed and running
- [ ] npm or yarn installed
- [ ] pip installed

## Step-by-Step Setup

### 1. Install Dependencies

```bash
# Install all dependencies
npm run install-all

# Or install individually:
cd frontend && npm install && cd ..
cd backend && npm install && cd ..
cd ai-service && pip install -r requirements.txt && cd ..
```

### 2. Download spaCy Model (Optional but Recommended)

```bash
python -m spacy download en_core_web_sm
```

### 3. Set Up Environment Variables

**Backend** - Create `backend/.env`:
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/plagiarism-checker
AI_SERVICE_URL=http://localhost:8000
```

**AI Service** - Create `ai-service/.env`:
```env
PORT=8000
DEBUG=False
```

### 4. Start MongoDB

**Windows:**
```bash
mongod
```

**macOS/Linux:**
```bash
sudo systemctl start mongod
# or
mongod --dbpath /path/to/data
```

### 5. Run the Application

**Option A: Run all services together**
```bash
npm run dev
```

**Option B: Run services individually**

Terminal 1 (AI Service):
```bash
cd ai-service
python app.py
```

Terminal 2 (Backend):
```bash
cd backend
npm run dev
```

Terminal 3 (Frontend):
```bash
cd frontend
npm start
```

### 6. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **AI Service**: http://localhost:8000

## Verification

1. Check AI Service: Visit http://localhost:8000/health
2. Check Backend: Visit http://localhost:5000/api/health
3. Check Frontend: Visit http://localhost:3000

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `mongod`
- Check connection string in `backend/.env`

### AI Service Not Starting
- Verify Python dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available
- First run will download the model (may take a few minutes)

### Frontend Not Connecting
- Ensure backend is running on port 5000
- Check CORS settings
- Verify API URL in `frontend/src/services/api.js`

### Port Already in Use
- Change ports in `.env` files
- Or stop the service using the port

