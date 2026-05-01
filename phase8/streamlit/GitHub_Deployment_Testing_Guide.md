# GitHub Deployment Testing Guide for Phase 8 Streamlit

## 🚀 Testing Your Deployed Streamlit App

### **Option 1: Test Locally from GitHub Clone**

#### **Step 1: Clone Your Repository**
```bash
# Clone your repository
git clone https://github.com/hemaaswath/Milestone1-RR.git
cd Milestone1-RR

# Navigate to Phase 8 Streamlit
cd phase8/streamlit
```

#### **Step 2: Install Dependencies**
```bash
# Option A: Pandas-free version (recommended for Windows)
pip install -r requirements_no_pandas.txt

# Option B: Full version (if you have pandas installed)
pip install -r requirements.txt
```

#### **Step 3: Run the App Locally**
```bash
# Run pandas-free version
streamlit run app_no_pandas.py

# OR run full version
streamlit run app.py
```

#### **Step 4: Test Scenarios**

**1. Demo Mode Testing (No Backend)**
- Open the app in your browser (usually http://localhost:8501)
- Should show: "ℹ️ Demo Mode - Showing sample recommendations"
- Test the complete workflow:
  - Fill out the preference form
  - Click "Get Recommendations"
  - Verify results display correctly
  - Check charts and analytics

**2. API Connected Mode Testing**
- Start Phase 6 Backend first:
  ```bash
  cd scripts
  python run_phase6_server.py
  ```
- In another terminal, run Streamlit:
  ```bash
  cd phase8/streamlit
  streamlit run app_no_pandas.py
  ```
- Should show: "🟢 Backend API Connected"
- Test with real API calls

### **Option 2: Deploy to Streamlit Cloud**

#### **Step 1: Go to Streamlit Cloud**
1. Visit: https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub account
4. Select repository: `hemaaswath/Milestone1-RR`

#### **Step 2: Configure Deployment**
```
Repository: hemaaswath/Milestone1-RR
Branch: main
Main file path: phase8/streamlit/app_no_pandas.py
```

#### **Step 3: Set Environment Variables**
```
GROQ_API_KEY=your_groq_api_key_here
API_BASE_URL=http://127.0.0.1:8000/api/v1
```

#### **Step 4: Deploy**
- Click "Deploy"
- Wait for deployment to complete
- Your app will be available at: `https://your-app-name.streamlit.app`

### **Option 3: Test Different Deployment Methods**

#### **Railway Deployment**
1. Go to: https://railway.app
2. Click "New Project"
3. Deploy from GitHub
4. Select `Milestone1-RR` repository
5. Set environment variables
6. Deploy

#### **Render Deployment**
1. Go to: https://render.com
2. Click "New Web Service"
3. Connect GitHub
4. Select repository
5. Configure build settings
6. Deploy

## 🧪 Testing Checklist

### **Basic Functionality Tests**
- [ ] App loads without errors
- [ ] Header displays correctly
- [ ] Sidebar information shows
- [ ] Preference form renders
- [ ] All dropdowns work
- [ ] Sliders function properly
- [ ] Submit button works
- [ ] Results display correctly
- [ ] Charts render (if using full version)
- [ ] Mobile responsive design works

### **API Integration Tests**
- [ ] Demo mode works (no backend)
- [ ] API mode works (with backend)
- [ ] Error handling works
- [ ] Loading states show
- [ ] Status indicators work

### **Performance Tests**
- [ ] App loads quickly (< 5 seconds)
- [ ] Form submission responds quickly
- [ ] Charts render smoothly
- [ ] No memory leaks
- [ ] Mobile performance is good

## 🔍 Debugging Common Issues

### **App Won't Start**
```bash
# Check Python version
python --version

# Check Streamlit installation
streamlit --version

# Check dependencies
pip list
```

### **Import Errors**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements_no_pandas.txt

# Check specific package
python -c "import streamlit; print('OK')"
```

### **API Connection Issues**
```bash
# Test API health
curl http://127.0.0.1:8000/api/v1/health

# Check environment variables
echo $GROQ_API_KEY
echo $API_BASE_URL
```

### **Charts Not Working**
- Use pandas-free version: `app_no_pandas.py`
- Check Plotly installation: `python -c "import plotly; print('OK')"`
- Verify data structure

## 📱 Mobile Testing

### **Mobile Browser Testing**
1. Open app on mobile device
2. Test touch interactions
3. Verify responsive design
4. Check text readability
5. Test scrolling

### **Mobile Emulator Testing**
```bash
# Use Chrome DevTools
1. Open app in Chrome
2. Press F12
3. Click device icon
4. Select mobile device
5. Test functionality
```

## 🚀 Production Testing

### **Streamlit Cloud Testing**
1. Deploy to Streamlit Cloud
2. Test all functionality
3. Verify environment variables
4. Check performance
5. Test on mobile devices

### **Performance Monitoring**
```bash
# Monitor app performance
- Check load times
- Monitor memory usage
- Test with multiple users
- Verify error rates
```

## 📊 Test Results Documentation

### **Test Report Template**
```
Date: [Date]
Environment: [Local/Streamlit Cloud/Railway]
App Version: [app.py/app_no_pandas.py]
Python Version: [Version]

✅ Working Features:
- Feature 1
- Feature 2

❌ Issues Found:
- Issue 1
- Issue 2

📱 Mobile Testing:
- iOS: [Status]
- Android: [Status]

🚀 Performance:
- Load Time: [Time]
- Memory Usage: [Usage]

📝 Notes:
[Additional observations]
```

## 🎯 Quick Testing Commands

### **Local Testing**
```bash
# Clone and test
git clone https://github.com/hemaaswath/Milestone1-RR.git
cd Milestone1-RR/phase8/streamlit
pip install -r requirements_no_pandas.txt
streamlit run app_no_pandas.py
```

### **URL Testing**
```bash
# Test local app
curl http://localhost:8501

# Test deployed app
curl https://your-app-name.streamlit.app
```

### **API Testing**
```bash
# Test backend API
curl http://127.0.0.1:8000/api/v1/health

# Test recommendations endpoint
curl -X POST http://127.0.0.1:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{"location": "Bellandur", "budget": "medium", "top_k": 3}'
```

## 🎉 Success Criteria

Your testing is successful when:
- ✅ App loads without errors
- ✅ All widgets work correctly
- ✅ Recommendations display properly
- ✅ Both demo and API modes work
- ✅ Mobile responsive design works
- ✅ Performance is acceptable
- ✅ Error handling works correctly

---

**Happy Testing! 🚀**
