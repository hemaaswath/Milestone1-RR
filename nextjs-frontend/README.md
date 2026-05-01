# FoodAI - Next.js Frontend

A modern, responsive Next.js frontend for the AI-powered restaurant recommendation system.

## 🚀 Features

- **Modern UI/UX** - Built with Next.js 14, Tailwind CSS, and Shadcn/ui
- **AI-Powered Search** - Smart restaurant recommendations with advanced filtering
- **Responsive Design** - Mobile-first approach with beautiful animations
- **Real-time Updates** - Live search, autocomplete, and dynamic content
- **Monitoring Dashboard** - System health and analytics visualization
- **TypeScript** - Full type safety and better developer experience
- **Performance Optimized** - Core Web Vitals compliance and fast loading

## 🛠️ Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + Custom design system
- **State Management**: Zustand
- **API Client**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod validation
- **Icons**: Lucide React
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Notifications**: React Hot Toast
- **TypeScript**: Full type safety

## 📦 Installation

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on `http://127.0.0.1:8000`

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nextjs-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment Setup**
   ```bash
   cp .env.example .env.local
   ```
   
   Configure your environment variables:
   ```env
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api/v1
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗️ Project Structure

```
nextjs-frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── globals.css         # Global styles
│   │   ├── layout.tsx          # Root layout
│   │   └── page.tsx            # Homepage
│   ├── components/             # Reusable components
│   │   ├── layout/             # Layout components
│   │   ├── search/             # Search components
│   │   ├── sections/           # Page sections
│   │   └── ui/                 # UI components
│   ├── lib/                    # Utilities and configuration
│   │   ├── api.ts              # API client
│   │   ├── react-query.ts       # Query client setup
│   │   └── utils.ts            # Utility functions
│   ├── types/                  # TypeScript types
│   │   └── api.ts              # API type definitions
│   └── hooks/                  # Custom React hooks
├── public/                     # Static assets
├── docs/                       # Documentation
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://127.0.0.1:8000/api/v1` |
| `NEXT_PUBLIC_APP_URL` | Frontend application URL | `http://localhost:3000` |
| `NEXT_PUBLIC_GA_ID` | Google Analytics ID (optional) | - |
| `NEXT_PUBLIC_SENTRY_DSN` | Sentry DSN for error tracking (optional) | - |

### Tailwind CSS Configuration

The project uses a custom design system with restaurant-specific colors:

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      restaurant: {
        primary: "#FF6B6B",
        secondary: "#4ECDC4", 
        accent: "#45B7D1",
        // ... more colors
      }
    }
  }
}
```

## 📱 Pages & Routes

### Core Pages

- **`/`** - Homepage with hero section and search
- **`/search`** - Advanced search and results
- **`/dashboard`** - User dashboard and preferences
- **`/monitoring`** - System monitoring dashboard
- **`/favorites`** - Saved restaurants

### API Integration

All API calls are handled through the centralized API client:

```typescript
import { apiClient } from '@/lib/api'

// Get recommendations
const recommendations = await apiClient.getRecommendations(preferences)

// Get system health
const health = await apiClient.getSystemHealth()
```

## 🎨 UI Components

### Design System

The project uses a consistent design system with:

- **Custom colors** - Restaurant-themed palette
- **Typography** - Inter font family
- **Spacing** - 4px grid system
- **Animations** - Smooth transitions and micro-interactions

### Key Components

- **Header** - Navigation with mobile menu
- **Footer** - Comprehensive footer with links
- **SearchForm** - Advanced restaurant search
- **RecommendationCard** - Restaurant display cards
- **LoadingSpinner** - Consistent loading states
- **ErrorBoundary** - Error handling components

## 🔍 Search Features

### Advanced Search

- **Location-based** - Search by area/neighborhood
- **Budget filtering** - Low, medium, high price ranges
- **Cuisine preferences** - Multiple cuisine types
- **Rating filters** - Minimum rating requirements
- **Additional preferences** - Custom requirements

### Real-time Features

- **Autocomplete** - Location and cuisine suggestions
- **Live filtering** - Instant result updates
- **Progressive loading** - Smooth content loading

## 📊 Monitoring Dashboard

### System Health

- **CPU/Memory usage** - Real-time system metrics
- **Response times** - API performance tracking
- **Error rates** - System error monitoring
- **Request volume** - Traffic analytics

### User Analytics

- **Search patterns** - Popular searches and locations
- **User behavior** - Engagement metrics
- **Recommendation performance** - Click-through rates
- **Feedback analysis** - User satisfaction

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect to Vercel**
   ```bash
   npx vercel
   ```

2. **Configure environment variables**
   - Set up all required environment variables in Vercel dashboard

3. **Deploy**
   ```bash
   vercel --prod
   ```

### Other Platforms

The app can be deployed to any platform that supports Next.js:

- **Netlify** - Static site generation
- **AWS** - Amplify or EC2
- **DigitalOcean** - App Platform
- **Docker** - Containerized deployment

## 🧪 Testing

### Unit Tests

```bash
npm run test
# or
yarn test
```

### E2E Tests

```bash
npm run test:e2e
# or
yarn test:e2e
```

### Type Checking

```bash
npm run type-check
# or
yarn type-check
```

## 📈 Performance

### Core Web Vitals

The application is optimized for:

- **LCP** < 2.5s (Largest Contentful Paint)
- **FID** < 100ms (First Input Delay)  
- **CLS** < 0.1 (Cumulative Layout Shift)

### Optimization Features

- **Image optimization** - Next.js Image component
- **Code splitting** - Automatic route-based splitting
- **Lazy loading** - Component and image lazy loading
- **Bundle analysis** - Optimized package sizes

## 🔒 Security

### Best Practices

- **Input validation** - Zod schema validation
- **XSS protection** - Built-in React protections
- **CSRF protection** - SameSite cookies
- **Content Security Policy** - Configured CSP headers
- **HTTPS enforcement** - SSL/TLS required

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- **Documentation** - Check the `/docs` folder
- **Issues** - Open an issue on GitHub
- **Discussions** - Join the GitHub Discussions
- **Email** - Contact the development team

## 🗺️ Roadmap

### Upcoming Features

- [ ] **User Authentication** - Login and user profiles
- [ ] **Restaurant Booking** - Direct booking integration
- [ ] **Mobile App** - React Native app
- [ ] **Social Features** - Reviews and sharing
- [ ] **Advanced Analytics** - Business intelligence dashboard
- [ ] **Multi-language Support** - Internationalization
- [ ] **Offline Mode** - PWA capabilities

### Technical Improvements

- [ ] **Database Integration** - PostgreSQL/SQLite
- [ ] **Caching** - Redis integration
- [ ] **WebSocket Support** - Real-time updates
- [ ] **Microservices** - Service-oriented architecture
- [ ] **AI Model Updates** - Enhanced recommendation algorithms

---

**Built with ❤️ using Next.js and modern web technologies**
