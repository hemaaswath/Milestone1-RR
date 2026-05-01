# Phase 5 Testing Guide

## 🧪 Comprehensive Testing Methods for Phase 5 Response Presentation Layer

This guide provides multiple approaches to test Phase 5, from unit tests to browser validation.

---

## 🚀 Quick Testing Methods

### 1. **Automated Test Suite** (Recommended)
```bash
cd "c:/Users/Family/Documents/Milestone1-Build Hours"
python scripts/test_phase5.py
```

This runs comprehensive tests covering:
- ✅ Unit tests for all components
- ✅ Format validation (JSON, HTML, Cards, Table, Summary)
- ✅ UI component generation
- ✅ Phase 3 + 4 + 5 integration
- ✅ Error handling
- ✅ Performance benchmarks
- ✅ Browser test file generation

### 2. **Basic Functionality Test**
```bash
python scripts/run_phase5.py
```

Demonstrates Phase 5 with sample data and generates output files.

---

## 📋 Manual Testing Approaches

### **1. Unit Testing**

Test individual components:

```python
# Test RecommendationCard
from phase5.formatters import RecommendationCard
card = RecommendationCard(
    restaurant_name="Test Restaurant",
    rank=1,
    score=0.95,
    explanation="Test explanation",
    location="Test Location",
    cuisines="Test Cuisine"
)
print(card.to_dict())

# Test ResponseFormatter
from phase5.formatters import ResponseFormatter
formatter = ResponseFormatter()
result = formatter.format_recommendations(sample_data, ResponseFormat.JSON)
print(result)
```

### **2. Format Testing**

Test each output format:

```python
from phase5.formatters import ResponseFormatter
from phase5.response_types import ResponseFormat

formatter = ResponseFormatter()
sample_data = [{"restaurant_name": "Test", "rank": 1, "score": 0.9, ...}]

# Test all formats
formats = [ResponseFormat.JSON, ResponseFormat.HTML, ResponseFormat.CARDS, 
           ResponseFormat.TABLE, ResponseFormat.SUMMARY]

for fmt in formats:
    result = formatter.format_recommendations(sample_data, fmt)
    print(f"{fmt}: {type(result)} - Keys: {list(result.keys())}")
```

### **3. UI Component Testing**

Test HTML generation:

```python
from phase5.ui_components import UIComponents

ui = UIComponents()
html = ui.generate_recommendation_html(sample_data)
print(f"HTML length: {len(html)}")
print(f"Contains DOCTYPE: {'<!DOCTYPE html>' in html}")
```

---

## 🌐 Browser Testing

### **1. Visual Testing**

Open the generated HTML files in your browser:

1. **Main Test Page**: `test_phase5_complete.html`
   - Check visual layout and styling
   - Test hover effects on recommendation cards
   - Verify responsive design (resize browser)
   - Validate color schemes and typography

2. **Component Testing**: 
   - `test_phase5_cards.html` - Card layout testing
   - `test_phase5_table.html` - Table format testing

3. **API Format Testing**:
   - `test_phase5_json.json` - Validate JSON structure

### **2. Responsive Design Testing**

```html
<!-- Open test_phase5_complete.html and test at different viewport sizes -->
<!-- Mobile: 375px width -->
<!-- Tablet: 768px width -->
<!-- Desktop: 1200px+ width -->
```

### **3. Interactive Testing**

Test interactive elements:
- Hover effects on cards
- Button interactions (if any)
- Link functionality
- Form elements

---

## 🔧 Integration Testing

### **1. Full Pipeline Testing**

Test the complete Phase 3 + 4 + 5 pipeline:

```python
from phase2.models import UserPreferences
from phase3.engine import load_restaurants, retrieve_top_candidates
from phase4.service import generate_ranked_recommendations
from phase5.formatters import ResponseFormatter

# Create preferences
preferences = UserPreferences(
    location="Bellandur",
    budget="medium", 
    cuisine="North Indian"
)

# Phase 3: Get candidates
restaurants_df = load_restaurants("data/processed/restaurants_phase1.csv")
phase3_result = retrieve_top_candidates(restaurants_df, preferences, top_n=5)

# Phase 4: Get recommendations
candidates = [c.to_dict() for c in phase3_result.candidates[:3]]
recommendations = generate_ranked_recommendations(preferences, candidates, top_k=3)

# Phase 5: Format results
formatter = ResponseFormatter()
json_result = formatter.format_recommendations(recommendations, ResponseFormat.JSON)
html_result = formatter.format_recommendations(recommendations, ResponseFormat.CARDS)
```

### **2. API Integration Testing**

Test Phase 5 with the Flask API:

```bash
# Start the backend API
python src/api/main.py

# Then test Phase 5 with real API calls
python scripts/test_phase5.py
```

---

## ⚠️ Error Testing

### **1. Edge Cases**

Test error handling:

```python
from phase5.formatters import ResponseFormatter

formatter = ResponseFormatter()

# Test empty recommendations
result = formatter.format_recommendations([], ResponseFormat.JSON)
print("Empty test:", result)

# Test invalid data
try:
    invalid_data = [{"invalid": "data"}]
    result = formatter.format_recommendations(invalid_data, ResponseFormat.JSON)
except Exception as e:
    print("Expected error:", type(e).__name__)
```

### **2. Data Validation**

Test with various data structures:

```python
# Missing fields
test_data_missing = [
    {"restaurant_name": "Test", "rank": 1}  # Missing required fields
]

# Invalid data types
test_data_invalid = [
    {"restaurant_name": 123, "rank": "invalid", "score": "high"}
]
```

---

## ⚡ Performance Testing

### **1. Speed Testing**

```python
import time
from phase5.formatters import ResponseFormatter

# Create large dataset
large_data = [{"restaurant_name": f"Restaurant {i}", "rank": i+1, 
               "score": 0.9, "explanation": "Test", 
               "location": "Test", "cuisines": "Test"} 
              for i in range(100)]

formatter = ResponseFormatter()

# Test performance
start_time = time.time()
result = formatter.format_recommendations(large_data, ResponseFormat.JSON)
end_time = time.time()

print(f"Formatted 100 items in {end_time - start_time:.3f} seconds")
```

### **2. Memory Testing**

Monitor memory usage with large datasets:

```python
import sys
from phase5.ui_components import UIComponents

ui = UIComponents()
large_data = [create_large_recommendation() for _ in range(50)]

html_result = ui.generate_recommendation_html(large_data)
print(f"Generated HTML size: {len(html_result)} characters")
print(f"Memory usage: {sys.getsizeof(html_result)} bytes")
```

---

## 🔍 Validation Testing

### **1. Output Validation**

Validate each format:

```python
# JSON validation
import json
json_result = formatter.format_recommendations(data, ResponseFormat.JSON)
parsed = json.dumps(json_result)  # Should not raise error

# HTML validation
html_result = ui.generate_recommendation_html(data)
assert '<!DOCTYPE html>' in html_result
assert '</html>' in html_result
assert 'restaurant' in html_result.lower()

# Structure validation
assert 'status' in json_result
assert json_result['status'] == 'success'
```

### **2. Content Validation**

Check content quality:

```python
result = formatter.format_recommendations(data, ResponseFormat.JSON)
recommendations = result['data'].get('recommendations', [])

for rec in recommendations:
    assert 'restaurant_name' in rec
    assert 'rank' in rec
    assert 'score' in rec
    assert isinstance(rec['rank'], int)
    assert 0 <= rec['score'] <= 1
```

---

## 📊 Test Results Interpretation

### **Success Indicators**
- ✅ All unit tests pass
- ✅ All formats generate valid output
- ✅ HTML files render correctly in browser
- ✅ Integration tests complete successfully
- ✅ Performance within acceptable limits (<1s for 100 items)

### **Common Issues & Solutions**

| Issue | Cause | Solution |
|-------|-------|----------|
| Import errors | Missing dependencies | Install requirements: `pip install -r requirements.txt` |
| Encoding errors | Special characters | Use UTF-8 encoding for file operations |
| Missing data | Incomplete Phase 3/4 results | Check backend API is running |
| Rendering issues | CSS conflicts | Validate HTML/CSS syntax |

---

## 🎯 Testing Checklist

### **Before Each Test**
- [ ] Backend API is running (for integration tests)
- [ ] Dependencies are installed
- [ ] Test data files exist
- [ ] Output directory is writable

### **During Testing**
- [ ] Monitor console for errors
- [ ] Check file generation
- [ ] Validate output formats
- [ ] Test browser rendering

### **After Testing**
- [ ] Review generated files
- [ ] Check performance metrics
- [ ] Validate error handling
- [ ] Document any issues

---

## 🚀 Continuous Testing

### **Automated Testing**
Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Test Phase 5
  run: |
    python scripts/test_phase5.py
    python scripts/run_phase5.py
```

### **Manual Testing Schedule**
- **Daily**: Run basic functionality test
- **Weekly**: Full integration test
- **Before Release**: Complete test suite

---

## 📞 Getting Help

If tests fail:
1. Check the error messages in console output
2. Verify backend API is accessible
3. Ensure all dependencies are installed
4. Check file permissions and paths
5. Review this guide for troubleshooting steps

---

**🎉 Happy Testing!**
