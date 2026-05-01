# Phase 8: Streamlit Deployment

## Overview

Phase 8 provides a fast-sharing demo app for course demos and stakeholder previews. This is a single-process Python app that avoids separate API + UI deployment.

## Architecture

**Goal:** Fast-sharing demo app for course demos and stakeholder previews.

**Concern:** Single-process Python app avoiding separate API + UI deployment.

**Key Components:**
- Streamlit widgets for preference input
- Direct milestone1 import or API calls
- Server-side secret management

## Features

### Demo Application Features
- **Interactive Preference Form**: Streamlit widgets for location, budget, cuisine, rating
- **Real-time Recommendations**: Instant AI-powered restaurant suggestions
- **Beautiful UI**: Professional-looking interface with charts and metrics
- **Fast Sharing**: One-click deployment and sharing
- **Server-side Processing**: All logic runs server-side, no frontend complexity

### Technical Features
- **Single Process**: No separate API + UI deployment needed
- **Secret Management**: Server-side GROQ API key handling
- **Data Integration**: Direct milestone1 import or API calls
- **Performance**: Fast loading and responsive interactions
- **Deployment Ready**: Easy sharing via Streamlit Cloud

## Exit Criteria

One demo path in the README: start app → submit preferences → see ranked results or an intentional empty state.

## Technology Stack

**Primary Framework:**
- Streamlit (Python web app framework)
- Pandas (Data processing)
- Plotly (Charts and visualizations)
- Requests (API calls)

**Deployment Options:**
- Streamlit Cloud (Free)
- Railway/Render (Free)
- Local deployment

## Folder Structure

```
phase8/
├── streamlit/
│   ├── app.py
│   ├── requirements.txt
│   ├── config.py
│   ├── components/
│   │   ├── preference_form.py
│   │   ├── results_display.py
│   │   └── metrics_dashboard.py
│   ├── utils/
│   │   ├── api_client.py
│   │   ├── data_processor.py
│   │   └── formatters.py
│   ├── tests/
│   │   └── test_streamlit_app.py
│   └── README.md
└── deployment/
    ├── streamlit_app.py
    ├── requirements.txt
    └── deployment_guide.md
```

## Development

### Prerequisites
- Python 3.8+
- Streamlit
- Pandas
- Plotly
- Requests

### Installation
```bash
pip install streamlit pandas plotly requests python-dotenv
```

### Development
```bash
cd phase8/streamlit
streamlit run app.py
```

### Testing
```bash
cd phase8/streamlit
python tests/test_streamlit_app.py
```

## Deployment

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Railway/Render
1. Use provided deployment files
2. Configure environment variables
3. Deploy as web service

## Environment Variables

```
GROQ_API_KEY=your_groq_api_key_here
API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## Phase 8 Exit Criteria Verification

✅ **Demo Path**: Start app → Submit preferences → See ranked results
✅ **Single Process**: No separate API + UI deployment
✅ **Fast Sharing**: One-click deployment and sharing
✅ **Server-side Secrets**: GROQ API key never exposed to client
✅ **Professional UI**: Beautiful interface with charts and metrics
✅ **Performance**: Fast loading and responsive interactions
