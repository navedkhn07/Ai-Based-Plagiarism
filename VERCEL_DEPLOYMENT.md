# Vercel Deployment Guide

This guide will help you deploy the AI-Based Plagiarism Checker to Vercel.

## 🔒 Security Warning

**⚠️ NEVER commit actual credentials to GitHub or any public repository!**

- Always use environment variables for sensitive data (MongoDB URIs, API keys, JWT secrets)
- Never hardcode passwords, connection strings, or secrets in your code
- Use `.env` files locally (already in `.gitignore`) and environment variables in production
- If you accidentally commit credentials, **immediately rotate/change them** in your services

## ⚠️ Important Notes

1. **AI Service (Python)**: The Python AI service cannot be deployed directly on Vercel. You'll need to deploy it separately on a platform that supports Python (e.g., Railway, Render, Heroku, or a VPS).

2. **Frontend & Backend**: The frontend (React) and backend (Node.js) can be deployed on Vercel.

## Prerequisites

- Vercel account (sign up at [vercel.com](https://vercel.com))
- MongoDB Atlas account (or your MongoDB connection string)
- Deployed AI Service URL (from Railway, Render, etc.)

## Step 1: Deploy AI Service Separately

> **📖 Detailed Guide**: See [AI_SERVICE_DEPLOYMENT.md](./AI_SERVICE_DEPLOYMENT.md) for complete step-by-step instructions.

Since Vercel doesn't support Python serverless functions for long-running services, deploy the AI service separately:

**Quick Answer**: Deploy on [Railway](https://railway.app) (recommended), [Render](https://render.com), or [Heroku](https://heroku.com), then copy the URL they provide. That URL is your `AI_SERVICE_URL`.

### Option A: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Add a new service and select "Deploy from GitHub repo"
5. Select the `ai-service` directory
6. Set environment variables:
   ```
   PORT=8000
   DEBUG=False
   ```
7. Railway will automatically detect Python and install dependencies
8. Copy the deployed URL (e.g., `https://your-app.railway.app`)

### Option B: Render
1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3
5. Add environment variables:
   ```
   PORT=8000
   DEBUG=False
   ```
6. Copy the deployed URL

### Option C: Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-ai-service-name`
4. Set environment variables:
   ```bash
   heroku config:set PORT=8000
   heroku config:set DEBUG=False
   ```
5. Deploy: `git push heroku main`
6. Copy the deployed URL

## Step 2: Set Up Environment Variables

### Backend Environment Variables (in Vercel)

1. Go to your Vercel project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

```
PORT=5000
MONGODB_URI=your-mongodb-connection-string
AI_SERVICE_URL=https://your-ai-service-url.com
JWT_SECRET=your-secure-random-secret-key
```

**⚠️ SECURITY WARNING**: Never commit actual credentials to GitHub! Always use environment variables.

**Where to get these values:**
- `MONGODB_URI`: Get from your MongoDB Atlas dashboard → Connect → Connection String
- `AI_SERVICE_URL`: Get from your deployed AI service (Railway/Render/Heroku) - see [AI_SERVICE_DEPLOYMENT.md](./AI_SERVICE_DEPLOYMENT.md)
- `JWT_SECRET`: Generate a secure random key (see below)

**To generate a secure JWT_SECRET:**
```bash
# On Linux/Mac
openssl rand -base64 32

# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

### Frontend Environment Variables (Optional)

If your backend is on a different domain, add:

```
REACT_APP_API_URL=https://your-backend-url.vercel.app/api
```

## Step 3: Deploy to Vercel

### Method 1: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Link to existing project? **No** (for first deployment)
   - Project name: **ai-based-plagiarism**
   - Directory: **./** (root)
   - Override settings? **No**

### Method 2: Using GitHub Integration (Recommended)

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: 
     ```
     cd frontend && npm install && npm run build
     ```
   - **Output Directory**: `frontend/build`
   - **Install Command**: 
     ```
     npm install && cd backend && npm install && cd ../frontend && npm install
     ```

5. Add environment variables (from Step 2)
6. Click "Deploy"

## Step 4: Update Frontend API URL

After deployment, update the frontend to use the production API URL:

1. In Vercel, go to your project settings
2. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend.vercel.app/api
   ```
3. Redeploy the frontend

Or update `frontend/src/services/api.js`:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend.vercel.app/api';
```

## Step 5: Configure Vercel.json (Optional)

The `vercel.json` file is already configured for you. It:
- Routes `/api/*` requests to the backend
- Serves the React frontend for all other routes
- Sets production environment

## Troubleshooting

### Backend Not Working
- Check that environment variables are set correctly in Vercel
- Verify MongoDB connection string is correct
- Check Vercel function logs for errors

### Frontend Not Loading
- Ensure build command completed successfully
- Check that `frontend/build` directory exists
- Verify output directory is set to `frontend/build`

### AI Service Connection Failed
- Verify AI service is deployed and accessible
- Check `AI_SERVICE_URL` environment variable
- Ensure AI service allows CORS from your Vercel domain

### CORS Errors
- Add your Vercel domain to CORS settings in backend
- Update `backend/server.js`:
  ```javascript
  app.use(cors({
    origin: ['https://your-app.vercel.app', 'http://localhost:3000']
  }));
  ```

## Environment Variables Summary

### Backend (.env in Vercel)
```
PORT=5000
MONGODB_URI=your-mongodb-connection-string
AI_SERVICE_URL=https://your-ai-service.railway.app
JWT_SECRET=your-secure-secret-key
```

**⚠️ IMPORTANT SECURITY NOTES:**
- **Never commit actual credentials to GitHub!** Always use placeholders in documentation.
- Replace `your-mongodb-connection-string` with your actual MongoDB Atlas connection string (get from MongoDB Atlas dashboard)
- Replace `your-ai-service.railway.app` with your actual deployed AI service URL
- Generate a secure `JWT_SECRET` using the commands provided above - never use the example value in production!

### AI Service (.env in Railway/Render/Heroku)
```
PORT=8000
DEBUG=False
```

### Frontend (Optional, in Vercel)
```
REACT_APP_API_URL=https://your-backend.vercel.app/api
```

## Post-Deployment Checklist

- [ ] AI Service is deployed and accessible
- [ ] Backend environment variables are set in Vercel
- [ ] MongoDB connection is working
- [ ] Frontend is building successfully
- [ ] API endpoints are accessible
- [ ] CORS is configured correctly
- [ ] JWT_SECRET is set to a secure value
- [ ] All services are communicating properly

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas Setup](https://www.mongodb.com/cloud/atlas)

---

**Note**: For production use, consider:
- Setting up a custom domain
- Enabling HTTPS (automatic with Vercel)
- Adding rate limiting
- Setting up monitoring and logging
- Implementing proper error handling

