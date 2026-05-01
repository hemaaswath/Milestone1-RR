# Phase 6 + Phase 7 Testing Guide

## Overview

This guide provides comprehensive testing instructions for the Phase 6 Backend HTTP API and Phase 7 Frontend Web UI integration that is currently running.

## 🌐 Access Points

**Frontend Application**: http://127.0.0.1:3000  
**Backend API**: http://127.0.0.1:8000  
**API Documentation**: http://127.0.0.1:8000/api/v1/meta

---

## 🧪 Testing Methods

### 1. **Manual Browser Testing (Recommended)**

#### Step 1: Access the Frontend
1. Open your web browser
2. Navigate to: http://127.0.0.1:3000
3. Verify the page loads correctly
4. Check API status indicator (should show "🟢 API Online")

#### Step 2: Test Form Functionality
1. **Location Selection**:
   - Click the location dropdown
   - Verify options: Bellandur, Delhi, Mumbai, Bangalore, Hyderabad
   - Select "Bellandur"

2. **Budget Selection**:
   - Click on budget radio buttons
   - Verify Low, Medium, High options work
   - Select "Medium"

3. **Cuisine Preference**:
   - Click cuisine dropdown
   - Verify options: North Indian, Chinese, Italian, South Indian, Continental
   - Select "North Indian" (optional)

4. **Rating Slider**:
   - Move the rating slider
   - Verify value updates (1.0 to 5.0)
   - Set to 3.5

5. **Number of Recommendations**:
   - Select from dropdown (3, 5, 7, 10)
   - Choose "5 recommendations"

#### Step 3: Test Recommendation Workflow
1. Click "Get Recommendations" button
2. Observe loading state (spinner and message)
3. Wait for results to appear
4. Verify results display:
   - Restaurant names
   - Ranking numbers (#1, #2, #3...)
   - Match scores (95.0%, 85.0%, etc.)
   - Location, cuisine, rating, cost details
   - AI explanations for each recommendation

#### Step 4: Test Edge Cases
1. **Empty Results**:
   - Try an invalid location combination
   - Verify "No Restaurants Found" message appears

2. **Form Validation**:
   - Try submitting without location
   - Try submitting without budget
   - Verify validation errors appear

### 2. **API Testing (Direct Backend Testing)**

#### Health Check
```bash
curl http://127.0.0.1:8000/api/v1/health
```
Expected: `{"status": "healthy", "phase": "6", ...}`

#### API Metadata
```bash
curl http://127.0.0.1:8000/api/v1/meta
```
Expected: API version, available locations, cuisines, etc.

#### Get Locations
```bash
curl http://127.0.0.1:8000/api/v1/locations
```
Expected: `{"status": "success", "data": {"locations": [...]}}`

#### Get Cuisines
```bash
curl http://127.0.0.1:8000/api/v1/cuisines
```
Expected: `{"status": "success", "data": {"cuisines": [...]}}`

#### Test Recommendations
```bash
curl -X POST http://127.0.0.1:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{"location": "Bellandur", "budget": "medium", "topK": 3}'
```
Expected: Restaurant recommendations with rankings and explanations

### 3. **Automated Testing (Scripts)**

#### Run Integration Tests
```bash
cd "c:/Users/Family/Documents/Milestone1-Build Hours"
python scripts/test_full_integration.py
```

#### Run Phase 6 Tests
```bash
cd "c:/Users/Family/Documents/Milestone1-Build Hours"
python scripts/test_phase6_direct.py
```

### 4. **Browser Developer Tools Testing**

#### Network Tab Testing
1. Open browser developer tools (F12)
2. Go to Network tab
3. Use the frontend application
4. Observe API calls:
   - GET /api/v1/health (status check)
   - GET /api/v1/locations (load locations)
   - GET /api/v1/cuisines (load cuisines)
   - POST /api/v1/recommendations (get recommendations)

#### Console Testing
1. Open browser console
2. Check for JavaScript errors
3. Verify API status updates
4. Monitor any error messages

---

## 🎯 Test Scenarios

### **Scenario 1: Happy Path**
1. Open: http://127.0.0.1:3000
2. Select: Bellandur, Medium budget, North Indian cuisine
3. Set rating: 3.5, Recommendations: 5
4. Click: "Get Recommendations"
5. **Expected**: 3-5 restaurant recommendations with AI explanations

### **Scenario 2: Different Locations**
1. Test each location: Bellandur, Delhi, Mumbai, Bangalore, Hyderabad
2. **Expected**: Different restaurant results for each location

### **Scenario 3: Different Budgets**
1. Test Low, Medium, High budgets
2. **Expected**: Different cost ranges in results

### **Scenario 4: Empty Results**
1. Select unusual combinations
2. **Expected**: "No Restaurants Found" message

### **Scenario 5: Form Validation**
1. Try submitting without required fields
2. **Expected**: Validation error messages

---

## 🔍 Performance Testing

### Response Time Testing
1. Use browser Network tab
2. Measure API response times
3. **Expected**: < 100ms for most endpoints

### Load Testing
1. Submit multiple requests quickly
2. **Expected**: Consistent responses, no timeouts

---

## 📱 Mobile Testing

### Responsive Design
1. Use browser developer tools
2. Switch to mobile view (iPhone, Android)
3. Test form functionality on small screens
4. **Expected**: Responsive layout, touch-friendly interface

---

## 🛡️ Security Testing

### CORS Testing
1. Verify frontend can access backend
2. **Expected**: No CORS errors in console

### Input Validation
1. Try submitting malformed data
2. **Expected**: Proper error responses

---

## 📊 Expected Results

### **Successful Test Indicators**
- ✅ Frontend loads at http://127.0.0.1:3000
- ✅ API status shows "🟢 API Online"
- ✅ Form data loads from backend
- ✅ Recommendations appear with AI explanations
- ✅ Loading states work correctly
- ✅ Error handling shows proper messages
- ✅ Responsive design works on mobile

### **Failure Indicators**
- ❌ Frontend doesn't load
- ❌ API status shows "🔴 API Offline"
- ❌ Form dropdowns are empty
- ❌ Recommendations don't appear
- ❌ Console errors present
- ❌ CORS errors in network tab

---

## 🔧 Troubleshooting

### **Frontend Not Loading**
- Check if frontend server is running (port 3000)
- Verify browser URL is correct
- Check for JavaScript errors in console

### **API Status Offline**
- Check if backend server is running (port 8000)
- Verify backend process hasn't crashed
- Check network connectivity

### **No Recommendations**
- Verify form is filled correctly
- Check API response in Network tab
- Verify backend has valid data

### **CORS Errors**
- Verify backend CORS configuration
- Check frontend URL matches CORS origins
- Restart backend if needed

---

## 📋 Test Checklist

### **Frontend Tests**
- [ ] Page loads correctly
- [ ] API status indicator shows online
- [ ] Location dropdown populated
- [ ] Cuisine dropdown populated
- [ ] Form validation works
- [ ] Loading states appear
- [ ] Recommendations display correctly
- [ ] Error messages appear when expected
- [ ] Responsive design works

### **Backend Tests**
- [ ] Health endpoint returns 200
- [ ] All API endpoints respond correctly
- [ ] Recommendations endpoint works
- [ ] Error handling returns proper HTTP codes
- [ ] CORS headers present
- [ ] Response times acceptable

### **Integration Tests**
- [ ] Frontend can call backend APIs
- [ ] Data flows correctly frontend → backend → frontend
- [ ] Complete user workflow works
- [ ] Error handling works end-to-end

---

## 🚀 Quick Test Command

For a quick verification, run this single command:

```bash
cd "c:/Users/Family/Documents/Milestone1-Build Hours" && python scripts/test_full_integration.py
```

This will run all integration tests and provide a comprehensive report.

---

## 📞 Support

If you encounter issues:
1. Check both services are running (ports 8000 and 3000)
2. Review browser console for errors
3. Check backend process logs
4. Run the integration test script for detailed diagnostics

The system is designed to be robust and should handle most testing scenarios gracefully.
