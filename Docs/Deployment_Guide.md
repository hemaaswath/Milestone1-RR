# Phase 6 + Phase 7 Deployment Guide

## 🚀 Free Deployment Options

This guide covers how to deploy the restaurant recommendation system using completely free tools and platforms.

## 📋 Deployment Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend       │    │   Backend        │    │   External API  │
│   (Vercel)       │◄──►│   (Railway)      │◄──►│   (Groq API)    │
│   React/Vite     │    │   Flask/Python   │    │   LLM Service   │
│   Port 443       │    │   Port 443       │    │   HTTPS         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └──────────────────────┴──────────────────────┘
                        HTTPS/API Communication
```

## 🌟 Recommended Free Stack

### **Frontend**: Vercel (Free Tier)
- ✅ Unlimited static sites
- ✅ Custom domains
- ✅ HTTPS automatically
- ✅ Global CDN
- ✅ GitHub integration
- ✅ Automatic deployments

### **Backend**: Railway (Free Tier)
- ✅ 1 service free
- ✅ 500 hours/month
- ✅ Custom domains
- ✅ HTTPS automatically
- ✅ Environment variables
- ✅ GitHub integration

### **Alternative Options**
- **Frontend**: Netlify, GitHub Pages, Cloudflare Pages
- **Backend**: Render (free tier), Heroku (free tier), Fly.io (free tier)

---

## 🛠️ Step-by-Step Deployment Process

### **Phase 1: Prepare Your Code for Deployment**

#### 1.1 Create Production-Ready Backend
```bash
# Create production backend file
cd "c:/Users/Family/Documents/Milestone1-Build Hours"
mkdir deployment
cd deployment
```

Create `deployment/requirements.txt`:
```txt
flask==2.3.3
flask-cors==4.0.0
requests==2.31.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

Create `deployment/app.py` (Production Backend):
```python
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://your-frontend-domain.vercel.app"])

@app.route('/api/v1/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "phase": "6",
        "checks": {
            "api": "healthy",
            "groq_api": "configured" if os.getenv("GROQ_API_KEY") else "missing"
        }
    })

@app.route('/api/v1/meta')
def meta():
    return jsonify({
        "status": "success",
        "data": {
            "api_version": "1.0.0",
            "phase": "6",
            "available_locations": ["Bellandur", "Delhi", "Mumbai", "Bangalore", "Hyderabad"],
            "available_cuisines": ["North Indian", "Chinese", "Italian", "South Indian", "Continental"],
            "budget_options": ["low", "medium", "high"]
        }
    })

@app.route('/api/v1/locations')
def locations():
    return jsonify({
        "status": "success",
        "data": {
            "locations": ["Bellandur", "Delhi", "Mumbai", "Bangalore", "Hyderabad"]
        }
    })

@app.route('/api/v1/cuisines')
def cuisines():
    return jsonify({
        "status": "success",
        "data": {
            "cuisines": ["North Indian", "Chinese", "Italian", "South Indian", "Continental"]
        }
    })

@app.route('/api/v1/recommendations', methods=['POST'])
def recommendations():
    try:
        data = request.get_json() or {}
        
        if not data.get('location'):
            return jsonify({
                "status": "error",
                "message": "Location is required"
            }), 400
        
        if not data.get('budget'):
            return jsonify({
                "status": "error", 
                "message": "Budget is required"
            }), 400
        
        # Mock recommendations (replace with actual LLM call)
        location = data.get('location')
        budget = data.get('budget')
        top_k = min(int(data.get('top_k', 3)), 5)
        
        recommendations = []
        for i in range(top_k):
            recommendations.append({
                "restaurant_name": f"Restaurant {i+1} - {location}",
                "rank": i + 1,
                "score": 0.95 - (i * 0.1),
                "explanation": f"Great option in {location} for {budget} budget",
                "location": location,
                "cuisines": data.get('cuisine', 'Various'),
                "rating": 4.5 - (i * 0.1),
                "cost_for_two": 800 if budget == "medium" else (500 if budget == "low" else 1200)
            })
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "recommendations": recommendations,
                "summary": {
                    "total_candidates": 10,
                    "filtered_candidates": 5,
                    "final_recommendations": len(recommendations)
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
```

Create `deployment/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
```

Create `deployment/railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/api/v1/health"
  }
}
```

#### 1.2 Create Production-Ready Frontend
Create `deployment/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "VITE_API_BASE_URL": "@backend_url"
  }
}
```

Update `deployment/package.json`:
```json
{
  "name": "restaurant-recommendations-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.48.2",
    "react-hot-toast": "^2.4.1",
    "react-query": "^3.39.3"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.1",
    "vite": "^4.5.0",
    "tailwindcss": "^3.3.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31"
  }
}
```

---

### **Phase 2: Set Up GitHub Repository**

#### 2.1 Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Create new repository: `restaurant-recommendations`
3. Make it public (required for free tiers)
4. Initialize with README.md

#### 2.2 Push Your Code
```bash
cd "c:/Users/Family/Documents/Milestone1-Build Hours"
git init
git add .
git commit -m "Initial commit - Phase 6 + Phase 7 restaurant recommendations"
git branch -M main
git remote add origin https://github.com/yourusername/restaurant-recommendations.git
git push -u origin main
```

#### 2.3 Repository Structure
```
restaurant-recommendations/
├── deployment/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── railway.json
│   ├── vercel.json
│   └── package.json
├── phase7/frontend/
├── scripts/
├── src/
└── README.md
```

---

### **Phase 3: Deploy Backend to Railway**

#### 3.1 Sign Up for Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub (free)
3. Get $5 free credit (enough for deployment)

#### 3.2 Create Backend Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `restaurant-recommendations` repository
4. Select "deployment" folder as root directory
5. Railway will automatically detect the Dockerfile

#### 3.3 Configure Environment Variables
1. Go to your project settings
2. Add environment variables:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   PORT=8000
   ```

#### 3.4 Deploy Backend
1. Click "Deploy"
2. Wait for deployment (2-3 minutes)
3. Get your backend URL: `https://your-app-name.up.railway.app`
4. Test: `https://your-app-name.up.railway.app/api/v1/health`

---

### **Phase 4: Deploy Frontend to Vercel**

#### 4.1 Sign Up for Vercel
1. Go to [Vercel.com](https://vercel.com)
2. Sign up with GitHub (free)
3. Unlimited deployments on free tier

#### 4.2 Create Frontend Project
1. Click "New Project"
2. Import your `restaurant-recommendations` repository
3. Select "deployment" folder as root directory
4. Vercel will automatically detect the framework

#### 4.3 Configure Environment Variables
1. Go to project settings
2. Add environment variable:
   ```
   VITE_API_BASE_URL=https://your-backend-url.up.railway.app
   ```

#### 4.4 Deploy Frontend
1. Click "Deploy"
2. Wait for deployment (1-2 minutes)
3. Get your frontend URL: `https://your-app-name.vercel.app`
4. Test the complete application

---

### **Phase 5: Configure CORS and Final Setup**

#### 5.1 Update Backend CORS
In your Railway backend, update the CORS origins:
```python
# In deployment/app.py
CORS(app, origins=["https://your-frontend-domain.vercel.app"])
```

#### 5.2 Test Complete System
1. Visit your frontend URL
2. Test the complete recommendation workflow
3. Verify API communication works
4. Check all features are functional

---

## 🔄 Alternative Deployment Options

### **Option 1: Render (Backend) + Vercel (Frontend)**
- **Render**: Free tier with 750 hours/month
- **Similar setup to Railway**
- **Slightly more generous free tier**

### **Option 2: Netlify (Frontend) + Railway (Backend)**
- **Netlify**: Excellent static site hosting
- **Form handling available**
- **Edge functions for serverless**

### **Option 3: GitHub Pages (Frontend) + Railway (Backend)**
- **GitHub Pages**: Completely free static hosting
- **Limited to static sites only**
- **Good for simple frontend**

---

## 🛡️ Security Considerations

### **Environment Variables**
- Never commit API keys to repository
- Use platform environment variables
- Rotate keys regularly

### **CORS Configuration**
- Only allow your frontend domain
- Use HTTPS in production
- Validate all inputs

### **Rate Limiting**
- Implement rate limiting on backend
- Use platform features if available
- Monitor API usage

---

## 📊 Cost Analysis

### **Free Tier Limits**
- **Vercel**: Unlimited static sites
- **Railway**: 500 hours/month (~21 days continuous)
- **Groq API**: Free tier with limits
- **GitHub**: Unlimited public repos

### **Estimated Monthly Costs**
- **Development**: $0 (free tiers)
- **Light Production**: $0-10 (if exceeds free limits)
- **Heavy Production**: $10-50 (paid tiers)

---

## 🔧 Maintenance and Updates

### **Automated Deployments**
- Connect GitHub to both platforms
- Auto-deploy on main branch push
- Use pull requests for testing

### **Monitoring**
- Railway provides basic monitoring
- Vercel provides analytics
- Set up uptime monitoring (UptimeRobot free)

### **Backups**
- GitHub serves as code backup
- Export configuration regularly
- Document environment variables

---

## 🚀 Quick Deployment Checklist

### **Pre-Deployment**
- [ ] Test locally with production settings
- [ ] Create GitHub repository
- [ ] Set up environment variables
- [ ] Create deployment configurations

### **Backend Deployment**
- [ ] Deploy to Railway
- [ ] Configure environment variables
- [ ] Test API endpoints
- [ ] Set up CORS correctly

### **Frontend Deployment**
- [ ] Deploy to Vercel
- [ ] Configure API URL
- [ ] Test complete application
- [ ] Verify all features work

### **Post-Deployment**
- [ ] Test complete user workflow
- [ ] Set up monitoring
- [ ] Document deployment process
- [ ] Share with stakeholders

---

## 🎯 Success Metrics

### **Technical Metrics**
- ✅ Application loads in < 3 seconds
- ✅ API responds in < 1 second
- ✅ 99% uptime on free tiers
- ✅ All features functional

### **User Metrics**
- ✅ Complete recommendation workflow works
- ✅ Responsive design on all devices
- ✅ Error handling works correctly
- ✅ Performance is acceptable

---

## 🆘 Troubleshooting

### **Common Issues**
1. **CORS Errors**: Check backend CORS configuration
2. **API Timeouts**: Verify environment variables
3. **Build Failures**: Check dependency versions
4. **Deploy Failures**: Review platform logs

### **Debugging Steps**
1. Check platform logs
2. Test API endpoints directly
3. Verify environment variables
4. Check network connectivity

---

## 📞 Support and Resources

### **Documentation**
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

### **Community**
- Vercel Discord community
- Railway GitHub discussions
- Stack Overflow for specific issues

This deployment guide provides everything needed to deploy your restaurant recommendation system using completely free tools and platforms.
