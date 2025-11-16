# How to Start the AI Service

## Quick Start

1. **Open a new terminal/command prompt**

2. **Navigate to the ai-service folder:**
   ```bash
   cd "c:\Users\123\Desktop\Ai based Plagiarism\ai-service"
   ```

3. **Start the AI service:**
   ```bash
   python app.py
   ```

4. **Wait for it to start** - You should see:
   ```
   Initializing Plagiarism Detector...
   Loading model: all-MiniLM-L6-v2...
   Model loaded successfully
   Plagiarism Detector initialized successfully
    * Running on http://0.0.0.0:8000
   ```

5. **Keep this terminal open** - The AI service must stay running!

## Verify It's Working

Open a browser and go to: http://localhost:8000/health

You should see:
```json
{"status":"ok","message":"AI Plagiarism Detection Service is running","model_loaded":true}
```

## Important Notes

- **First run**: The model download may take 1-2 minutes
- **Keep the terminal open**: The service must stay running
- **If you see errors**: Check that all dependencies are installed:
  ```bash
  pip install flask flask-cors sentence-transformers scikit-learn textblob numpy pandas requests python-dotenv
  ```

## Troubleshooting

If you get "ModuleNotFoundError":
```bash
pip install -r requirements.txt
```

If port 8000 is already in use:
- Stop the other service using port 8000
- Or change the port in `ai-service/.env`:
  ```
  PORT=8001
  ```
- Then update `backend/.env`:
  ```
  AI_SERVICE_URL=http://localhost:8001
  ```

