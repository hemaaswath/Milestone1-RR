# Google Stitch Frontend Generation Prompt

## Project Overview
**Restaurant Recommendation System - Next.js Frontend**

Generate a modern, production-ready Next.js frontend for an AI-powered restaurant recommendation system with comprehensive UI/UX, real-time features, and beautiful design.

## Technology Stack
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + Shadcn/ui components
- **State Management**: Zustand
- **API Integration**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **Images**: Next.js Image Optimization
- **Deployment**: Vercel-ready

## API Integration
**Base URL**: `http://127.0.0.1:8000/api/v1`

### Key Endpoints to Integrate:
```typescript
// Core Recommendation API
POST /recommendations - Get AI recommendations
POST /recommendations/web - Web interface recommendations

// Data Endpoints
GET /locations - Available locations (349+ Bangalore areas)
GET /cuisines - Available cuisines (50+ types)
GET /stats - Dataset statistics

// Monitoring & Analytics (Phase 6)
GET /monitoring/health - System health
GET /monitoring/metrics - Performance metrics
GET /analytics/user-behavior - User analytics
GET /analytics/recommendations - Recommendation analytics
POST /feedback/collect - Collect user feedback
```

## Pages & Components Required

### 1. Homepage (`/`)
- Hero section with gradient background
- Smart search form with autocomplete
- Feature highlights
- Call-to-action sections

### 2. Search Results Page (`/search`)
- Advanced search filters
- Real-time recommendations display
- Multiple view modes (cards, table, map)
- Loading states and skeleton screens

### 3. Restaurant Detail Page (`/restaurant/[id]`)
- Restaurant information display
- AI-generated explanations
- User reviews and ratings
- Booking integration placeholder

### 4. Dashboard Page (`/dashboard`)
- User preferences management
- Search history
- Favorite restaurants
- Personalized insights

### 5. Monitoring Dashboard (`/monitoring`)
- System health indicators
- Performance metrics charts
- User analytics visualizations
- Real-time data updates

## Component Library Requirements

### Core Components
```typescript
// Search Components
- SearchForm (with autocomplete)
- LocationAutocomplete
- CuisineAutocomplete
- BudgetSelector
- RatingSlider

// Recommendation Components
- RecommendationCard
- RecommendationTable
- RecommendationMap
- ScoreVisualization
- ExplanationDisplay

// UI Components
- LoadingSpinner
- ErrorBoundary
- AlertBanner
- Modal
- Tooltip
- Badge
- ProgressBar

// Layout Components
- Header (with navigation)
- Footer
- Sidebar
- Breadcrumb
- Container
```

### Design System
```css
/* Color Palette */
--primary: #FF6B6B
--secondary: #4ECDC4
--accent: #45B7D1
--success: #27ae60
--warning: #f39c12
--error: #e74c3c
--dark: #2c3e50
--light: #ecf0f1

/* Typography */
- Font: Inter (Google Fonts)
- Sizes: 12px to 48px scale
- Weights: 300 to 700

/* Spacing */
- Scale: 4px, 8px, 16px, 24px, 32px, 48px, 64px

/* Border Radius */
- Small: 4px
- Medium: 8px
- Large: 12px
- XL: 16px
```

## Image Requirements

### Hero Section Images
- **Restaurant Hero**: High-quality restaurant interior, warm lighting, professional photography
- **Food Photography**: Delicious Indian cuisine dishes, vibrant colors, professional food styling
- **AI/Tech Images**: Modern AI visualization, data visualization graphics, technology concepts

### UI Icons & Illustrations
- **Custom Icons**: Restaurant, search, location, rating, budget, cuisine icons
- **Illustrations**: User journey, recommendation process, data flow diagrams
- **Background Patterns**: Subtle geometric patterns, food-related illustrations

### Stock Image Categories
- **Restaurant Interiors**: Modern, traditional, casual, fine dining
- **Food Photography**: Indian cuisine, international dishes, appetizing presentations
- **People**: Diverse customers, families, business professionals dining
- **Technology**: AI/ML concepts, data visualization, modern interfaces

## State Management Structure

```typescript
// Global Store (Zustand)
interface AppState {
  // Search State
  searchQuery: SearchPreferences
  searchResults: Recommendation[]
  isLoading: boolean
  error: string | null
  
  // User State
  userPreferences: UserPreferences
  searchHistory: SearchHistory[]
  favorites: Restaurant[]
  
  // UI State
  viewMode: 'cards' | 'table' | 'map'
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  
  // Monitoring State
  systemHealth: HealthStatus
  analyticsData: AnalyticsData
}
```

## API Integration Patterns

```typescript
// React Query Configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 3,
      refetchOnWindowFocus: false,
    },
  },
})

// API Hooks
const useRecommendations = (preferences: SearchPreferences) => {
  return useQuery({
    queryKey: ['recommendations', preferences],
    queryFn: () => api.getRecommendations(preferences),
    enabled: !!preferences.location,
  })
}

const useLocations = () => {
  return useQuery({
    queryKey: ['locations'],
    queryFn: () => api.getLocations(),
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
  })
}
```

## Responsive Design Requirements

### Breakpoints
- Mobile: 320px - 768px
- Tablet: 768px - 1024px
- Desktop: 1024px - 1440px
- Large Desktop: 1440px+

### Mobile-First Features
- Touch-friendly interfaces
- Swipe gestures for cards
- Mobile-optimized search
- Progressive web app capabilities

## Performance Requirements

### Core Web Vitals
- **LCP**: < 2.5s (Largest Contentful Paint)
- **FID**: < 100ms (First Input Delay)
- **CLS**: < 0.1 (Cumulative Layout Shift)

### Optimization Features
- Image optimization with Next.js Image
- Code splitting and lazy loading
- Service worker for offline support
- Prefetching for navigation
- Bundle size optimization

## SEO & Accessibility

### SEO Requirements
- Meta tags for all pages
- Structured data (JSON-LD)
- Open Graph tags
- Sitemap generation
- Robot.txt configuration

### Accessibility (WCAG 2.1 AA)
- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation
- Screen reader support
- Color contrast compliance
- Focus indicators

## Animation & Interactions

### Micro-interactions
- Button hover states
- Card hover effects
- Loading animations
- Form validation feedback
- Smooth transitions

### Page Transitions
- Fade-in animations
- Slide transitions
- Loading skeletons
- Progress indicators

## Error Handling & Loading States

### Error Boundaries
- Global error boundary
- Component-specific boundaries
- Error logging and reporting
- User-friendly error messages

### Loading States
- Skeleton screens
- Loading spinners
- Progress bars
- Optimistic updates

## Deployment Configuration

### Environment Variables
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api/v1
NEXT_PUBLIC_APP_URL=https://your-domain.com
NEXT_PUBLIC_GA_ID=your-google-analytics-id
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
```

### Build Configuration
- Next.js 14 App Router
- Static generation where possible
- ISR for dynamic content
- Edge runtime for API routes

## File Structure
```
src/
├── app/
│   ├── (auth)/
│   ├── dashboard/
│   ├── monitoring/
│   ├── search/
│   ├── restaurant/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   ├── search/
│   ├── recommendations/
│   ├── charts/
│   └── layout/
├── lib/
│   ├── api.ts
│   ├── utils.ts
│   └── validations.ts
├── hooks/
│   ├── useRecommendations.ts
│   ├── useAnalytics.ts
│   └── useLocalStorage.ts
├── store/
│   └── app-store.ts
├── types/
│   ├── api.ts
│   ├── recommendation.ts
│   └── user.ts
└── public/
    ├── images/
    ├── icons/
    └── favicon.ico
```

## Specific Image Prompts for Generation

### Hero Section Images
1. **Modern Restaurant Interior**: "Professional photo of a modern restaurant interior with warm ambient lighting, wooden tables, comfortable seating, elegant decor, high resolution, architectural photography style"

2. **Delicious Indian Cuisine**: "Professional food photography of delicious Indian cuisine dishes, vibrant colors, garnished beautifully, restaurant-quality presentation, top-down view, high resolution"

3. **AI Technology Visualization**: "Abstract AI visualization with neural network patterns, blue and purple gradient, data flow graphics, modern tech aesthetic, high resolution digital art"

### UI Icons Set
1. **Restaurant Icons**: "Modern flat icons for restaurant, fork, knife, plate, chef hat, in consistent style, SVG format, 24x24 pixels"

2. **Search Icons**: "Search, location pin, filter, sort, map icons in modern flat design, consistent color scheme, SVG format"

3. **Rating Icons**: "Star rating icons, filled and empty states, heart icon, thumbs up/down, in consistent style, SVG format"

### Background Patterns
1. **Food Pattern**: "Subtle food-related background pattern with fork, knife, plate silhouettes, light gray, seamless repeat, high resolution"

2. **Geometric Pattern**: "Modern geometric pattern with triangles and circles, subtle colors, seamless repeat, suitable for web backgrounds"

## Content & Copywriting

### Homepage Copy
- Headline: "Discover Your Perfect Dining Experience with AI"
- Subheadline: "Personalized restaurant recommendations powered by advanced AI technology"
- Features: "Real-time Search • AI Explanations • Personalized Results"

### SEO Meta Tags
- Title: "AI Restaurant Recommendations | Find Perfect Restaurants | FoodAI"
- Description: "Discover personalized restaurant recommendations powered by AI. Search by location, cuisine, budget, and preferences. Get AI explanations for every recommendation."

## Testing Requirements

### Unit Tests
- Component testing with Jest + React Testing Library
- API integration tests
- Utility function tests
- Hook testing

### E2E Tests
- User journey testing with Playwright
- Search functionality
- Recommendation flow
- Responsive design testing

## Analytics & Monitoring

### User Analytics
- Page view tracking
- User interaction events
- Search behavior analysis
- Conversion tracking

### Performance Monitoring
- Core Web Vitals monitoring
- Error tracking with Sentry
- Performance budget alerts
- Real user monitoring

---

## Deliverables Expected

1. **Complete Next.js Application** with all pages and components
2. **Responsive Design** optimized for all devices
3. **API Integration** with full backend connectivity
4. **Image Assets** including hero images, icons, and illustrations
5. **Documentation** for setup and deployment
6. **Testing Suite** with unit and E2E tests
7. **Deployment Configuration** for Vercel/Netlify
8. **Performance Optimization** meeting Core Web Vitals
9. **Accessibility Compliance** (WCAG 2.1 AA)
10. **SEO Optimization** with meta tags and structured data

The frontend should be production-ready, visually stunning, and provide an exceptional user experience for the AI restaurant recommendation system.
