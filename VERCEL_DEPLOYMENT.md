# Quiz Mate - Vercel Deployment Guide

This guide covers deploying the Quiz Mate frontend to Vercel while hosting the backend separately.

## Architecture Overview

- **Frontend**: React app deployed to Vercel (static hosting)
- **Backend**: Node.js/Express server with Socket.IO (must be hosted elsewhere)

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Backend Hosting**: Choose a platform that supports WebSockets:
   - [Railway](https://railway.app) (recommended - easy setup)
   - [Render](https://render.com)
   - [Fly.io](https://fly.io)
   - Any VPS (DigitalOcean, AWS, etc.)

## Step 1: Deploy Backend

First, deploy the backend to a WebSocket-compatible platform. Here's an example for Railway:

### Option A: Railway (Recommended)

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `quiz-mate` repository
4. Railway will auto-detect the Node.js app
5. Configure the deployment:
   - **Root Directory**: `backend`
   - **Start Command**: `npm start`
   - **Port**: Railway will auto-assign (usually 3000)
6. Add environment variables if needed (check `backend/quiz-mate.cfg`)
7. Deploy and note your backend URL (e.g., `https://your-app.railway.app`)

### Option B: Render

1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: quiz-mate-backend
   - **Root Directory**: `backend`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
5. Deploy and note your backend URL

## Step 2: Configure Frontend for Backend URL

The frontend needs to know where to connect to the backend. You'll set this via Vercel environment variables.

Your backend URL will be something like:
- Railway: `https://quiz-mate-backend-production.up.railway.app`
- Render: `https://quiz-mate-backend.onrender.com`

## Step 3: Deploy Frontend to Vercel

### Option A: Vercel Dashboard (Easiest)

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your `quiz-mate` repository from GitHub
4. Vercel will auto-detect the configuration from `vercel.json`
5. **Important**: Add environment variable:
   - **Key**: `REACT_APP_BACKEND_URL`
   - **Value**: Your backend URL (e.g., `https://your-app.railway.app`)
6. Click "Deploy"

### Option B: Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? quiz-mate (or your preferred name)
# - In which directory is your code located? ./

# Add environment variable
vercel env add REACT_APP_BACKEND_URL

# When prompted, enter your backend URL
# Select all environments (Production, Preview, Development)

# Deploy to production
vercel --prod
```

## Step 4: Update Frontend Code (If Needed)

If the frontend doesn't already support the `REACT_APP_BACKEND_URL` environment variable, you'll need to update the Socket.IO connection code.

Check `frontend/src` for Socket.IO initialization and update it to use:

```javascript
const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:3001';
const socket = io(backendUrl);
```

## Step 5: Test Your Deployment

1. Visit your Vercel URL (e.g., `https://quiz-mate.vercel.app`)
2. Create a quiz and start hosting
3. Join from another device/browser
4. Verify real-time features work (player joining, answers, leaderboard)

## Configuration Files Created

- **`vercel.json`**: Vercel deployment configuration
  - Builds the frontend from the `frontend/` directory
  - Configures SPA routing (all routes → index.html)
  - Sets cache headers for static assets

- **`package.json`**: Root package file for Vercel
  - Defines build scripts
  - Repository metadata

- **`.vercelignore`**: Excludes backend and unnecessary files from deployment
  - Backend code is not deployed to Vercel
  - Only frontend build is deployed

## Troubleshooting

### Build Fails on Vercel

- Check the build logs in Vercel dashboard
- Ensure all frontend dependencies are in `frontend/package.json`
- Try building locally first: `cd frontend && npm install && npm run build`

### WebSocket Connection Fails

- Verify backend is running and accessible
- Check `REACT_APP_BACKEND_URL` environment variable in Vercel
- Ensure backend allows CORS from your Vercel domain
- Check backend logs for connection errors

### Players Can't Join Quiz

- Verify backend WebSocket server is running
- Check browser console for connection errors
- Ensure backend firewall allows WebSocket connections
- Test backend URL directly in browser

## Local Development

To run locally with the same setup:

```bash
# Terminal 1: Start backend
cd backend
npm install
npm start

# Terminal 2: Start frontend
cd frontend
npm install
REACT_APP_BACKEND_URL=http://localhost:3001 npm start
```

## Next Steps

1. **Custom Domain**: Add a custom domain in Vercel dashboard
2. **HTTPS**: Vercel provides automatic HTTPS, ensure backend also uses HTTPS
3. **Monitoring**: Set up monitoring for both frontend (Vercel Analytics) and backend
4. **Scaling**: Consider backend scaling options on your hosting platform

## Important Notes

- **Backend must stay running**: The backend stores quiz state in memory
- **No database required**: Quiz data is stored in JSON files and memory
- **WebSocket requirement**: Backend must support persistent connections
- **CORS**: Backend may need CORS configuration for your Vercel domain
