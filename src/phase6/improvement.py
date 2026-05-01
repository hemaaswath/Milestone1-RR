"""
Continuous Improvement for Phase 6

Provides automated model optimization, data refresh, and system
improvement capabilities.
"""

import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import pandas as pd

from phase4.llm_client import run_groq_inference
from phase4.prompt_builder import build_ranking_prompt
from phase2.models import UserPreferences


@dataclass
class ModelPerformance:
    """Model performance metrics."""
    model_name: str
    avg_response_time: float
    success_rate: float
    user_satisfaction: float
    cost_per_request: float
    accuracy_score: float
    last_updated: str


@dataclass
class OptimizationResult:
    """Results from optimization process."""
    original_performance: ModelPerformance
    optimized_performance: ModelPerformance
    improvement_percentage: float
    recommended_changes: List[str]
    a_b_test_results: Optional[Dict] = None


class ModelOptimizer:
    """Optimizes LLM models and prompts for better performance."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.performance_history = []
        self.optimization_log = []
        
    def evaluate_model_performance(self, model_name: str, test_cases: List[Dict]) -> ModelPerformance:
        """Evaluate model performance against test cases."""
        response_times = []
        success_count = 0
        user_ratings = []
        
        for i, test_case in enumerate(test_cases):
            try:
                start_time = datetime.now()
                
                # Run inference with specified model
                response = run_groq_inference(
                    prompt=test_case['prompt'],
                    model=model_name
                )
                
                response_time = (datetime.now() - start_time).total_seconds()
                response_times.append(response_time)
                
                # Parse response to check success
                try:
                    parsed = json.loads(response)
                    if 'recommendations' in parsed and parsed['recommendations']:
                        success_count += 1
                        
                        # Extract user rating from test case if available
                        if 'expected_quality' in test_case:
                            user_ratings.append(test_case['expected_quality'])
                    
                except json.JSONDecodeError:
                    pass
                
                self.logger.info(f"Test case {i+1}/{len(test_cases)} completed")
                
            except Exception as e:
                self.logger.error(f"Test case {i+1} failed: {e}")
                response_times.append(10.0)  # Penalty for failure
        
        # Calculate metrics
        avg_response_time = sum(response_times) / len(response_times)
        success_rate = (success_count / len(test_cases)) * 100
        avg_user_satisfaction = sum(user_ratings) / len(user_ratings) if user_ratings else 0.0
        
        # Mock cost and accuracy (would be calculated from real usage)
        cost_per_request = self._estimate_model_cost(model_name)
        accuracy_score = self._calculate_accuracy(test_cases, model_name)
        
        return ModelPerformance(
            model_name=model_name,
            avg_response_time=avg_response_time,
            success_rate=success_rate,
            user_satisfaction=avg_user_satisfaction,
            cost_per_request=cost_per_request,
            accuracy_score=accuracy_score,
            last_updated=datetime.now().isoformat()
        )
    
    def _estimate_model_cost(self, model_name: str) -> float:
        """Estimate cost per request for model."""
        # Mock pricing based on model tiers
        model_costs = {
            "llama-3.3-70b-versatile": 0.005,
            "llama-3.1-8b-instant": 0.001,
            "mixtral-8x7b": 0.003,
            "gemma-7b-it": 0.002
        }
        return model_costs.get(model_name, 0.005)  # Default cost
    
    def _calculate_accuracy(self, test_cases: List[Dict], model_name: str) -> float:
        """Calculate model accuracy based on test cases."""
        # Mock accuracy calculation - in real implementation, this would
        # compare model outputs against expected results
        base_accuracy = random.uniform(0.75, 0.95)  # Mock realistic accuracy
        
        # Adjust based on model characteristics
        if "70b" in model_name:
            return min(base_accuracy + 0.05, 1.0)  # Larger models typically more accurate
        elif "8b" in model_name:
            return max(base_accuracy - 0.05, 0.0)  # Smaller models less accurate
        
        return base_accuracy
    
    def optimize_prompt_template(self, current_prompt: str, performance_data: ModelPerformance) -> str:
        """Optimize prompt template based on performance."""
        optimizations = []
        
        # If success rate is low, simplify prompt
        if performance_data.success_rate < 80:
            optimizations.append("Simplify instructions and reduce complexity")
            current_prompt = self._simplify_prompt(current_prompt)
        
        # If response time is high, reduce prompt length
        if performance_data.avg_response_time > 3.0:
            optimizations.append("Reduce prompt length and focus on key requirements")
            current_prompt = self._shorten_prompt(current_prompt)
        
        # If accuracy is low, add more specific guidance
        if performance_data.accuracy_score < 0.8:
            optimizations.append("Add more specific examples and constraints")
            current_prompt = self._add_examples_to_prompt(current_prompt)
        
        # Log optimization
        optimization_entry = {
            "timestamp": datetime.now().isoformat(),
            "original_performance": asdict(performance_data),
            "optimizations_applied": optimizations,
            "resulting_prompt": current_prompt
        }
        
        self.optimization_log.append(optimization_entry)
        self.logger.info(f"Applied {len(optimizations)} prompt optimizations")
        
        return current_prompt
    
    def _simplify_prompt(self, prompt: str) -> str:
        """Simplify prompt by removing complex instructions."""
        # Remove redundant phrases and simplify language
        simplified = prompt.replace("Please ensure that", "Ensure")
        simplified = simplified.replace("It is important to", "Important:")
        simplified = simplified.replace("You must", "Must")
        
        return simplified
    
    def _shorten_prompt(self, prompt: str) -> str:
        """Shorten prompt by focusing on essential elements."""
        lines = prompt.split('\n')
        essential_lines = []
        
        for line in lines:
            # Keep only essential instructions
            if any(keyword in line.lower() for keyword in [
                'rank', 'recommend', 'user preferences', 'restaurant'
            ]):
                essential_lines.append(line)
        
        return '\n'.join(essential_lines)
    
    def _add_examples_to_prompt(self, prompt: str) -> str:
        """Add specific examples to prompt."""
        example_section = """
        
Examples:
Good recommendation: {"restaurant_name": "Spice Garden", "rank": 1, "score": 0.9, "explanation": "Perfect match for location and cuisine"}
Bad recommendation: {"restaurant_name": "Wrong Place", "rank": 1, "score": 0.3, "explanation": "Doesn't match user preferences"}
        """
        
        return prompt + example_section
    
    def run_a_b_test(self, model_a: str, model_b: str, test_cases: List[Dict]) -> OptimizationResult:
        """Run A/B test between two models."""
        self.logger.info(f"Starting A/B test: {model_a} vs {model_b}")
        
        # Evaluate both models
        perf_a = self.evaluate_model_performance(model_a, test_cases)
        perf_b = self.evaluate_model_performance(model_b, test_cases)
        
        # Calculate improvement
        improvement = ((perf_b.user_satisfaction - perf_a.user_satisfaction) / perf_a.user_satisfaction) * 100
        
        # Determine winner
        winner = model_b if perf_b.user_satisfaction > perf_a.user_satisfaction else model_a
        
        result = OptimizationResult(
            original_performance=perf_a,
            optimized_performance=perf_b,
            improvement_percentage=improvement,
            recommended_changes=[f"Switch from {model_a} to {model_b}"],
            a_b_test_results={
                "test_cases": len(test_cases),
                "winner": winner,
                "improvement": f"{improvement:.1f}%",
                "statistical_significance": self._calculate_significance(perf_a, perf_b, test_cases)
            }
        )
        
        self.logger.info(f"A/B test completed. Winner: {winner}")
        return result
    
    def _calculate_significance(self, perf_a: ModelPerformance, perf_b: ModelPerformance, 
                              test_cases: List[Dict]) -> str:
        """Calculate statistical significance of A/B test results."""
        # Simplified significance calculation
        if len(test_cases) < 30:
            return "Insufficient sample size"
        
        # Mock statistical test - in real implementation, use proper statistical tests
        improvement = perf_b.user_satisfaction - perf_a.user_satisfaction
        pooled_std = (perf_a.user_satisfaction + perf_b.user_satisfaction) / 2
        
        # Z-score approximation
        z_score = improvement / (pooled_std / (len(test_cases) ** 0.5))
        
        if abs(z_score) > 1.96:
            return "Statistically significant (p < 0.05)"
        elif abs(z_score) > 1.645:
            return "Marginally significant (p < 0.1)"
        else:
            return "Not statistically significant"


class DataRefresher:
    """Handles data refresh and quality improvement."""
    
    def __init__(self, data_source: str = "data/processed/restaurants_phase1.csv"):
        self.data_source = data_source
        self.logger = logging.getLogger(__name__)
        self.refresh_history = []
        
    def check_data_freshness(self) -> Dict:
        """Check if data needs refresh."""
        try:
            # Get file modification time
            import os
            file_mtime = os.path.getmtime(self.data_source)
            file_age_days = (datetime.now() - datetime.fromtimestamp(file_mtime)).days
            
            # Load data to check quality
            df = pd.read_csv(self.data_source)
            
            # Data quality checks
            null_counts = df.isnull().sum().to_dict()
            total_records = len(df)
            
            # Calculate data quality score
            quality_issues = sum(null_counts.values())
            quality_score = 1.0 - (quality_issues / (total_records * len(df.columns)))
            
            return {
                "data_age_days": file_age_days,
                "total_records": total_records,
                "null_counts": null_counts,
                "quality_score": quality_score,
                "needs_refresh": file_age_days > 30 or quality_score < 0.8,
                "recommendations": self._generate_refresh_recommendations(file_age_days, quality_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error checking data freshness: {e}")
            return {"error": str(e)}
    
    def _generate_refresh_recommendations(self, age_days: int, quality_score: float) -> List[str]:
        """Generate data refresh recommendations."""
        recommendations = []
        
        if age_days > 30:
            recommendations.append("Data is over 30 days old - consider refreshing from source")
        
        if age_days > 90:
            recommendations.append("Data is over 90 days old - immediate refresh recommended")
        
        if quality_score < 0.9:
            recommendations.append("Data quality score below 90% - investigate missing values")
        
        if quality_score < 0.7:
            recommendations.append("Data quality score below 70% - comprehensive data cleaning needed")
        
        return recommendations
    
    def refresh_data(self, source_url: Optional[str] = None) -> Dict:
        """Refresh data from source."""
        self.logger.info("Starting data refresh process")
        
        try:
            if source_url:
                # In real implementation, fetch from external API
                self.logger.info(f"Fetching data from: {source_url}")
                # Mock: df = pd.read_json(source_url)
                df = pd.read_csv(self.data_source)  # Fallback for demo
            else:
                # Re-process existing data
                self.logger.info("Re-processing existing data")
                df = pd.read_csv(self.data_source)
                
                # Data cleaning and enhancement
                df = self._clean_and_enhance_data(df)
            
            # Save refreshed data
            df.to_csv(self.data_source, index=False)
            
            refresh_entry = {
                "timestamp": datetime.now().isoformat(),
                "source": source_url or "reprocessing",
                "records_processed": len(df),
                "status": "success"
            }
            
            self.refresh_history.append(refresh_entry)
            
            self.logger.info(f"Data refresh completed. Processed {len(df)} records")
            
            return {
                "status": "success",
                "records_processed": len(df),
                "timestamp": refresh_entry["timestamp"]
            }
            
        except Exception as e:
            error_entry = {
                "timestamp": datetime.now().isoformat(),
                "source": source_url or "reprocessing",
                "status": "error",
                "error": str(e)
            }
            
            self.refresh_history.append(error_entry)
            self.logger.error(f"Data refresh failed: {e}")
            
            return {
                "status": "error",
                "error": str(e),
                "timestamp": error_entry["timestamp"]
            }
    
    def _clean_and_enhance_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and enhance restaurant data."""
        # Remove duplicates
        df = df.drop_duplicates(subset=['restaurant_name', 'location'])
        
        # Standardize location names
        df['location'] = df['location'].str.title().str.strip()
        
        # Standardize cuisine names
        df['cuisines'] = df['cuisines'].str.title().str.strip()
        
        # Fill missing values with defaults
        df['rating'] = df['rating'].fillna(df['rating'].median())
        df['cost_for_two'] = df['cost_for_two'].fillna(800)  # Default cost
        
        # Add quality score based on completeness
        completeness_score = (
            df['restaurant_name'].notna().astype(int) +
            df['location'].notna().astype(int) +
            df['cuisines'].notna().astype(int) +
            df['rating'].notna().astype(int) +
            df['cost_for_two'].notna().astype(int)
        ) / 5
        
        df['quality_score'] = completeness_score
        
        return df
    
    def get_refresh_history(self, days: int = 30) -> List[Dict]:
        """Get data refresh history."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_history = [
            entry for entry in self.refresh_history
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        
        return recent_history
