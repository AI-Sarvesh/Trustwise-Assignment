import pytest
import time
from .utils.test_utils import TestUtils

@pytest.mark.reliability
class TestSystemReliability:
    """Comprehensive reliability tests"""
    
    def test_service_recovery(self):
        """Test automatic service recovery"""
        assert TestUtils.wait_for_service(timeout=30), "Service recovery failed"
    
    def test_high_availability(self, test_client):
        """Test sustained operation under load"""
        for _ in range(20):  # Increased load test
            response = test_client.get("/health")
            assert response.status_code == 200
            time.sleep(0.05)

@pytest.mark.reliability
class TestPerformanceMetrics:
    """Performance metric validation tests"""
    
    def test_response_times(self, test_client):
        """Validate response time thresholds"""
        endpoints = [
            ("/", "GET"),
            ("/analyze", "POST"),
            ("/history", "GET")
        ]
        
        for endpoint, method in endpoints:
            start = time.time()
            if method == "POST":
                response = test_client.post(endpoint, json={"text": "test"})
            else:
                response = test_client.get(endpoint)
            
            response_time = time.time() - start
            assert response_time < 2.0, f"Slow response at {endpoint}: {response_time}s"
            assert response.status_code in [200, 422]

@pytest.mark.reliability
class TestMetricsMiddleware:
    """Group all metrics middleware tests"""
    
    def test_request_tracking(self, test_client):
        """Test request tracking"""
        from app.monitoring import REQUEST_COUNTER, ERROR_COUNTER
        
        # Normal request
        initial_requests = float(REQUEST_COUNTER._value.get())
        response = test_client.get("/")
        assert float(REQUEST_COUNTER._value.get()) > initial_requests
        
        # Error request
        initial_errors = float(ERROR_COUNTER._value.get())
        response = test_client.get("/nonexistent")
        assert float(ERROR_COUNTER._value.get()) > initial_errors
    
    def test_resource_metrics(self, test_client):
        """Test resource metrics"""
        from app.monitoring import MEMORY_USAGE, CPU_USAGE
        
        assert float(MEMORY_USAGE._value.get()) > 0
        assert float(CPU_USAGE._value.get()) >= 0
    
    def test_content_length(self, test_client):
        """Test content-length handling"""
        response = test_client.post(
            "/analyze",
            json={"text": "test"},
            headers={"content-length": "100"}
        )
        assert response.status_code == 200

@pytest.mark.reliability
def test_metrics_middleware(test_client):
    """Test metrics middleware functionality"""
    from app.monitoring import (
        REQUEST_COUNTER, ERROR_COUNTER,
        MEMORY_USAGE, CPU_USAGE
    )
    
    # Get initial values
    initial_requests = REQUEST_COUNTER._value.get()
    initial_errors = ERROR_COUNTER._value.get()
    
    # Make valid request
    test_client.get("/")
    assert REQUEST_COUNTER._value.get() > initial_requests
    
    # Make invalid request
    test_client.get("/invalid-endpoint")
    assert ERROR_COUNTER._value.get() > initial_errors
    
    # Verify resource metrics
    assert MEMORY_USAGE._value.get() > 0
    assert CPU_USAGE._value.get() >= 0 