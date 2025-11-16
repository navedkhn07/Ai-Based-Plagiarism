# AI Plagiarism Detection Service

Python-based AI service for detecting plagiarism using Sentence-Transformers and NLP.

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy English model (optional but recommended):
```bash
python -m spacy download en_core_web_sm
```

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Run the service:
```bash
python app.py
```

The service will run on `http://localhost:8000` by default.

## API Endpoints

### Health Check
- **GET** `/health`
- Returns service status and model information

### Check Plagiarism
- **POST** `/check`
- Body: `{ "text": "Your text here" }`
- Returns plagiarism detection results

## Model Information

The service uses `all-MiniLM-L6-v2` by default, which is a lightweight but effective model for semantic similarity. You can change this in `plagiarism_detector.py`.

