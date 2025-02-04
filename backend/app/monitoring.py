from prometheus_client import Counter, Histogram, Gauge, Summary
import time
import psutil

# Metrics
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests')
RESPONSE_TIME = Histogram('http_response_time_seconds', 'Response time in seconds')
ERROR_COUNTER = Counter('http_errors_total', 'Total HTTP errors')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')
MODEL_ACCURACY = Gauge('model_accuracy', 'Model accuracy score')

# New metrics for non-functional aspects
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
REQUEST_SIZE = Summary('http_request_size_bytes', 'Request size in bytes')
RESPONSE_SIZE = Summary('http_response_size_bytes', 'Response size in bytes')
DB_QUERY_TIME = Histogram('db_query_duration_seconds', 'Database query duration')

class MetricsMiddleware:
    async def __call__(self, request, call_next):
        REQUEST_COUNTER.inc()
        start_time = time.time()
        
        # Track system resources
        MEMORY_USAGE.set(psutil.Process().memory_info().rss)
        CPU_USAGE.set(psutil.Process().cpu_percent())
        
        # Track request size
        content_length = request.headers.get('content-length')
        if content_length:
            REQUEST_SIZE.observe(int(content_length))
        
        try:
            response = await call_next(request)
            
            # Track response size
            resp_size = len(response.body) if hasattr(response, 'body') else 0
            RESPONSE_SIZE.observe(resp_size)
            
            return response
        except Exception as e:
            ERROR_COUNTER.inc()
            raise e
        finally:
            RESPONSE_TIME.observe(time.time() - start_time) 