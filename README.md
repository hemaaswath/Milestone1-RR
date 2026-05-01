# 🍽️ Restaurant Recommendation System

A comprehensive AI-powered restaurant recommendation system built with multiple phases of development, from data processing to deployment.

## 🎯 Project Overview

This project implements a complete restaurant recommendation pipeline with:
- **Data Processing & Analysis** (Phases 1-5)
- **Backend HTTP API** (Phase 6)
- **Frontend Web UI** (Phase 7)
- **Streamlit Demo App** (Phase 8)

## 📋 Phases Completed

### ✅ Phase 1-5: Data Processing Pipeline
- Data collection and cleaning
- Feature engineering
- ML model development
- Recommendation algorithm
- Performance optimization

### ✅ Phase 6: Backend HTTP API
- Flask-based REST API
- Request validation and sanitization
- CORS configuration
- Rate limiting
- Structured logging and telemetry
- Health checks and monitoring

### ✅ Phase 7: Frontend Web UI
- Modern web interface
- Preference collection forms
- Real-time results display
- Responsive design
- API integration

### ✅ Phase 8: Streamlit Deployment
- Fast-sharing demo app
- Beautiful UI with charts
- Single-process deployment
- Server-side secret management
- Production-ready deployment

## 🚀 Quick Start

### **Option 1: Streamlit Demo (Recommended for Quick Testing)**
```bash
cd phase8/streamlit
pip install -r requirements_no_pandas.txt
streamlit run app_no_pandas.py
```

### **Option 2: Full System (Backend + Frontend)**
```bash
# Start Backend API
python scripts/run_phase6_server.py

# Start Frontend (in separate terminal)
cd phase7/simple_frontend
python -m http.server 3000
```

### **Option 3: Phase 8 Full Streamlit**
```bash
cd phase8/streamlit
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Project Structure

```
Milestone1-RR/
├── phase1-5/                    # Data processing pipeline
├── phase6/                      # Backend HTTP API
├── phase7/                      # Frontend Web UI
├── phase8/                      # Streamlit Demo App
│   └── streamlit/
│       ├── app.py              # Main Streamlit app
│       ├── app_no_pandas.py    # Pandas-free version
│       ├── components/         # UI components
│       ├── tests/             # Test suites
│       └── deployment/        # Deployment configs
├── scripts/                    # Utility scripts
├── docs/                      # Documentation
├── deployment/                 # Production deployment files
└── data/                      # Data files
```

## 🛠️ Technology Stack

### **Backend (Phase 6)**
- **Flask** - Web framework
- **Python** - Programming language
- **GROQ API** - AI model integration
- **Requests** - HTTP client

### **Frontend (Phase 7)**
- **HTML/CSS/JavaScript** - Web technologies
- **Bootstrap** - UI framework
- **Axios** - HTTP client

### **Streamlit (Phase 8)**
- **Streamlit** - Web app framework
- **Plotly** - Charts and visualizations
- **Pandas** - Data processing (optional)

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```bash
GROQ_API_KEY=your_groq_api_key_here
API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## 📊 API Endpoints

### **Health Check**
```
GET /api/v1/health
```

### **Get Recommendations**
```
POST /api/v1/recommendations
Content-Type: application/json

{
  "location": "Bellandur",
  "budget": "medium",
  "cuisine": "North Indian",
  "top_k": 5
}
```

### **Available Locations**
```
GET /api/v1/locations
```

### **Available Cuisines**
```
GET /api/v1/cuisines
```

## 🚀 Deployment Options

### **Streamlit Cloud (Recommended)**
1. Push to GitHub
2. Connect to [Streamlit Cloud](https://share.streamlit.io)
3. Deploy automatically

### **Free Hosting**
- **Frontend**: [Vercel](https://vercel.com)
- **Backend**: [Railway](https://railway.app) or [Render](https://render.com)

### **Local Development**
```bash
# Backend
python scripts/run_phase6_server.py

# Frontend
cd phase7/simple_frontend
python -m http.server 3000

# Streamlit
cd phase8/streamlit
streamlit run app.py
```

## 🧪 Testing

### **Run All Tests**
```bash
# Phase 6 Tests
python scripts/test_phase6_direct.py

# Phase 7 Tests
cd phase7/simple_frontend
python ../tests/test_phase7_integration.py

# Phase 8 Tests
cd phase8/streamlit
python tests/test_phase8_basic.py
```

### **Integration Testing**
```bash
python scripts/test_full_integration.py
```

## 📈 Features

### **AI-Powered Recommendations**
- Personalized restaurant suggestions
- Multi-criteria filtering
- Real-time processing
- Explanatory recommendations

### **User-Friendly Interface**
- Intuitive preference forms
- Beautiful result displays
- Interactive charts and analytics
- Mobile-responsive design

### **Production Ready**
- Secure API with validation
- Rate limiting and CORS
- Structured logging
- Health checks and monitoring
- Easy deployment

## 🔍 Monitoring & Analytics

### **API Metrics**
- Request counts and response times
- Error rates and status codes
- Performance monitoring
- Health check endpoints

### **User Analytics**
- Preference patterns
- Popular locations and cuisines
- Recommendation accuracy
- User engagement metrics

## 🛡️ Security

### **API Security**
- Input validation and sanitization
- Rate limiting (60 requests/minute)
- CORS configuration
- Request size limits (1MB max)

### **Data Protection**
- Server-side secret management
- Environment variable handling
- No sensitive data in client code
- Secure API key storage

## 📚 Documentation

- **[Architecture](docs/Architecture.md)** - System design and architecture
- **[Testing Guide](docs/Testing_Guide.md)** - Comprehensive testing instructions
- **[Deployment Guide](docs/Deployment_Guide.md)** - Production deployment guide
- **[Phase 8 Guide](phase8/streamlit/README.md)** - Streamlit deployment details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Current Status

- ✅ **Phase 1-5**: Data processing complete
- ✅ **Phase 6**: Backend API production ready
- ✅ **Phase 7**: Frontend UI complete
- ✅ **Phase 8**: Streamlit demo app deployed
- 🔄 **Deployment**: Ready for production deployment

## 🚀 Next Steps

1. Deploy to production (Streamlit Cloud, Vercel, Railway)
2. Set up monitoring and analytics
3. Add user authentication
4. Implement database integration
5. Scale for production use

---

**Built with ❤️ for restaurant discovery and culinary exploration!**
