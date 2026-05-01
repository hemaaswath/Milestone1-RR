## Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)

Build an AI-powered restaurant recommendation system inspired by Zomato.  
The system should combine structured restaurant data with a Large Language Model (LLM) to provide personalized, relevant, and easy-to-understand recommendations based on user preferences.

## Objective

Design and implement an application that:

- Accepts user preferences such as location, budget, cuisine, and minimum rating.
- Uses a real-world restaurant dataset.
- Leverages an LLM to generate personalized, human-like recommendations.
- Presents clear, useful, and actionable results to users.

## System Workflow

### 1) Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:  
  [https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- Extract relevant fields such as restaurant name, location, cuisine, cost, and rating.

### 2) User Input Collection

Collect user preferences, including:

- Location (e.g., Delhi, Bangalore)
- Budget (low, medium, high)
- Preferred cuisine (e.g., Italian, Chinese)
- Minimum acceptable rating
- Additional preferences (e.g., family-friendly, quick service)

### 3) Integration Layer

- Filter and prepare restaurant records based on user input.
- Convert filtered data into structured context for the LLM.
- Design prompts that enable the LLM to reason, compare, and rank options effectively.

### 4) Recommendation Engine

Use the LLM to:

- Rank restaurants according to user preferences.
- Explain why each recommendation is a good match.
- Optionally provide a short summary of the best choices.

### 5) Output Display

Present top recommendations in a user-friendly format, including:

- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation

## Phase-Wise Architecture

### Phase 1: Data Foundation and Preprocessing

**Goal:** Build a clean and reliable restaurant dataset for recommendations.

**Key Components:**
- Dataset loader (Hugging Face Zomato dataset)
- Data cleaning and normalization module
- Feature extractor (name, location, cuisines, cost, rating, tags)
- Storage layer (CSV/SQLite/PostgreSQL)
- Basic Web UI (initial source of user input for location, budget, cuisine, and rating)

**Output:**
- Preprocessed and structured restaurant data ready for querying.

### Phase 2: User Preference Capture Layer

**Goal:** Collect and validate user requirements in a structured format.

**Key Components:**
- Input interface (CLI/Web form/API)
- Preference schema validator
- User profile/preference object creator

**Output:**
- Standardized user preference object (location, budget, cuisine, rating, extras).

### Phase 3: Candidate Retrieval and Filtering Layer

**Goal:** Narrow down restaurants that satisfy hard constraints before LLM reasoning.

**Key Components:**
- Rule-based filtering engine (location, budget, minimum rating)
- Candidate scorer (basic relevance score)
- Top-N candidate selector

**Output:**
- Shortlisted candidate restaurants for LLM-based ranking.

### Phase 4: LLM Recommendation and Ranking Layer

**Goal:** Generate personalized ranking with human-like explanations.

**Key Components:**
- Prompt builder (injects user preferences + shortlisted restaurants)
- LLM inference module
- Rank and explanation parser
- Guardrails (format checks, hallucination control)

**Output:**
- Ordered recommendations with explanation for each restaurant.

### Phase 5: Response Presentation Layer

**Goal:** Deliver recommendations in a clear and user-friendly format.

**Key Components:**
- Result formatter
- UI renderer (table/cards/list)
- Optional summary generator

**Output:**
- Final response with restaurant name, cuisine, rating, estimated cost, and rationale.

### Phase 6: Backend HTTP API

**Goal:** Provide a secure, scalable HTTP service that orchestrates the recommendation pipeline.

**Concern:** Thin HTTP service that owns server-side secrets (GROQ_API_KEY), dataset access, and orchestration. The browser must not call Groq or Hugging Face directly.

**Contract:** Stable JSON request/response for recommendations with preferences body aligned with Phase 2 keys; response carries ranked items, source information, and telemetry fields.

**Key Components:**
- FastAPI/Flask HTTP service
- Request validation and sanitization
- Phase orchestration (1-5 pipeline)
- Structured logging and telemetry
- CORS configuration
- Rate limiting and request size limits

**Endpoints (v1 intent):**
- `POST /api/v1/recommendations` - Main recommendation endpoint
- `GET /health` - Service health check
- `GET /api/v1/meta` - Metadata and configuration hints

**Stack:** Python-first (FastAPI/Flask) sharing the installed milestone1 library.

**Exit Criteria:** Frontend can complete one recommendation flow using only the API; API returns the same logical outcomes as CLI for identical inputs.

**Output:** RESTful API with JSON responses and structured server logs.

---

### Phase 7: Frontend Web UI

**Goal:** Primary user-facing surface for preference collection and result display.

**Concern:** Browser-only client that communicates exclusively with Phase 6 API.

**Data Flow:** Browser → Phase 6 API → Response rendering

**Key Components:**
- Preference form (location, budget, cuisines, rating, additional text)
- Results display with restaurant details and AI explanations
- Loading states and validation error handling
- Responsive design for mobile/desktop

**UX Features:**
- Inline validation errors
- Disabled submit while pending
- Clear empty-state messaging
- Optional "copy as Markdown" functionality

**Stack Options:**
- React + Vite (SPA) - Recommended
- HTMX + server templates (minimal JS)

**Exit Criteria:** One demo path in the README: start API + UI, submit preferences, see ranked results or an intentional empty state.

**Output:** Complete web application interface with preference collection and result display.

---

### Phase 8: Streamlit Deployment (Optional)

**Goal:** Fast-sharing demo app for course demos and stakeholder previews.

**Concern:** Single-process Python app avoiding separate API + UI deployment.

**Key Components:**
- Streamlit widgets for preference input
- Direct milestone1 import or API calls
- Server-side secret management
- Community Cloud deployment

**UX Scope:**
- Forms with selectbox/text_input/slider controls
- Spinner during model processing
- Expander for raw JSON/telemetry
- Phase 5 empty-state semantics

**Deployment:**
- Streamlit Community Cloud (free tier)
- Environment variables for secrets
- Conservative load limits for free tier

**Relationship to Phase 6-7:** Complementary to Phase 7; ideal for demos and fast sharing without operating Vite + CORS + two deployables.

**Exit Criteria:** README documents local execution and Community Cloud deployment; reviewer can open hosted URL and complete recommendation flow.

**Output:** Shareable demo URL with one-click deployment.

---

### Phase 9: Hardening and Handoff

**Goal:** Production-ready system with comprehensive testing and documentation.

**Key Components:**
- Automated test suite
- API contract tests
- Performance optimization
- Cost/latency monitoring
- Comprehensive documentation

**Testing Coverage:**
- Filter validation tests
- Prompt shape tests
- JSON parsing tests
- Golden JSON for happy/empty/error paths
- API contract validation

**Documentation:**
- Installation instructions
- API key setup
- Deployment guides
- CLI fallbacks
- System limitations
- Cost optimization notes

**Output:** Production-ready recommendation system with complete documentation and testing coverage.

## High-Level Component Flow

**Phase 7 Flow:** Web UI → Phase 6 API → Phase 1-5 Pipeline → Formatted Response → UI Display

**Phase 8 Flow:** Streamlit App → Direct Phase 1-5 Import → Formatted Response → UI Display

**Complete System Flow:** User Preferences → Validation → Filtering → LLM Ranking → Presentation → User Interface
