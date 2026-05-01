# Phase 8: Testing and Deployment Guide

## 🧪 Testing Phase 8 Streamlit App

### **Local Testing**

#### **Prerequisites**
```bash
# Install dependencies
cd phase8/streamlit
pip install -r requirements.txt
```

#### **Run Local Tests**
```bash
# Run basic structure tests
cd phase8/streamlit
python tests/test_phase8_basic.py

# Expected: 75% success rate (6/8 tests passed)
```

#### **Run the App Locally**
```bash
cd phase8/streamlit
streamlit run app.py

# Or use the deployment version
cd phase8/streamlit/deployment
streamlit run streamlit_app.py
```

#### **Test Scenarios**

**1. API Connected Mode**
- Ensure Phase 6 Backend is running (http://127.0.0.1:8000)
- Open Streamlit app
- Should show "🟢 Backend API Connected"
- Test complete workflow with real API

**2. Demo Mode (API Offline)**
- Run Streamlit app without backend
- Should show "ℹ️ Demo Mode - Showing sample recommendations"
- Test complete workflow with demo data

**3. Manual Testing Checklist**
- ✅ App loads without errors
- ✅ Preference form renders correctly
- ✅ All widgets work (dropdowns, sliders, buttons)
- ✅ Submit button triggers recommendations
- ✅ Results display with proper formatting
- ✅ Charts render correctly
- ✅ Sidebar information updates
- ✅ Responsive design works

### **Automated Testing**

#### **Run Test Suite**
```bash
cd phase8/streamlit
python tests/test_phase8_basic.py
```

#### **Test Results Expected**
```
🧪 Phase 8 Basic Test Suite
====================================
test_config_import ... ok
test_config_api_urls ... ok
test_default_values ... ok
test_file_structure ... ok
test_readme_content ... ok
test_requirements_file ... ok
test_deployment_files ... ok
test_app_file_structure ... ok

Ran 8 tests in 0.053s
PASSED: 6/8 (75% success rate)
```

---

## 🚀 Deployment Options

### **Option 1: Streamlit Cloud (Recommended)**

#### **Step 1: Prepare for Deployment**
```bash
# Create deployment-ready app
cd phase8/streamlit/deployment
cp streamlit_app.py app.py
cp requirements.txt ../requirements.txt
```

#### **Step 2: Create GitHub Repository**
```bash
# Create new repository on GitHub
# Repository name: restaurant-recommendations-streamlit
# Make it public

# Push code to GitHub
git init
git add .
git commit -m "Phase 8 Streamlit Demo App"
git branch -M main
git remote add origin https://github.com/yourusername/restaurant-recommendations-streamlit.git
git push -u origin main
```

#### **Step 3: Deploy to Streamlit Cloud**
1. Go to [Streamlit Cloud](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Select `app.py` as main file
5. Add environment variables:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   API_BASE_URL=http://127.0.0.1:8000/api/v1
   ```
6. Click "Deploy"

#### **Step 4: Test Deployment**
- Your app will be available at: `https://yourapp.streamlit.app`
- Test all features work correctly
- Share the link with stakeholders

### **Option 2: Railway Deployment**

#### **Step 1: Prepare Railway Files**
```bash
# Create Railway-compatible app
cd phase8/streamlit/deployment
```

#### **Step 2: Deploy to Railway**
1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Add environment variables:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   API_BASE_URL=http://127.0.0.1:8000/api/v1
   PORT=8501
   ```
6. Deploy

#### **Step 3: Access Your App**
- Your app will be available at: `https://your-app-name.up.railway.app`
- Test all functionality

### **Option 3: Local Production Deployment**

#### **Step 1: Set Up Environment**
```bash
cd phase8/streamlit
export GROQ_API_KEY=your_groq_api_key_here
export API_BASE_URL=http://127.0.0.1:8000/api/v1
```

#### **Step 2: Run Production Server**
```bash
streamlit run app.py --server.port 8501 --server.headless true
```

#### **Step 3: Access Your App**
- Open: `http://localhost:8501`
- Test all features

---

## 🔧 Environment Variables Setup

### **Required Variables**
```bash
# GROQ API Key (required for real recommendations)
GROQ_API_KEY=your_groq_api_key_here

# API Base URL (optional, defaults to localhost)
API_BASE_URL=http://127.0.0.1:8000/api/v1
```

### **How to Get GROQ API Key**
1. Go to [Groq Console](https://console.groq.com)
2. Sign up/login
3. Go to API Keys
4. Create new key
5. Copy the key

### **Setting Environment Variables**

**Streamlit Cloud:**
- In app settings → Environment variables
- Add each variable separately

**Railway:**
- In project settings → Variables
- Add each variable separately

**Local:**
```bash
# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
echo "API_BASE_URL=http://127.0.0.1:8000/api/v1" >> .env

# Or set in terminal
export GROQ_API_KEY=your_key_here
export API_BASE_URL=http://127.0.0.1:8000/api/v1
```

---

## 📊 Testing After Deployment

### **Functional Testing Checklist**

#### **1. Basic Functionality**
- ✅ App loads without errors
- ✅ All widgets render correctly
- ✅ Form submission works
- ✅ Results display properly
- ✅ Charts render correctly

#### **2. API Integration**
- ✅ API status indicator works
- ✅ Real recommendations work (when API available)
- ✅ Demo mode works (when API unavailable)
- ✅ Error handling works correctly

#### **3. User Experience**
- ✅ Loading states show
- ✅ Responsive design works
- ✅ Sidebar information updates
- ✅ Performance is acceptable

#### **4. Data Flow**
- ✅ Form data captured correctly
- ✅ API calls made properly
- ✅ Results parsed and displayed
- ✅ Charts data generated correctly

### **Performance Testing**

#### **Load Testing**
```bash
# Test with multiple simultaneous users
# Monitor response times
# Check for memory leaks
# Verify error handling under load
```

#### **Browser Testing**
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

### **Integration Testing**

#### **With Phase 6 Backend**
```bash
# Start Phase 6 Backend
cd "c:/Users/Family/Documents/Milestone1-Build Hours"
python scripts/run_phase6_server.py

# Start Phase 8 Streamlit
cd phase8/streamlit
streamlit run app.py

# Test complete integration
```

#### **Demo Mode Testing**
```bash
# Stop Phase 6 Backend
# Run Phase 8 Streamlit
# Verify demo mode works correctly
```

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **1. App Won't Start**
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version (3.8+ required)
python --version

# Check for syntax errors
python -m py_compile app.py
```

#### **2. API Connection Issues**
```bash
# Check API status
curl http://127.0.0.1:8000/api/v1/health

# Check environment variables
echo $GROQ_API_KEY
echo $API_BASE_URL

# Check CORS configuration
```

#### **3. Charts Not Rendering**
```bash
# Check Plotly installation
pip install plotly==5.17.0

# Check data structure
# Verify DataFrame creation
```

#### **4. Deployment Issues**
```bash
# Check repository structure
# Verify requirements.txt
# Check environment variables
# Review deployment logs
```

### **Debug Mode**

#### **Enable Debug Logging**
```python
# In app.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Check Logs**
```bash
# Streamlit logs
streamlit logs

# Railway logs
# Check Railway dashboard

# Streamlit Cloud logs
# Check Streamlit Cloud dashboard
```

---

## 📱 Mobile Testing

### **Responsive Design Testing**
1. Open app on mobile device
2. Test all widgets work on touch
3. Verify charts render correctly
4. Check text readability
5. Test scrolling and navigation

### **Mobile Browser Testing**
- Safari (iOS)
- Chrome (Android)
- Edge (Mobile)

---

## 🚀 Production Deployment Checklist

### **Pre-Deployment**
- [ ] All tests pass locally
- [ ] Environment variables configured
- [ ] Repository pushed to GitHub
- [ ] Dependencies verified
- [ ] Documentation updated

### **Deployment**
- [ ] App deployed successfully
- [ ] Environment variables set
- [ ] Domain configured (if custom)
- [ ] SSL certificate active
- [ ] Health checks passing

### **Post-Deployment**
- [ ] Manual testing completed
- [ ] Performance verified
- [ ] Mobile testing completed
- [ ] Stakeholder testing done
- [ ] Documentation updated
- [ ] Monitoring set up

---

## 📞 Support and Resources

### **Documentation**
- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Docs](https://plotly.com/python)
- [Pandas Docs](https://pandas.pydata.org)

### **Community**
- Streamlit Community Forum
- Stack Overflow
- GitHub Issues

### **Monitoring**
- Streamlit Cloud Analytics
- Railway Monitoring
- Custom logging

---

## 🎯 Quick Start Summary

### **For Immediate Testing:**
```bash
cd phase8/streamlit
pip install -r requirements.txt
streamlit run app.py
```

### **For Quick Deployment:**
1. Push to GitHub
2. Deploy to Streamlit Cloud
3. Set environment variables
4. Test and share

### **For Production:**
1. Complete all testing
2. Set up monitoring
3. Configure domain
4. Document deployment process

This guide provides everything needed to test and deploy Phase 8 Streamlit app successfully!
