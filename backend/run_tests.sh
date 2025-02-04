#!/bin/bash

echo "🧪 Starting Test Suite..."

# Run unit tests with coverage
echo "\n📊 Running Unit Tests and Coverage..."
pytest tests/test_metrics.py -v --cov=app --cov-report=term-missing

# Run load tests
echo "\n🔄 Running Load Tests..."
echo "Starting Locust in headless mode..."
locust -f tests/load_test.py --headless -u 10 -r 2 --run-time 30s --host http://localhost:8000

echo "\n✅ All tests completed!"