# Deployment Guide - Full-Stack Todo App

This guide covers deploying your Todo app to production using:
- **Railway**: Backend API + PostgreSQL Database (Free tier)
- **Vercel**: Frontend (Free tier)

Total cost: **$0/month** on free tiers!

---

## Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- Vercel account (sign up at https://vercel.com)
- Git installed locally

---

## Part 1: Push Code to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Todo app ready for deployment"
   ```

2. **Create GitHub repository**:
   - Go to https://github.com/new
   - Name it `todo-app` (or your preferred name)
   - **DO NOT** initialize with README (we already have code)
   - Click "Create repository"

3. **Push code to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/todo-app.git
   git branch -M main
   git push -u origin main
   ```

---

## Part 2: Deploy Backend to Railway (with PostgreSQL)

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authenticate with GitHub and select your `todo-app` repository
5. Railway will detect your project

### Step 2: Add PostgreSQL Database

1. In your Railway project dashboard, click "**+ New**"
2. Select "**Database**" → "**PostgreSQL**"
3. Railway will provision a PostgreSQL database (takes ~30 seconds)
4. The database connection details are automatically generated

### Step 3: Configure Backend Service

1. Click on your backend service (should be auto-detected from Dockerfile)
2. If not auto-detected, click "**+ New**" → "**GitHub Repo**" → Select your repo
3. Set the **Root Directory** to `backend`
4. Go to **"Settings"** tab:
   - **Build**: Should detect Dockerfile automatically
   - **Deploy**: Start command should be from railway.json

### Step 4: Set Environment Variables

1. In backend service, click **"Variables"** tab
2. Click "**+ New Variable**"
3. Add the following variables:

   **DATABASE_URL** (Reference from PostgreSQL service):
   - Click "**+ New Variable**" → "**Add Reference**"
   - Select your PostgreSQL service
   - Choose `DATABASE_URL`
   - This automatically links your backend to the database

   **CORS_ORIGINS** (Manual):
   - Click "**+ New Variable**"
   - Key: `CORS_ORIGINS`
   - Value: `https://your-app.vercel.app` (we'll update this after Vercel deployment)
   - For now, use: `http://localhost:3000,https://*.vercel.app`

   **ENVIRONMENT** (Manual):
   - Key: `ENVIRONMENT`
   - Value: `production`

4. Click "**Deploy**" (Railway will rebuild with new environment variables)

### Step 5: Get Backend URL

1. Go to **"Settings"** → **"Networking"**
2. Click "**Generate Domain**"
3. Railway will generate a public URL like: `todo-backend-production-xxxx.up.railway.app`
4. **Copy this URL** - you'll need it for frontend deployment
5. Test it: Visit `https://YOUR_BACKEND_URL.up.railway.app/health`
   - Should return: `{"status": "healthy"}`
6. Test API docs: `https://YOUR_BACKEND_URL.up.railway.app/docs`

### Step 6: Verify Database Migration

1. Check deployment logs in Railway dashboard
2. Look for: `alembic upgrade head` in logs
3. Should see: `Running upgrade -> 001, Create tasks table`
4. Database is ready! ✅

---

## Part 3: Deploy Frontend to Vercel

### Step 1: Import Project to Vercel

1. Go to https://vercel.com/dashboard
2. Click "**Add New**" → "**Project**"
3. Import your GitHub repository (`todo-app`)
4. Vercel will detect Next.js automatically

### Step 2: Configure Build Settings

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: Click "**Edit**" → Enter `frontend`
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)

### Step 3: Set Environment Variables

1. Before clicking "Deploy", expand "**Environment Variables**"
2. Add the following:

   **NEXT_PUBLIC_API_URL**:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://YOUR_BACKEND_URL.up.railway.app` (from Part 2, Step 5)
   - Make sure to use **https://** and no trailing slash

3. Click "**Deploy**"

### Step 4: Get Frontend URL

1. Vercel will build and deploy (takes 1-2 minutes)
2. Once complete, you'll see: "**Congratulations! Your project has been deployed**"
3. Your frontend URL will be: `https://todo-app-xxxxx.vercel.app`
4. Click "**Visit**" to open your deployed app

### Step 5: Update CORS in Railway

1. Go back to Railway dashboard
2. Click on backend service → **"Variables"** tab
3. Find `CORS_ORIGINS` variable
4. Update value to: `https://your-app.vercel.app` (your actual Vercel URL)
5. Click "**Deploy**" to restart backend with new CORS settings

---

## Part 4: Test Your Deployed App

1. **Open your Vercel frontend URL**: `https://todo-app-xxxxx.vercel.app`

2. **Test functionality**:
   - ✅ Add a new task
   - ✅ Mark task as complete
   - ✅ Delete a task
   - ✅ Refresh page - tasks should persist

3. **Check API**:
   - Open: `https://YOUR_BACKEND_URL.up.railway.app/docs`
   - Try the interactive API endpoints

4. **Check database**:
   - Go to Railway → PostgreSQL service → **"Data"** tab
   - You should see your tasks in the `tasks` table

---

## Deployment Summary

### Your Production URLs

- **Frontend**: `https://todo-app-xxxxx.vercel.app`
- **Backend API**: `https://todo-backend-production-xxxx.up.railway.app`
- **API Docs**: `https://todo-backend-production-xxxx.up.railway.app/docs`
- **Database**: Managed by Railway (PostgreSQL)

### Free Tier Limits

**Railway Free Tier**:
- $5 in credits per month
- 512 MB RAM per service
- 1 GB disk space
- Enough for moderate usage

**Vercel Free Tier**:
- Unlimited deployments
- 100 GB bandwidth per month
- Automatic HTTPS
- Global CDN

### What Happens on Every Git Push

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

2. **Automatic Deployments**:
   - Railway: Rebuilds backend automatically
   - Vercel: Rebuilds frontend automatically

3. **Preview Deployments** (Vercel):
   - Every branch gets a preview URL
   - Test changes before merging to main

---

## Environment Variables Reference

### Backend (.env on Railway)

```env
DATABASE_URL=postgresql://user:pass@host:5432/db  # Auto-generated by Railway
CORS_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
```

### Frontend (.env.local on Vercel)

```env
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

---

## Monitoring and Logs

### Railway Backend Logs

1. Go to Railway dashboard
2. Click backend service
3. Click "**Deployments**" → Latest deployment
4. View real-time logs

### Vercel Frontend Logs

1. Go to Vercel dashboard
2. Click your project
3. Click "**Deployments**" → Latest deployment
4. Click "**View Function Logs**"

### Database Access (Railway)

1. Go to Railway → PostgreSQL service
2. Click "**Data**" tab to view tables
3. Or use connection string with any PostgreSQL client:
   ```bash
   psql "postgresql://user:pass@host:5432/db"
   ```

---

## Troubleshooting

### Frontend can't connect to backend

**Issue**: CORS errors or "Failed to fetch"

**Solutions**:
1. Verify `NEXT_PUBLIC_API_URL` in Vercel settings (no trailing slash)
2. Verify `CORS_ORIGINS` in Railway includes your Vercel URL
3. Redeploy both services after changing environment variables

### Database connection error

**Issue**: Backend logs show "could not connect to database"

**Solutions**:
1. Verify `DATABASE_URL` is referenced from PostgreSQL service
2. Check PostgreSQL service is running in Railway
3. Restart backend service

### 404 on API endpoints

**Issue**: Frontend shows 404 for `/api/todos`

**Solutions**:
1. Check backend logs for errors
2. Verify Docker build succeeded
3. Test API directly: `curl https://YOUR_BACKEND_URL/api/todos`

### Build failures

**Railway Backend**:
- Check `requirements.txt` has all dependencies
- Verify Python version (3.11)
- Check Dockerfile syntax

**Vercel Frontend**:
- Check `package.json` scripts
- Verify all dependencies are in `package.json`, not `package-lock.json` only
- Check for TypeScript errors

---

## Advanced: Custom Domains

### Add Custom Domain to Vercel

1. Buy domain (e.g., from Namecheap, Google Domains)
2. Vercel dashboard → Your project → **"Settings"** → **"Domains"**
3. Add your domain: `yourdomain.com`
4. Follow DNS configuration instructions
5. Vercel provides automatic HTTPS

### Add Custom Domain to Railway

1. Railway dashboard → Backend service → **"Settings"** → **"Networking"**
2. Click "**Custom Domain**"
3. Enter your subdomain: `api.yourdomain.com`
4. Add CNAME record to your DNS provider
5. Update `CORS_ORIGINS` in Railway to include new domain

---

## Rollback Deployment

### Railway

1. Go to **"Deployments"** tab
2. Find previous successful deployment
3. Click "**···**" → "**Redeploy**"

### Vercel

1. Go to **"Deployments"** tab
2. Find previous deployment
3. Click "**···**" → "**Promote to Production**"

---

## Cost Optimization

### Stay on Free Tier

1. **Monitor usage**:
   - Railway: Check usage in dashboard
   - Vercel: Check bandwidth usage

2. **Database optimization**:
   - Add indexes for frequently queried columns (already done in migration)
   - Clean up old completed tasks periodically

3. **Frontend optimization**:
   - Next.js automatically optimizes images and code splitting
   - Vercel's CDN caches static assets

### Upgrade if Needed

**Railway Pro** ($20/month):
- $20 in credits
- Better performance
- More storage

**Vercel Pro** ($20/month):
- Password protection
- Advanced analytics
- More bandwidth

---

## Security Best Practices

### Production Checklist

- ✅ HTTPS enabled (automatic on both platforms)
- ✅ Environment variables not in code
- ✅ Database connection encrypted (Railway default)
- ✅ CORS configured correctly
- ✅ No exposed secrets in GitHub

### Additional Security (Optional)

1. **Rate limiting**: Add middleware to FastAPI
2. **API authentication**: Add JWT tokens
3. **Input validation**: Already handled by Pydantic
4. **SQL injection protection**: Already handled by SQLModel

---

## Next Steps

After successful deployment:

1. **Share your app**: Send Vercel URL to friends
2. **Custom domain**: Add your own domain
3. **Monitoring**: Set up error tracking (e.g., Sentry)
4. **Analytics**: Add analytics (e.g., Vercel Analytics)
5. **CI/CD**: Already set up via Railway + Vercel auto-deploy
6. **Implement remaining features**: US4, US5, US6 from your spec

---

## Support

**Railway**:
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app

**Vercel**:
- Discord: https://vercel.com/discord
- Docs: https://vercel.com/docs

**Issues with this deployment**:
- Check logs first (Railway and Vercel dashboards)
- Verify environment variables
- Test API endpoints directly with curl/Postman

---

## Quick Reference Commands

### Local Development
```bash
# Backend
cd backend
.venv\Scripts\activate
uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
npm run dev
```

### Deploy Updates
```bash
git add .
git commit -m "Your update message"
git push
# Railway and Vercel auto-deploy!
```

### Check Production Logs
```bash
# Railway CLI (optional)
railway logs

# Or use web dashboard
```

---

## Success Checklist

- ✅ Code pushed to GitHub
- ✅ Backend deployed to Railway
- ✅ PostgreSQL database provisioned on Railway
- ✅ Frontend deployed to Vercel
- ✅ Environment variables configured
- ✅ CORS configured correctly
- ✅ Custom domains added (optional)
- ✅ App fully functional in production
- ✅ Auto-deploy on git push enabled

**Your app is live! 🚀**
