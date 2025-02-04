from locust import HttpUser, task, between, events
import json
import random
import time
from .utils.test_utils import TestUtils
from app.config.monitoring import PERFORMANCE_THRESHOLDS

class TextAnalysisUser(HttpUser):
    wait_time = between(1, 3)
    host = TestUtils.BASE_URL
    
    def on_start(self):
        """Initialize test data"""
        self.test_texts = self.environment.runner.test_texts
        
    @task(3)
    def analyze_text(self):
        """Test text analysis with random text samples"""
        text = random.choice(self.test_texts)
        start_time = time.time()
        
        with self.client.post(
            "/analyze",
            json={"text": text},
            catch_response=True
        ) as response:
            response_time = time.time() - start_time
            
            # Use shared performance check
            is_performance_ok, message = TestUtils.check_performance(
                response_time, 
                "/analyze"
            )
            if not is_performance_ok:
                response.failure(message)
            
            if response.status_code == 200:
                self._validate_analysis_response(response)
            else:
                response.failure(f"Request failed with status {response.status_code}")
    
    def _validate_analysis_response(self, response):
        """Validate analysis response"""
        data = response.json()
        if not all(k in data for k in ["emotion_scores", "hallucination_score"]):
            response.failure("Missing required fields in response")
        if not (0 <= data.get("hallucination_score", -1) <= 1):
            response.failure("Invalid hallucination score range")

    @task(1)
    def get_history(self):
        """Test history retrieval with performance monitoring"""
        start_time = time.time()
        
        with self.client.get("/history", catch_response=True) as response:
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Performance checks
                if response_time > 1.0:  # 1 second threshold
                    response.failure(f"History retrieval too slow: {response_time}s")
                
                # Data structure validation
                if not isinstance(data, list):
                    response.failure("History response is not a list")
                
                # Size limits
                if len(data) > 1000:  # Example threshold
                    response.failure("History response too large")
            else:
                response.failure(f"History request failed with status {response.status_code}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Initialize test environment"""
    print("Starting load test...")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Generate test summary"""
    print("Load test completed") 