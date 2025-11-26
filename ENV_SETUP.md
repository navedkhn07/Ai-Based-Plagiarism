# Environment Variables Setup Guide

This guide will help you set up your environment variables securely. **Never commit your actual credentials to GitHub!**

## Quick Setup

### 1. Backend Environment Variables

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file (copy from example):
   ```bash
   # On Windows (PowerShell)
   Copy-Item .env.example .env
   
   # On Mac/Linux
   cp .env.example .env
   ```

3. Open the `.env` file and add your actual values:
   ```env
   PORT=5000
   MONGODB_URI=your-actual-mongodb-connection-string-here
   AI_SERVICE_URL=http://localhost:8000
   JWT_SECRET=your-secure-random-secret-key-here
   ```

### 2. AI Service Environment Variables

1. Navigate to the `ai-service` directory:
   ```bash
   cd ai-service
   ```

2. Create a `.env` file:
   ```bash
   # On Windows (PowerShell)
   Copy-Item .env.example .env
   
   # On Mac/Linux
   cp .env.example .env
   ```

3. Open the `.env` file:
   ```env
   PORT=8000
   DEBUG=False
   ```

## Where to Get Your MongoDB URI

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Log in to your account
3. Click on your cluster
4. Click **"Connect"** button
5. Choose **"Connect your application"**
6. Copy the connection string (it looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
7. Replace `<password>` with your actual database password
8. Paste it into your `backend/.env` file as `MONGODB_URI`

**Example:**
```env
MONGODB_URI=mongodb+srv://myuser:mypassword123@cluster0.xxxxx.mongodb.net/
```

## Generate JWT Secret

### Windows (PowerShell):
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

### Mac/Linux:
```bash
openssl rand -base64 32
```

Copy the output and use it as your `JWT_SECRET` in `backend/.env`.

## Verify Setup

1. Make sure `.env` files are in `.gitignore` (they already are ✅)
2. Never commit `.env` files to Git
3. Your MongoDB URI should **only** be in your local `.env` file
4. The code reads from `process.env.MONGODB_URI` - no hardcoded values ✅

## Security Checklist

- ✅ `.env` files are in `.gitignore`
- ✅ No hardcoded credentials in code
- ✅ All sensitive data uses environment variables
- ✅ Documentation uses placeholders only
- ⚠️ **Never share your `.env` file with anyone**
- ⚠️ **Never commit `.env` files to Git**

## Troubleshooting

### "MONGODB_URI environment variable is not set!"
- Make sure you created `backend/.env` file
- Verify the file is named exactly `.env` (not `.env.txt`)
- Check that `MONGODB_URI=...` is in the file
- Restart your backend server after creating/updating `.env`

### MongoDB Connection Fails
- Verify your MongoDB URI is correct
- Check if your IP is whitelisted in MongoDB Atlas
- Ensure your password doesn't have special characters that need URL encoding
- Test the connection string in MongoDB Compass first

---

**Remember**: Your MongoDB connection string is **only** in your local `.env` file, which is **never** committed to GitHub. This keeps your credentials secure! 🔒

