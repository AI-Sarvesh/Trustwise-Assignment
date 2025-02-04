# New file for monitoring configuration
PERFORMANCE_THRESHOLDS = {
    'response_time_max': 2.0,
    'memory_usage_max': 1024 * 1024 * 1024,
    'cpu_usage_max': 80,
    'error_rate_max': 0.01,
    'concurrent_users_max': 1000
}

METRICS_CONFIG = {
    'enable_prometheus': True,
    'collection_interval': 15,  # seconds
    'retention_days': 30
}

# Move these from monitoring.py
METRIC_NAMES = {
    'http_requests': 'http_requests_total',
    'response_time': 'http_response_time_seconds',
    'errors': 'http_errors_total',
    'active_users': 'active_users',
    'model_accuracy': 'model_accuracy',
    'memory_usage': 'memory_usage_bytes',
    'cpu_usage': 'cpu_usage_percent',
    'request_size': 'http_request_size_bytes',
    'response_size': 'http_response_size_bytes',
    'db_query_time': 'db_query_duration_seconds'
} 