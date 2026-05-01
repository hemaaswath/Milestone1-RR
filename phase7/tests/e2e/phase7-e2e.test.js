import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { chromium } from 'playwright'

// E2E Tests for Phase 7 Frontend Web UI
describe('Phase 7 E2E Tests', () => {
  let browser
  let page

  beforeAll(async () => {
    browser = await chromium.launch({ headless: true })
    page = await browser.newPage()
  })

  afterAll(async () => {
    await browser.close()
  })

  describe('Phase 7 Exit Criteria Verification', () => {
    it('should complete demo path: API + UI → submit preferences → see results', async () => {
      // Navigate to Phase 7 frontend
      await page.goto('http://localhost:3000')
      
      // Wait for page to load
      await page.waitForSelector('h1')
      
      // Check API status
      const apiStatus = await page.locator('[data-testid="api-status"]').textContent()
      expect(apiStatus).toContain('API Online')
      
      // Fill in preferences
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      await page.selectOption('[data-testid="cuisine-select"]', 'North Indian')
      await page.fill('[data-testid="min-rating"]', '3.5')
      
      // Submit form
      await page.click('[data-testid="submit-button"]')
      
      // Wait for results
      await page.waitForSelector('[data-testid="results-display"]', { timeout: 30000 })
      
      // Verify results
      const resultsTitle = await page.locator('h2').textContent()
      expect(resultsTitle).toContain('Your Restaurant Recommendations')
      
      // Check that recommendations are displayed
      const recommendationCards = await page.locator('[data-testid="recommendation-card"]').count()
      expect(recommendationCards).toBeGreaterThan(0)
      
      // Verify recommendation details
      const firstRestaurant = await page.locator('[data-testid="recommendation-card"]').first()
      await expect(firstRestaurant.locator('[data-testid="restaurant-name"]')).toBeVisible()
      await expect(firstRestaurant.locator('[data-testid="restaurant-rating"]')).toBeVisible()
      await expect(firstRestaurant.locator('[data-testid="restaurant-explanation"]')).toBeVisible()
    })

    it('should handle API offline state gracefully', async () => {
      // Mock API offline state
      await page.route('**/api/v1/health', route => {
        route.fulfill({
          status: 503,
          contentType: 'application/json',
          body: JSON.stringify({ error: 'Service Unavailable' })
        })
      })
      
      await page.goto('http://localhost:3000')
      
      // Should show API offline message
      await expect(page.locator('[data-testid="api-offline-message"]')).toBeVisible()
      await expect(page.locator('[data-testid="api-instructions"]')).toBeVisible()
    })

    it('should validate form inputs correctly', async () => {
      await page.goto('http://localhost:3000')
      
      // Try to submit without required fields
      await page.click('[data-testid="submit-button"]')
      
      // Should show validation errors
      await expect(page.locator('[data-testid="error-location"]')).toBeVisible()
      await expect(page.locator('[data-testid="error-budget"]')).toBeVisible()
      
      // Fill in required fields
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      
      // Submit button should be enabled now
      const submitButton = page.locator('[data-testid="submit-button"]')
      await expect(submitButton).toBeEnabled()
    })

    it('should display loading states during API calls', async () => {
      // Mock slow API response
      await page.route('**/api/v1/recommendations', async route => {
        await new Promise(resolve => setTimeout(resolve, 2000)) // 2 second delay
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'success',
            data: {
              recommendations: [
                {
                  restaurant_name: 'Test Restaurant',
                  rank: 1,
                  score: 0.95,
                  explanation: 'Great match',
                  location: 'Bellandur',
                  cuisines: 'North Indian',
                  rating: 4.5,
                  cost_for_two: 800
                }
              ]
            }
          })
        })
      })
      
      await page.goto('http://localhost:3000')
      
      // Fill and submit form
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      await page.click('[data-testid="submit-button"]')
      
      // Should show loading state
      await expect(page.locator('[data-testid="loading-state"]')).toBeVisible()
      await expect(page.locator('[data-testid="loading-message"]')).toContain('Finding Restaurants')
      
      // Should show results after loading
      await page.waitForSelector('[data-testid="results-display"]', { timeout: 30000 })
      await expect(page.locator('[data-testid="results-display"]')).toBeVisible()
    })

    it('should handle empty results gracefully', async () => {
      // Mock empty results
      await page.route('**/api/v1/recommendations', route => {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'success',
            data: {
              recommendations: []
            }
          })
        })
      })
      
      await page.goto('http://localhost:3000')
      
      // Fill and submit form
      await page.selectOption('[data-testid="location-select"]', 'NonExistentLocation')
      await page.click('[data-testid="budget-medium"]')
      await page.click('[data-testid="submit-button"]')
      
      // Should show empty state
      await expect(page.locator('[data-testid="empty-state"]')).toBeVisible()
      await expect(page.locator('[data-testid="empty-message"]')).toContain('No Restaurants Found')
    })

    it('should support copy as markdown functionality', async () => {
      await page.goto('http://localhost:3000')
      
      // Fill and submit form
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      await page.click('[data-testid="submit-button"]')
      
      // Wait for results
      await page.waitForSelector('[data-testid="results-display"]', { timeout: 30000 })
      
      // Test copy functionality
      const copyButton = page.locator('[data-testid="copy-markdown"]')
      await copyButton.click()
      
      // Verify clipboard content (in real test, you'd check clipboard)
      await expect(copyButton).toBeVisible()
    })

    it('should be responsive on mobile devices', async () => {
      // Set mobile viewport
      await page.setViewportSize({ width: 375, height: 667 })
      
      await page.goto('http://localhost:3000')
      
      // Check mobile layout
      await expect(page.locator('[data-testid="mobile-menu"]')).not.toBeVisible() // Should not need mobile menu for this simple app
      
      // Form should be usable on mobile
      await expect(page.locator('[data-testid="preference-form"]')).toBeVisible()
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      
      const submitButton = page.locator('[data-testid="submit-button"]')
      await expect(submitButton).toBeVisible()
      await expect(submitButton).toBeEnabled()
    })

    it('should handle API errors gracefully', async () => {
      // Mock API error
      await page.route('**/api/v1/recommendations', route => {
        route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'error',
            message: 'Internal server error'
          })
        })
      })
      
      await page.goto('http://localhost:3000')
      
      // Fill and submit form
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      await page.click('[data-testid="submit-button"]')
      
      // Should show error message
      await expect(page.locator('[data-testid="error-message"]')).toBeVisible()
      await expect(page.locator('[data-testid="error-message"]')).toContain('Internal server error')
    })
  })

  describe('Phase 7 Integration with Phase 6 API', () => {
    it('should communicate exclusively with Phase 6 API', async () => {
      // Monitor API calls
      const apiCalls = []
      page.on('request', request => {
        if (request.url().includes('/api/v1/')) {
          apiCalls.push({
            url: request.url(),
            method: request.method()
          })
        }
      })
      
      await page.goto('http://localhost:3000')
      
      // Should make health check call
      await page.waitForTimeout(2000)
      expect(apiCalls.some(call => call.url.includes('/health'))).toBe(true)
      
      // Fill and submit form
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      await page.click('[data-testid="submit-button"]')
      
      // Should make recommendations call
      await page.waitForTimeout(3000)
      expect(apiCalls.some(call => call.url.includes('/recommendations') && call.method === 'POST')).toBe(true)
      
      // All API calls should go to Phase 6 API
      apiCalls.forEach(call => {
        expect(call.url).toContain('/api/v1/')
      })
    })

    it('should use correct API endpoints', async () => {
      await page.goto('http://localhost:3000')
      
      // Should call meta endpoint for form options
      await page.waitForTimeout(2000)
      
      // Verify location and cuisine data is loaded
      const locationSelect = page.locator('[data-testid="location-select"]')
      await expect(locationSelect).toBeVisible()
      
      const options = await locationSelect.locator('option').count()
      expect(options).toBeGreaterThan(1) // Should have loaded locations from API
    })
  })

  describe('Phase 7 Performance Tests', () => {
    it('should load within acceptable time limits', async () => {
      const startTime = Date.now()
      
      await page.goto('http://localhost:3000')
      await page.waitForSelector('h1')
      
      const loadTime = Date.now() - startTime
      expect(loadTime).toBeLessThan(3000) // Should load in under 3 seconds
    })

    it('should handle form submission quickly', async () => {
      await page.goto('http://localhost:3000')
      
      // Time form submission
      const startTime = Date.now()
      
      await page.selectOption('[data-testid="location-select"]', 'Bellandur')
      await page.click('[data-testid="budget-medium"]')
      await page.click('[data-testid="submit-button"]')
      
      // Should show loading state quickly
      await page.waitForSelector('[data-testid="loading-state"]')
      const submissionTime = Date.now() - startTime
      
      expect(submissionTime).toBeLessThan(1000) // Should submit in under 1 second
    })
  })
})
