# 🚀 Deploy to Vercel - Step by Step Guide

## Prerequisites

- GitHub account
- Vercel account (free)
- OMDb API key (free from https://www.omdbapi.com/apikey.aspx)

## 📋 Deployment Steps

### 1. **Prepare Your Repository**

```bash
# Make sure you're in your project directory
cd "New Movie Project"

# Add all files to Git
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. **Get OMDb API Key**

1. Visit https://www.omdbapi.com/apikey.aspx
2. Choose "FREE! (1,000 daily limit)"
3. Enter your email and get your API key
4. Save it - you'll need it for Vercel

### 3. **Deploy to Vercel**

#### Option A: Via Vercel Dashboard (Recommended)

1. Go to https://vercel.com
2. Sign up/Login with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect it as a Python project
6. **Important**: In Environment Variables section, add:
   - Name: `OMDB_API_KEY`
   - Value: `your_actual_api_key_here`
7. Click "Deploy"

#### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (choose your account)
# - Link to existing project? N
# - What's your project's name? movie-recommender
# - In which directory is your code? ./
```

### 4. **Add Environment Variables**

After deployment, go to your Vercel dashboard:

1. Select your deployed project
2. Go to "Settings" → "Environment Variables"
3. Add: `OMDB_API_KEY` = `your_actual_api_key`
4. Redeploy if needed

### 5. **Custom Domain (Optional)**

- In Vercel dashboard → "Domains"
- Add your custom domain or use the provided vercel.app URL

## 📁 Files Created for Deployment

- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- `vercel_app.py` - Entry point for Vercel
- `.env.example` - Environment variables template

## 🔒 Security Notes

- Never commit your `.env` file to Git
- Use Vercel's environment variables for production
- The `.env.example` file helps others understand what variables are needed

## 🎯 After Deployment

Your app will be available at: `https://your-app-name.vercel.app`

### Features that work on Vercel:

✅ Glassmorphism UI  
✅ OMDb API integration  
✅ Movie recommendations  
✅ Interactive sorting  
✅ Responsive design  
✅ All animations and effects

## 🆓 Vercel Free Tier Limits

- 100 GB bandwidth per month
- 100 serverless function executions per day
- 6000 serverless function execution hours per month
- Perfect for personal projects and testing!

## 🛠️ Troubleshooting

- If deployment fails, check the build logs in Vercel dashboard
- Make sure `OMDB_API_KEY` environment variable is set
- Verify all files are committed to your Git repository

---

**Your beautiful glassmorphism movie recommendation app will be live on Vercel! 🎬✨**
