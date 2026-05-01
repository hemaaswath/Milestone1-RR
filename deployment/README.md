# Restaurant Recommendation System - Production Deployment

## 🚀 Free Deployment Setup

This folder contains production-ready configurations for deploying the restaurant recommendation system using free tools.

## 📁 Files Overview

### Backend Files (Railway Deployment)
- `app.py` - Production Flask backend
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `railway.json` - Railway deployment settings

### Frontend Files (Vercel Deployment)
- `package.json` - Node.js dependencies
- `vercel.json` - Vercel deployment settings

## 🛠️ Quick Start

### 1. Deploy Backend (Railway)
1. Push code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Connect GitHub repository
4. Select this folder as root
5. Add environment variable: `GROQ_API_KEY=your_key_here`
6. Deploy

### 2. Deploy Frontend (Vercel)
1. Go to [Vercel.com](https://vercel.com)
2. Connect GitHub repository
3. Select this folder as root
4. Add environment variable: `VITE_API_BASE_URL=https://your-backend-url.up.railway.app`
5. Deploy

### 3. Update CORS
In Railway, update `app.py` line 12:
```python
CORS(app, origins=["https://your-frontend-domain.vercel.app"])
```

## 🔧 Environment Variables

### Backend (Railway)
```
GROQ_API_KEY=your_groq_api_key
PORT=8000
```

### Frontend (Vercel)
```
VITE_API_BASE_URL=https://your-backend-url.up.railway.app
```

## 📊 Free Tier Limits

- **Railway**: 500 hours/month (~21 days continuous)
- **Vercel**: Unlimited static sites
- **Groq API**: Free tier with rate limits

## 🎯 Expected URLs

After deployment:
- Frontend: `https://your-app-name.vercel.app`
- Backend: `https://your-app-name.up.railway.app`
- API Health: `https://your-app-name.up.railway.app/api/v1/health`

## 🔍 Testing

1. Test backend health: `/api/v1/health`
2. Test frontend loads
3. Test complete recommendation workflow
4. Verify CORS configuration

## 📞 Support

- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- Check platform logs for issues
