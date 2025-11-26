# AI Service Deployment Guide

This guide will help you deploy the Python AI service separately, which is required because Vercel doesn't support long-running Python services.

## Why Deploy Separately?

The AI service is a Python Flask application that needs to run continuously. Vercel is designed for serverless functions, not long-running services. You need to deploy it on a platform that supports Python applications.

## Quick Start - Railway (Easiest Option) 🚀

### Step 1: Sign Up for Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account (recommended)

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `navedkhn07/Ai-Based-Plagiarism`
4. Railway will detect your repository

### Step 3: Add Service
1. Click "New Service"
2. Select "GitHub Repo"
3. Choose your repository again
4. **Important**: In the settings, set the **Root Directory** to: `ai-service`

### Step 4: Configure Environment Variables
1. Go to your service settings
2. Click on "Variables" tab
3. Add these environment variables:
   ```
   PORT=8000
   DEBUG=False
   ```

### Step 5: Deploy
1. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Start the service with `python app.py`
2. Wait for deployment to complete (usually 2-5 minutes)

### Step 6: Get Your AI Service URL
1. Once deployed, Railway will provide a URL like:
   - `https://your-app-name.up.railway.app`
   - Or `https://your-app-name.railway.app`
2. **Copy this URL** - this is your `AI_SERVICE_URL`!

### Step 7: Test Your AI Service
1. Visit: `https://your-ai-service-url.railway.app/health`
2. You should see: `{"status":"ok","message":"AI Plagiarism Detection Service is running"}`
3. If you see this, your service is working! ✅

---

## Alternative: Render

### Step 1: Sign Up
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select: `navedkhn07/Ai-Based-Plagiarism`

### Step 3: Configure
- **Name**: `ai-plagiarism-service` (or any name)
- **Root Directory**: `ai-service`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### Step 4: Environment Variables
Add in the "Environment" section:
```
PORT=8000
DEBUG=False
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. **Copy the URL** provided (e.g., `https://ai-plagiarism-service.onrender.com`)

---

## Alternative: Heroku

### Step 1: Install Heroku CLI
Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### Step 2: Login
```bash
heroku login
```

### Step 3: Create App
```bash
cd ai-service
heroku create your-ai-service-name
```

### Step 4: Set Environment Variables
```bash
heroku config:set PORT=8000
heroku config:set DEBUG=False
```

### Step 5: Deploy
```bash
git push heroku main
```

### Step 6: Get URL
```bash
heroku info
```
The URL will be: `https://your-ai-service-name.herokuapp.com`

---

## After Deployment

Once you have your AI service URL, use it in Vercel:

1. Go to your Vercel project
2. Settings → Environment Variables
3. Update `AI_SERVICE_URL`:
   ```
   AI_SERVICE_URL=https://your-ai-service.railway.app
   ```
   (Replace with your actual URL)

4. Redeploy your Vercel project

---

## Troubleshooting

### Service Not Starting
- Check the logs in Railway/Render/Heroku dashboard
- Ensure `requirements.txt` is in the `ai-service` directory
- Verify Python version (3.8+)

### Health Check Fails
- Check if port is set correctly (8000)
- Verify all dependencies are installed
- Check service logs for errors

### Connection Timeout
- Ensure the service is running (not sleeping)
- Check if CORS is configured in `app.py` (already done)
- Verify the URL is correct

### Model Download Issues
- The Sentence-Transformers model downloads automatically on first run
- This may take a few minutes on first deployment
- Check logs to see download progress

---

## Free Tier Limits

### Railway
- $5 free credit monthly
- Sleeps after inactivity (wakes on request)
- Good for development/testing

### Render
- Free tier available
- Sleeps after 15 minutes of inactivity
- Slower cold starts

### Heroku
- No longer has free tier
- Paid plans start at $7/month

**Recommendation**: Use Railway for easiest deployment and good free tier.

---

## Example URLs

After deployment, your URLs will look like:

- **Railway**: `https://ai-plagiarism-service-production.up.railway.app`
- **Render**: `https://ai-plagiarism-service.onrender.com`
- **Heroku**: `https://your-app-name.herokuapp.com`

Copy the exact URL and use it as your `AI_SERVICE_URL` in Vercel!

---

## Next Steps

1. ✅ Deploy AI service (Railway recommended)
2. ✅ Copy the deployed URL
3. ✅ Add `AI_SERVICE_URL` to Vercel environment variables
4. ✅ Deploy backend and frontend on Vercel
5. ✅ Test the complete application

Need help? Check the deployment logs in your chosen platform's dashboard.

