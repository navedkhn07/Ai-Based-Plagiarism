# Development Guide

## Development Workflow

### Starting Development

1. **Start MongoDB**:
   ```bash
   mongod
   ```

2. **Start AI Service** (Terminal 1):
   ```bash
   cd ai-service
   python app.py
   ```

3. **Start Backend** (Terminal 2):
   ```bash
   cd backend
   npm run dev
   ```

4. **Start Frontend** (Terminal 3):
   ```bash
   cd frontend
   npm start
   ```

Or use the convenience script:
```bash
npm run dev
```

## Code Structure

### Frontend Development

**Components** (`frontend/src/components/`):
- `Header.js` - Navigation header
- `TextInput.js` - Text input with word/character count
- `Results.js` - Results display with similarity scores
- `LoadingSpinner.js` - Loading indicator

**Services** (`frontend/src/services/`):
- `api.js` - API client for backend communication

**Styling**:
- Tailwind CSS configured in `tailwind.config.js`
- Global styles in `index.css`
- Component-level styling using Tailwind classes

### Backend Development

**Routes** (`backend/routes/`):
- `check.js` - Main plagiarism check endpoint
- `plagiarism.js` - History and statistics endpoints

**Models** (`backend/models/`):
- `PlagiarismCheck.js` - MongoDB schema for check history

**Server** (`backend/server.js`):
- Express server setup
- Middleware configuration
- MongoDB connection

### AI Service Development

**Main Files**:
- `app.py` - Flask API application
- `plagiarism_detector.py` - Core detection logic

**Key Classes**:
- `PlagiarismDetector` - Main detection class
  - `detect_plagiarism()` - Main detection method
  - `detect_ai_generated()` - AI content detection
  - `extract_features()` - Feature extraction
  - `calculate_similarity()` - Similarity calculation

## Adding New Features

### Frontend Feature

1. Create component in `frontend/src/components/`
2. Import and use in `App.js` or relevant component
3. Add API calls in `frontend/src/services/api.js` if needed
4. Style with Tailwind CSS

### Backend Feature

1. Create route in `backend/routes/`
2. Add model in `backend/models/` if needed
3. Register route in `backend/server.js`
4. Test with Postman or similar tool

### AI Service Feature

1. Add method to `PlagiarismDetector` class
2. Add endpoint in `app.py` if needed
3. Test with Python or API client

## Testing

### Manual Testing

1. **Frontend**: Test UI components in browser
2. **Backend**: Test API endpoints with Postman
3. **AI Service**: Test with curl or Postman

### Example API Calls

**Check Plagiarism**:
```bash
curl -X POST http://localhost:5000/api/check \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

**Health Check**:
```bash
curl http://localhost:5000/api/health
```

**AI Service Health**:
```bash
curl http://localhost:8000/health
```

## Debugging

### Frontend Debugging

- Use React DevTools browser extension
- Check browser console for errors
- Verify API calls in Network tab

### Backend Debugging

- Check server console for errors
- Use `console.log()` for debugging
- Verify MongoDB connection
- Check environment variables

### AI Service Debugging

- Check Flask console output
- Verify model loading
- Test detection methods directly
- Check Python dependencies

## Common Issues

### Port Already in Use

**Solution**: Change port in `.env` file or stop the service using the port

### MongoDB Connection Error

**Solution**: 
- Ensure MongoDB is running: `mongod`
- Check connection string in `backend/.env`
- Verify MongoDB is accessible

### AI Service Not Responding

**Solution**:
- Verify Python dependencies: `pip install -r requirements.txt`
- Check if model downloads successfully
- Verify port 8000 is available
- Check Flask console for errors

### Frontend Not Connecting to Backend

**Solution**:
- Verify backend is running on port 5000
- Check CORS settings in `backend/server.js`
- Verify API URL in `frontend/src/services/api.js`
- Check browser console for errors

## Performance Optimization

### Frontend

- Use React.memo() for expensive components
- Lazy load components if needed
- Optimize images and assets

### Backend

- Add caching for frequently accessed data
- Optimize MongoDB queries
- Add rate limiting for production

### AI Service

- Cache model embeddings if possible
- Optimize text preprocessing
- Consider using faster models for production

## Environment Variables

### Backend (`backend/.env`)

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/plagiarism-checker
AI_SERVICE_URL=http://localhost:8000
```

### AI Service (`ai-service/.env`)

```env
PORT=8000
DEBUG=False
```

## Best Practices

1. **Code Organization**: Keep components modular and reusable
2. **Error Handling**: Add proper error handling in all layers
3. **Validation**: Validate input at both frontend and backend
4. **Security**: Add authentication and rate limiting for production
5. **Documentation**: Document API endpoints and functions
6. **Testing**: Write unit and integration tests
7. **Logging**: Add logging for debugging and monitoring

## Deployment Considerations

1. **Environment Variables**: Use environment variables for configuration
2. **Error Handling**: Implement comprehensive error handling
3. **Rate Limiting**: Add rate limiting for API endpoints
4. **Authentication**: Add authentication for production
5. **Monitoring**: Add logging and monitoring
6. **Security**: Implement security best practices
7. **Database**: Use production-grade database setup
8. **Caching**: Implement caching for better performance

