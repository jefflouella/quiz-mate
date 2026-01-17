# Quiz Mate - Railway + Vercel Deployment Guide

Complete guide for deploying Quiz Mate with the backend on Railway and frontend on Vercel.

## 🚀 Quick Start

**Total deployment time: ~10 minutes**

1. Deploy backend to Railway (5 min)
2. Deploy frontend to Vercel (5 min)
3. Test your quiz app!

---

## Part 1: Deploy Backend to Railway

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click "Login" and sign in with GitHub
3. Authorize Railway to access your GitHub account

### Step 2: Deploy Backend

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `quiz-mate` repository
4. Railway will detect it as a Node.js app

### Step 3: Configure Backend Deployment

Railway should auto-detect the configuration, but verify these settings:

1. Click on your deployment
2. Go to **Settings** tab
3. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `npm start` (should auto-detect)
   - **Build Command**: Leave empty (not needed)

### Step 4: Get Your Backend URL

1. Go to the **Settings** tab
2. Scroll to **Networking** section
3. Click **"Generate Domain"**
4. Copy your Railway URL (e.g., `https://quiz-mate-backend-production.up.railway.app`)

**Save this URL - you'll need it for Vercel!**

### Step 5: Verify Backend is Running

1. Visit your Railway URL in a browser
2. You should see the Quiz Mate interface (this is expected - it serves the frontend too)
3. Check the **Deployments** tab to ensure it's running successfully

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Click "Sign Up" and use GitHub
3. Authorize Vercel to access your GitHub account

### Step 2: Import Project

1. Click **"Add New..."** → **"Project"**
2. Find and import your `quiz-mate` repository
3. Vercel will auto-detect the configuration from `vercel.json`

### Step 3: Configure Environment Variable

**CRITICAL STEP:** Tell the frontend where to find the backend

1. Before clicking "Deploy", expand **"Environment Variables"**
2. Add a new variable:
   - **Name**: `REACT_APP_BACKEND_URL`
   - **Value**: Your Railway URL (e.g., `https://quiz-mate-backend-production.up.railway.app`)
   - **Environments**: Check all three (Production, Preview, Development)
3. Click **"Deploy"**

### Step 4: Wait for Deployment

Vercel will:
1. Install dependencies
2. Build the React app
3. Deploy to their CDN

This takes 2-3 minutes.

### Step 5: Get Your Frontend URL

Once deployed, Vercel will show your URL:
- Default: `https://quiz-mate.vercel.app` (or similar)
- You can add a custom domain later

---

## Part 3: Test Your Deployment

### Test the Full Flow

1. **Open your Vercel URL** in a browser
2. Click **"Host a quiz"**
3. Upload a quiz JSON file (or create one in the editor)
4. Start the quiz and note the room code
5. **Open a new browser tab** (or use your phone)
6. Join the quiz using the room code
7. **Verify real-time features work:**
   - Player count updates on host screen
   - Questions appear on player screen
   - Answers are submitted and counted
   - Leaderboard updates

If all of this works, **congratulations!** 🎉 Your quiz app is fully deployed.

---

## Configuration Files Explained

### `vercel.json`
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/build",
  ...
}
```
- Tells Vercel to build only the frontend
- Sets the output directory to `frontend/build`
- Configures SPA routing (all routes → index.html)

### `frontend/src/connection/config.js`
```javascript
export const server = process.env.REACT_APP_BACKEND_URL || ...
```
- Checks for `REACT_APP_BACKEND_URL` environment variable
- Falls back to localhost for development
- Falls back to same domain if not specified

---

## Environment Variables

### Vercel (Frontend)

| Variable | Value | Purpose |
|----------|-------|---------|
| `REACT_APP_BACKEND_URL` | Your Railway URL | Tells frontend where backend is hosted |

### Railway (Backend)

No environment variables needed for basic setup. The backend uses default configuration from `backend/quiz-mate.cfg`.

---

## Updating Your Deployment

### Update Frontend

```bash
# Make changes to frontend code
git add .
git commit -m "Update frontend"
git push

# Vercel auto-deploys on push to main branch
```

### Update Backend

```bash
# Make changes to backend code
git add .
git commit -m "Update backend"
git push

# Railway auto-deploys on push to main branch
```

Both platforms support **automatic deployments** from GitHub!

---

## Custom Domains

### Add Custom Domain to Vercel

1. Go to your project in Vercel
2. Click **Settings** → **Domains**
3. Add your domain (e.g., `quiz.yourdomain.com`)
4. Follow DNS configuration instructions

### Add Custom Domain to Railway

1. Go to your project in Railway
2. Click **Settings** → **Networking**
3. Add custom domain
4. Update DNS records as instructed

---

## Troubleshooting

### Frontend loads but can't connect to backend

**Symptom**: Players can't join, no real-time updates

**Solution**:
1. Check Vercel environment variables
2. Verify `REACT_APP_BACKEND_URL` is set correctly
3. Ensure Railway backend is running (check Deployments tab)
4. Check browser console for WebSocket errors

### Railway backend won't start

**Symptom**: Deployment fails or crashes

**Solution**:
1. Check Railway logs (Deployments → View Logs)
2. Verify `backend/package.json` has correct start script
3. Ensure Root Directory is set to `backend`
4. Check for port conflicts (Railway auto-assigns ports)

### Build fails on Vercel

**Symptom**: Deployment fails during build

**Solution**:
1. Check build logs in Vercel
2. Test build locally: `cd frontend && npm install && npm run build`
3. Ensure all dependencies are in `frontend/package.json`
4. Check for Node.js version compatibility

### CORS errors

**Symptom**: Browser shows CORS policy errors

**Solution**:
Railway backend already allows CORS from all origins (see `backend/src/express.js`). If you still see errors:
1. Check Railway logs for CORS-related messages
2. Verify backend URL is correct (no trailing slash)
3. Ensure backend is using HTTPS (Railway provides this automatically)

---

## Cost

Both platforms offer generous free tiers:

- **Railway**: Free tier includes 500 hours/month (enough for testing)
- **Vercel**: Free tier includes unlimited deployments for personal projects

For production use with high traffic, you may need paid plans.

---

## Local Development

To develop locally with the same setup:

```bash
# Terminal 1: Start backend
cd backend
npm install
npm start
# Backend runs on http://localhost:3001

# Terminal 2: Start frontend  
cd frontend
npm install
npm start
# Frontend runs on http://localhost:3000
# Automatically connects to localhost:3001
```

The frontend automatically detects development mode and connects to `localhost:3001`.

---

## Next Steps

- ✅ **Add custom domains** for professional URLs
- ✅ **Set up monitoring** (Railway and Vercel both provide analytics)
- ✅ **Create quiz content** using the built-in editor
- ✅ **Share your quiz app** with friends and colleagues!

---

## Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Quiz Mate Issues**: [github.com/jefflouella/quiz-mate/issues](https://github.com/jefflouella/quiz-mate/issues)
