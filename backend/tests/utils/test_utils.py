import requests
import time
from fastapi.testclient import TestClient
from app.main import app
from app.config.monitoring import PERFORMANCE_THRESHOLDS

class TestUtils:
    BASE_URL = "http://localhost:8000"
    
    @staticmethod
    def get_test_client():
        """Get FastAPI test client"""
        return TestClient(app)
    
    @staticmethod
    def is_service_up():
        """Check if service is responding"""
        try:
            response = requests.get(f"{TestUtils.BASE_URL}/")
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def wait_for_service(timeout=60):
        """Wait for service to become available"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if TestUtils.is_service_up():
                return True
            time.sleep(1)
        return False
    
    @staticmethod
    def check_performance(response_time, endpoint):
        """Check if response time is within threshold"""
        threshold = PERFORMANCE_THRESHOLDS['response_time_max']
        return response_time <= threshold, f"Response time {response_time}s exceeds threshold {threshold}s for {endpoint}" 