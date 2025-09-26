# 🚀 Deploy to Render - Complete Guide

## Prerequisites

- GitHub account
- Render account (free at https://render.com)
- OMDb API key (free from https://www.omdbapi.com/apikey.aspx)

## 📋 Deployment Steps

### 1. **Prepare Your Repository**

```bash
# Make sure you're in your project directory
cd "New Movie Project"

# Add all files to Git
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. **Get OMDb API Key**

1. Visit https://www.omdbapi.com/apikey.aspx
2. Choose "FREE! (1,000 daily limit)"
3. Enter your email and get your API key
4. Save it - you'll need it for Render

### 3. **Deploy to Render**

#### Option A: Using render.yaml (Recommended)

1. Go to https://render.com and sign up/login
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to create the service

#### Option B: Manual Web Service Creation

1. Go to https://render.com and sign up/login
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: movie-recommender
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - **Plan**: Free

### 4. **Add Environment Variables**

In your Render service dashboard:

1. Go to "Environment" tab
2. Add these variables:
   - `OMDB_API_KEY` = your_actual_omdb_api_key
   - `FLASK_ENV` = production
   - `SECRET_KEY` = your_random_secret_key_here

### 5. **Deploy and Access**

- Your app will be available at: `https://your-app-name.onrender.com`
- First deployment takes 2-5 minutes
- Health check available at: `/health`

## 📁 Files Created for Render Deployment

- `render.yaml` - Render service configuration
- `Procfile` - Alternative deployment configuration
- `requirements.txt` - Updated with gunicorn
- `/health` endpoint - Health check for monitoring

## 🔒 Security & Configuration

- `.env` file is for local development only (not deployed)
- Environment variables are set in Render dashboard
- Flask app configured for production mode
- Gunicorn handles multiple workers for better performance

## 🎯 After Deployment

Your movie recommendation app will be live with:

### ✅ Features that work on Render:

- Beautiful glassmorphism UI
- OMDb API integration
- Movie recommendations (15 movies)
- Interactive sorting and filtering
- Responsive design
- All animations and effects
- Enhanced text readability
- Custom error pages

## 🆓 Render Free Tier Benefits

- **750 hours/month** of runtime (enough for personal projects)
- **Custom domains** supported
- **Automatic HTTPS**
- **Global CDN**
- **Auto-deploy** from GitHub
- **Build & deployment logs**

## 🛠️ Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **App won't start**: Verify the start command is `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
3. **API errors**: Ensure `OMDB_API_KEY` environment variable is set correctly
4. **500 errors**: Check the logs in Render dashboard

### Debug Commands:

```bash
# Test locally with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Check if health endpoint works
curl http://localhost:5000/health
```

## 📊 Monitoring

- Use `/health` endpoint for uptime monitoring
- Check Render dashboard for performance metrics
- View logs for debugging issues

## 🔄 Auto-Deploy Setup

Render automatically deploys when you push to your main branch:

```bash
git add .
git commit -m "Update feature"
git push origin main
# Render will automatically deploy!
```

---

**Your glassmorphism movie recommendation app is now production-ready on Render! 🎬✨**

### Live Features:

- ✅ Real-time movie recommendations
- ✅ Stunning glassmorphism design
- ✅ Interactive UI with purple-maroon-pink theme
- ✅ Mobile responsive
- ✅ Production-optimized performance
