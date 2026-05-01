// Modern JavaScript for Restaurant Recommendation Frontend

class RestaurantRecommendationApp {
    constructor() {
        this.apiBase = 'http://127.0.0.1:8000/api/v1';
        this.currentRecommendations = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.setupAutoComplete();
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('recommendation-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });

        // Clear button
        const clearBtn = document.getElementById('clear-btn');
        clearBtn.addEventListener('click', () => {
            this.clearForm();
        });

        // View format change
        const viewFormat = document.getElementById('view-format');
        viewFormat.addEventListener('change', (e) => {
            this.changeViewFormat(e.target.value);
        });

        // Input validation
        const inputs = document.querySelectorAll('.form-input, .form-select');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.validateInput(input);
            });
        });
    }

    async loadInitialData() {
        try {
            // Load available locations and cuisines
            const [locationsResponse, cuisinesResponse] = await Promise.all([
                fetch(`${this.apiBase}/locations`),
                fetch(`${this.apiBase}/cuisines`)
            ]);

            const locations = await locationsResponse.json();
            const cuisines = await cuisinesResponse.json();

            this.setupAutoCompleteData(locations.data.locations, cuisines.data.cuisines);
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    setupAutoCompleteData(locations, cuisines) {
        this.availableLocations = locations;
        this.availableCuisines = cuisines;
    }

    setupAutoComplete() {
        const locationInput = document.getElementById('location');
        const cuisineInput = document.getElementById('cuisine');

        // Location autocomplete
        this.setupAutoCompleteForInput(locationInput, 'location-suggestions', this.availableLocations);

        // Cuisine autocomplete
        this.setupAutoCompleteForInput(cuisineInput, 'cuisine-suggestions', this.availableCuisines);
    }

    setupAutoCompleteForInput(input, suggestionsId, data) {
        const suggestionsDiv = document.getElementById(suggestionsId);

        input.addEventListener('input', () => {
            const value = input.value.toLowerCase();
            if (value.length < 2) {
                suggestionsDiv.style.display = 'none';
                return;
            }

            const filtered = data.filter(item => 
                item.toLowerCase().includes(value)
            ).slice(0, 5);

            if (filtered.length > 0) {
                suggestionsDiv.innerHTML = filtered.map(item => 
                    `<div class="suggestion-item">${item}</div>`
                ).join('');
                suggestionsDiv.style.display = 'block';

                // Add click handlers
                suggestionsDiv.querySelectorAll('.suggestion-item').forEach(item => {
                    item.addEventListener('click', () => {
                        input.value = item.textContent;
                        suggestionsDiv.style.display = 'none';
                    });
                });
            } else {
                suggestionsDiv.style.display = 'none';
            }
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.contains(e.target) && !suggestionsDiv.contains(e.target)) {
                suggestionsDiv.style.display = 'none';
            }
        });
    }

    validateInput(input) {
        const value = input.value.trim();
        let isValid = true;

        if (input.id === 'location' && value.length < 2) {
            isValid = false;
        }

        if (input.id === 'min_rating') {
            const rating = parseFloat(value);
            if (isNaN(rating) || rating < 0 || rating > 5) {
                isValid = false;
            }
        }

        input.style.borderColor = isValid ? '#e0e0e0' : '#e74c3c';
        return isValid;
    }

    async handleFormSubmit() {
        const formData = new FormData(document.getElementById('recommendation-form'));
        const preferences = {
            location: formData.get('location'),
            budget: formData.get('budget'),
            cuisine: formData.get('cuisine'),
            min_rating: parseFloat(formData.get('min_rating')) || 0,
            additional_preferences: formData.get('additional_preferences')
                .split(',')
                .map(pref => pref.trim())
                .filter(pref => pref.length > 0)
        };

        // Validate all inputs
        const locationInput = document.getElementById('location');
        const ratingInput = document.getElementById('min_rating');
        
        if (!this.validateInput(locationInput) || !this.validateInput(ratingInput)) {
            this.showError('Please fill in all required fields correctly.');
            return;
        }

        await this.getRecommendations(preferences);
    }

    async getRecommendations(preferences) {
        this.showLoading();

        try {
            const response = await fetch(`${this.apiBase}/recommendations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...preferences,
                    top_k: 5,
                    format: 'cards',
                    include_summary: true
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                this.currentRecommendations = data.data.recommendations;
                this.showResults(data.data);
            } else {
                this.showError(data.message || 'Failed to get recommendations');
            }
        } catch (error) {
            console.error('Error getting recommendations:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        document.getElementById('error').style.display = 'none';
        
        // Scroll to loading section
        document.getElementById('loading').scrollIntoView({ behavior: 'smooth' });
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showResults(data) {
        const resultsSection = document.getElementById('results');
        const container = document.getElementById('recommendations-container');

        // Show summary
        this.showSummary(data.summary);

        // Render recommendations based on current view format
        const viewFormat = document.getElementById('view-format').value;
        this.renderRecommendations(data.recommendations, viewFormat);

        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showSummary(summary) {
        // Create or update summary section
        let summaryDiv = document.getElementById('recommendations-summary');
        if (!summaryDiv) {
            summaryDiv = document.createElement('div');
            summaryDiv.id = 'recommendations-summary';
            summaryDiv.className = 'summary-card';
            document.getElementById('results').insertBefore(summaryDiv, document.getElementById('recommendations-container'));
        }

        summaryDiv.innerHTML = `
            <h3>📊 Summary</h3>
            <p>We analyzed <strong>${summary.total_candidates}</strong> restaurants and found 
               <strong>${summary.filtered_candidates}</strong> matching your criteria.</p>
            <p>Presenting top <strong>${summary.final_recommendations}</strong> recommendations.</p>
        `;
    }

    renderRecommendations(recommendations, format) {
        const container = document.getElementById('recommendations-container');
        
        if (format === 'table') {
            this.renderTableView(recommendations);
        } else if (format === 'map') {
            this.renderMapView(recommendations);
        } else {
            this.renderCardsView(recommendations);
        }
    }

    renderCardsView(recommendations) {
        const container = document.getElementById('recommendations-container');
        container.innerHTML = recommendations.map((rec, index) => `
            <div class="recommendation-card" style="animation-delay: ${index * 0.1}s">
                <div class="card-header">
                    <h3 class="restaurant-name">${rec.restaurant_name}</h3>
                    <div class="card-rank">#${rec.rank}</div>
                </div>
                <div class="card-body">
                    <div class="card-info">
                        <div class="info-item">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>${rec.location}</span>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-utensils"></i>
                            <span>${rec.cuisines}</span>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-star"></i>
                            <span class="rating-stars">${this.generateStars(rec.rating)}</span>
                        </div>
                        <div class="info-item">
                            <i class="fas fa-wallet"></i>
                            <span>₹${rec.cost_for_two || 'N/A'}</span>
                        </div>
                    </div>
                    
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${rec.score * 100}%"></div>
                    </div>
                    
                    <div class="explanation">
                        <strong>💡 Why we recommend this:</strong><br>
                        ${rec.explanation}
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderTableView(recommendations) {
        const container = document.getElementById('recommendations-container');
        container.innerHTML = `
            <div class="table-container">
                <table class="recommendations-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Restaurant</th>
                            <th>Location</th>
                            <th>Cuisine</th>
                            <th>Rating</th>
                            <th>Cost</th>
                            <th>Score</th>
                            <th>Explanation</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${recommendations.map(rec => `
                            <tr>
                                <td><strong>#${rec.rank}</strong></td>
                                <td>${rec.restaurant_name}</td>
                                <td>${rec.location}</td>
                                <td>${rec.cuisines}</td>
                                <td>${this.generateStars(rec.rating)}</td>
                                <td>₹${rec.cost_for_two || 'N/A'}</td>
                                <td><span class="score-badge">${(rec.score * 100).toFixed(1)}%</span></td>
                                <td>${rec.explanation}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    renderMapView(recommendations) {
        // Placeholder for map view - would integrate with Google Maps or similar
        const container = document.getElementById('recommendations-container');
        container.innerHTML = `
            <div class="map-placeholder">
                <h3>🗺️ Map View</h3>
                <p>Map integration coming soon! Here are the restaurant locations:</p>
                <div class="location-list">
                    ${recommendations.map(rec => `
                        <div class="location-item">
                            <strong>${rec.restaurant_name}</strong> - ${rec.location}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    generateStars(rating) {
        if (!rating || rating === 'N/A') return 'No rating';
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        
        return '⭐'.repeat(fullStars) + 
               (hasHalfStar ? '⭐' : '') + 
               '☆'.repeat(emptyStars) + 
               ` (${rating})`;
    }

    changeViewFormat(format) {
        if (this.currentRecommendations.length > 0) {
            this.renderRecommendations(this.currentRecommendations, format);
        }
    }

    showError(message) {
        const errorSection = document.getElementById('error');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        
        // Scroll to error
        errorSection.scrollIntoView({ behavior: 'smooth' });
    }

    clearForm() {
        document.getElementById('recommendation-form').reset();
        document.getElementById('results').style.display = 'none';
        document.getElementById('error').style.display = 'none';
        
        // Clear validation styles
        document.querySelectorAll('.form-input, .form-select').forEach(input => {
            input.style.borderColor = '#e0e0e0';
        });
    }
}

// Add table styles to CSS
const tableStyles = `
    <style>
        .table-container {
            overflow-x: auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .recommendations-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }
        
        .recommendations-table th,
        .recommendations-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .recommendations-table th {
            background: var(--light-color);
            font-weight: 600;
            color: var(--dark-color);
        }
        
        .recommendations-table tr:hover {
            background: var(--light-color);
        }
        
        .score-badge {
            background: var(--success-color);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .map-placeholder {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .location-list {
            margin-top: 1.5rem;
            text-align: left;
        }
        
        .location-item {
            background: var(--light-color);
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 6px;
            border-left: 4px solid var(--primary-color);
        }
    </style>
`;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add table styles
    document.head.insertAdjacentHTML('beforeend', tableStyles);
    
    // Initialize the app
    window.restaurantApp = new RestaurantRecommendationApp();
    
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
});
