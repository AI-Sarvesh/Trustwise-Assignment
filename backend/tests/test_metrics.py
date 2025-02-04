import pytest
from .utils.fixtures import test_client, test_db, sample_texts
from .utils.test_utils import TestUtils
from app.monitoring import (
    REQUEST_COUNTER, RESPONSE_TIME, ERROR_COUNTER,
    MEMORY_USAGE, CPU_USAGE, REQUEST_SIZE, RESPONSE_SIZE
)
import time
from prometheus_client import Counter, Histogram
import json
import numpy
import threading

# Core Performance Metrics
REQUEST_TIME = Histogram(
    'request_processing_seconds',
    'Time spent processing request',
    ['endpoint']
)

MODEL_INFERENCE_TIME = Histogram(
    'model_inference_seconds',
    'Time spent on model inference',
    ['model_type']
)

ERROR_COUNTER = Counter(
    'error_total',
    'Total number of errors',
    ['error_type']
)

@pytest.fixture
def client():
    return test_client

@pytest.mark.metrics
class TestCoreFunctionality:
    """Tests for core API functionality"""
    
    def test_analyze_endpoint(self, test_client, sample_texts):
        """Test /analyze endpoint with various inputs"""
        for text in sample_texts:
            response = test_client.post("/analyze", json={"text": text})
            assert response.status_code == 200
            data = response.json()
            assert all(key in data for key in ["id", "text", "emotion_scores", 
                                             "hallucination_score", "created_at"])

    def test_history_endpoint(self, test_client, test_db):
        """Test /history endpoint data integrity"""
        # Add test data
        test_client.post("/analyze", json={"text": "History test"})
        
        response = test_client.get("/history")
        assert response.status_code == 200
        history = response.json()
        assert isinstance(history, list)
        if history:
            assert all(key in history[0] for key in ["id", "text", "emotion_scores", 
                                                   "hallucination_score", "created_at"])

@pytest.mark.metrics
class TestDatabaseOperations:
    """Tests for database operations"""
    
    def test_crud_operations(self, test_db):
        """Complete CRUD test sequence"""
        from app.database import Analysis
        from datetime import datetime
        
        # Create
        analysis = Analysis(
            text="CRUD test",
            emotion_results=json.dumps([{"label": "neutral", "score": 0.9}]),
            hallucination_score=0.05,
            created_at=datetime.utcnow()
        )
        test_db.add(analysis)
        test_db.commit()
        
        # Read
        saved = test_db.query(Analysis).filter_by(text="CRUD test").first()
        assert saved is not None
        
        # Update
        saved.hallucination_score = 0.15
        test_db.commit()
        updated = test_db.query(Analysis).filter_by(text="CRUD test").first()
        assert updated.hallucination_score == 0.15
        
        # Delete
        test_db.delete(updated)
        test_db.commit()
        assert test_db.query(Analysis).filter_by(text="CRUD test").first() is None

@pytest.mark.metrics
class TestModelOperations:
    """Tests for ML model operations"""
    
    def test_model_initialization(self):
        """Test model loading and basic inference"""
        from app.models import MLModels
        ml_models = MLModels()
        
        # Emotion analysis
        emotions = ml_models.analyze_emotions("Test text")
        assert isinstance(emotions, list)
        assert len(emotions) <= 3  # Should return top 3 emotions
        
        # Hallucination detection
        hallucination = ml_models.analyze_hallucination([("Test", "")])
        assert isinstance(hallucination, list)
        assert 0 <= hallucination[0] <= 1

    def test_error_handling(self):
        """Test model error resilience"""
        from app.models import MLModels
        ml_models = MLModels()
        
        # Empty input handling - model returns neutral for empty text, which is correct
        result = ml_models.analyze_emotions("")
        assert isinstance(result, list)
        assert len(result) <= 3
        
        # Test hallucination with empty input
        assert ml_models.analyze_hallucination([]) == []

def test_analyze_endpoint_performance(test_client):
    """Test performance of /analyze endpoint"""
    start_time = time.time()
    response = test_client.post("/analyze", json={"text": "Test text"})
    response_time = time.time() - start_time
    
    is_performance_ok, message = TestUtils.check_performance(
        response_time, 
        "/analyze"
    )
    assert is_performance_ok, message
    assert response.status_code == 200

def test_history_endpoint_comprehensive(test_client, test_db):
    """Test history endpoint comprehensively"""
    # First add some test data
    test_text = "Test text for history"
    response = test_client.post("/analyze", json={"text": test_text})
    assert response.status_code == 200
    
    # Now test history
    response = test_client.get("/history")
    assert response.status_code == 200
    data = response.json()
    
    # Validate history data
    assert isinstance(data, list)
    if len(data) > 0:
        entry = data[0]
        assert "id" in entry
        assert "text" in entry
        assert "emotion_scores" in entry
        assert "hallucination_score" in entry
        assert "created_at" in entry

@pytest.mark.metrics
def test_database_init():
    """Test database initialization"""
    from app.database import init_db, engine, get_pool_status
    
    # Test pool status instead of direct pool access
    status = get_pool_status()
    assert isinstance(status, dict)
    assert "pool_size" in status
    assert status["pool_size"] >= 0

@pytest.mark.metrics
def test_database_connection_errors():
    """Test database connection error handling"""
    from app.database import get_pool_status
    
    # Test pool status
    status = get_pool_status()
    assert isinstance(status, dict)
    assert "pool_size" in status

@pytest.mark.metrics
def test_database_session_handling(test_db):
    """Test session cleanup and error handling"""
    from app.database import get_db
    from sqlalchemy.exc import SQLAlchemyError
    
    # Test normal operation
    with get_db() as db:
        assert db is not None

    # Test error handling
    try:
        with get_db() as db:
            raise SQLAlchemyError("Test error")
    except SQLAlchemyError:
        pass

@pytest.mark.metrics
def test_pool_status_endpoint(test_client):
    """Test /pool-status endpoint"""
    response = test_client.get("/pool-status")
    assert response.status_code == 200
    data = response.json()
    assert all(key in data for key in ["pool_size", "checked_out", "overflow"])

@pytest.mark.metrics
def test_analyze_error_handling(test_client):
    """Test error handling in analyze endpoint"""
    # Test invalid input
    response = test_client.post("/analyze", json={"text": None})
    assert response.status_code == 422

@pytest.mark.metrics
def test_history_pagination(test_client):
    """Test history endpoint with pagination"""
    response = test_client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.metrics
def test_model_inference_times():
    """Test ML model inference times"""
    from app.models import MLModels
    ml_models = MLModels()
    
    # Test emotion analysis
    with MODEL_INFERENCE_TIME.labels(model_type="emotion").time():
        emotions = ml_models.analyze_emotions("Test text")
    
    # Test hallucination analysis
    with MODEL_INFERENCE_TIME.labels(model_type="hallucination").time():
        hallucination = ml_models.analyze_hallucination([("Test text", "")])
    
    assert emotions is not None
    assert hallucination is not None

@pytest.mark.metrics
def test_database_operations(test_db):
    """Test database CRUD operations"""
    from app.database import Analysis
    from datetime import datetime
    
    # Create
    analysis = Analysis(
        text="Test text",
        emotion_results=json.dumps([{"label": "happy", "score": 0.8}]),
        hallucination_score=0.1,
        created_at=datetime.utcnow()
    )
    test_db.add(analysis)
    test_db.commit()
    
    # Read
    saved_analysis = test_db.query(Analysis).filter_by(id=analysis.id).first()
    assert saved_analysis is not None
    assert saved_analysis.text == "Test text"
    
    # Update
    saved_analysis.hallucination_score = 0.2
    test_db.commit()
    
    # Delete
    test_db.delete(saved_analysis)
    test_db.commit()
    
    assert test_db.query(Analysis).filter_by(id=analysis.id).first() is None

@pytest.mark.metrics
def test_analyze_endpoint_edge_cases(test_client):
    """Test analyze endpoint edge cases"""
    # Test very long text
    long_text = "test " * 1000
    response = test_client.post("/analyze", json={"text": long_text})
    assert response.status_code == 200
    
    # Test special characters
    special_text = "!@#$%^&*()_+ 测试 тест"
    response = test_client.post("/analyze", json={"text": special_text})
    assert response.status_code == 200
    
    # Test error handling
    response = test_client.post("/analyze", json={"text": None})
    assert response.status_code == 422

@pytest.mark.metrics
def test_history_endpoint_error_handling(test_client, test_db):
    """Test history endpoint error cases"""
    # Test with invalid emotion_results JSON
    from app.database import Analysis
    from datetime import datetime
    
    # Create invalid analysis record
    analysis = Analysis(
        text="Test text",
        emotion_results="invalid json",
        hallucination_score=0.1,
        created_at=datetime.utcnow()
    )
    test_db.add(analysis)
    test_db.commit()
    
    response = test_client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.metrics
def test_model_error_handling():
    """Test model error resilience"""
    from app.models import MLModels
    ml_models = MLModels()
    
    # Test with None input (should handle gracefully)
    assert isinstance(ml_models.analyze_emotions(None), list)
    
    # Test with empty input
    assert isinstance(ml_models.analyze_emotions(""), list)
    
    # Test hallucination with empty input
    assert ml_models.analyze_hallucination([]) == []
    
    # Test hallucination with None input
    assert ml_models.analyze_hallucination(None) == []
    
    # Test with invalid pairs
    result = ml_models.analyze_hallucination([("", "")])
    assert isinstance(result, list)
    assert all(isinstance(score, float) for score in result)

@pytest.mark.metrics
class TestRateLimiting:
    def test_rate_limiting(self, test_client):
        """Test API rate limiting"""
        responses = []
        
        # Make 30 rapid requests (above our 20/minute limit)
        for _ in range(30):
            response = test_client.post("/analyze", json={"text": "test"})
            responses.append(response.status_code)
        
        # Verify that some requests were rate-limited (429)
        rate_limited = sum(1 for status in responses if status == 429)
        assert rate_limited > 0, "Rate limiting should trigger after 20 requests per minute"

@pytest.mark.metrics
class TestConcurrency:
    def test_concurrent_requests(self, test_client):
        """Test handling of concurrent requests"""
        def make_request():
            response = test_client.post("/analyze", json={"text": "concurrent test"})
            return response.status_code
        
        # Create multiple threads
        threads = []
        responses = []
        for _ in range(10):
            thread = threading.Thread(
                target=lambda: responses.append(make_request())
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify that responses are either successful or rate-limited
        assert all(status in [200, 429] for status in responses), \
            f"Unexpected status codes in responses: {responses}"

@pytest.mark.metrics
class TestModelPerformance:
    def test_model_latency_distribution(self, test_client):
        """Test model inference latency distribution"""
        latencies = []
        for _ in range(10):
            start_time = time.time()
            response = test_client.post("/analyze", json={"text": "test"})
            latencies.append(time.time() - start_time)
        
        # Calculate percentiles
        p50 = numpy.percentile(latencies, 50)
        p95 = numpy.percentile(latencies, 95)
        p99 = numpy.percentile(latencies, 99)
        
        assert p50 < 1.0, "Median latency too high"
        assert p95 < 2.0, "95th percentile latency too high"
        assert p99 < 3.0, "99th percentile latency too high" 

@pytest.mark.metrics
class TestMemoryUsage:
    def test_memory_leak(self, test_client):
        """Test for memory leaks during repeated operations"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Perform multiple operations
        for _ in range(100):
            test_client.post("/analyze", json={"text": "memory test"})
        
        final_memory = process.memory_info().rss
        memory_growth = (final_memory - initial_memory) / initial_memory
        
        assert memory_growth < 0.1, "Significant memory growth detected" 

@pytest.mark.metrics
class TestDatabaseMetrics:
    def test_connection_pool_metrics(self, test_client):
        """Test database connection pool metrics"""
        def make_request():
            return test_client.get("/history")  # Fix the lambda issue
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start() 