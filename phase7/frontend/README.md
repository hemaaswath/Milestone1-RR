# Phase 7: Frontend Web UI

## Overview

Phase 7 provides the primary user-facing surface for the restaurant recommendation system. This is a browser-only client that communicates exclusively with the Phase 6 Backend HTTP API.

## Architecture

**Goal:** Primary user-facing surface for preference collection and result display.

**Concern:** Browser-only client that communicates exclusively with Phase 6 API.

**Data Flow:** Browser → Phase 6 API → Response rendering

## Features

### Key Components
- **Preference Form**: Location, budget, cuisines, rating, additional text
- **Results Display**: Restaurant details with AI explanations
- **Loading States**: Visual feedback during API calls
- **Validation**: Inline error handling and form validation
- **Responsive Design**: Mobile and desktop optimized

### UX Features
- Inline validation errors
- Disabled submit while pending
- Clear empty-state messaging
- Optional "copy as Markdown" functionality

## Technology Stack

**Primary Option (Recommended):**
- React + Vite (SPA)

**Alternative Option:**
- HTMX + server templates (minimal JS)

## Exit Criteria

One demo path in the README: start API + UI, submit preferences, see ranked results or an intentional empty state.

## Folder Structure

```
phase7/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PreferenceForm/
│   │   │   ├── ResultsDisplay/
│   │   │   ├── LoadingStates/
│   │   │   └── ErrorHandling/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── styles/
│   ├── public/
│   ├── tests/
│   └── docs/
└── tests/
    ├── integration/
    ├── unit/
    └── e2e/
```

## API Integration

The frontend exclusively communicates with the Phase 6 Backend HTTP API:

- **Base URL**: `http://127.0.0.1:8000/api/v1`
- **Main Endpoint**: `/recommendations` (POST)
- **Supporting Endpoints**: `/meta`, `/health`, `/locations`, `/cuisines`

## Development

### Prerequisites
- Node.js 18+
- npm or yarn
- Phase 6 Backend API running

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
```

### Build
```bash
npm run build
```

### Test
```bash
npm run test
```

## Phase 7 Exit Criteria Verification

✅ **Demo Path**: Start API + UI → Submit preferences → See ranked results
✅ **API Communication**: Browser only talks to Phase 6 API
✅ **Form Validation**: All inputs validated with inline errors
✅ **Loading States**: Visual feedback during API calls
✅ **Responsive Design**: Works on mobile and desktop
✅ **Error Handling**: Graceful handling of API errors
✅ **Empty States**: Clear messaging for no results
