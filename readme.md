# Text Analysis API

This project provides a comprehensive text analysis API built with FastAPI for the backend and a React frontend. It includes features for emotion analysis, hallucination detection, and performance monitoring using Prometheus.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Docker Setup](#docker-setup)
- [Local Development Setup](#local-development-setup)
- [Backend](#backend)
- [Frontend](#frontend)
- [Prometheus Monitoring](#prometheus-monitoring)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Emotion Analysis**: Analyze text to detect top 3 emotions using Hugging Face's emotion-english-distilroberta-base model
- **Real-time Processing**: Fast and efficient text analysis
- **Performance Monitoring**: Monitor API performance and resource usage with Prometheus
- **Rate Limiting**: Control the number of requests to the API
- **History Retrieval**: Access previous analysis results
- **Docker Support**: Easy deployment with Docker containers

## Technologies

- **Backend**: 
  - FastAPI
  - SQLAlchemy
  - Pydantic
  - Hugging Face Transformers
- **Frontend**: 
  - React
  - Vite
  - Tailwind CSS
- **Database**: SQLite
- **Containerization**: Docker & Docker Compose
- **Monitoring**: Prometheus
- **Testing**: Pytest, Locust

## Prerequisites

- Docker and Docker Compose
- Git
- Node.js 16+ (for local development)
- Python 3.10+ (for local development)

## Docker Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and Start Containers**:
   ```bash
   docker compose build --no-cache
   docker compose up
   ```

3. **Access the Applications**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Prometheus: http://localhost:9090

4. **Stop the Containers**:
   ```bash
   docker compose down
   ```

5. **View Logs**:
   ```bash
   # All services
   docker compose logs

   # Specific service
   docker compose logs backend
   docker compose logs frontend
   ```

6. **Rebuild Single Service**:
   ```bash
   docker compose build backend
   # or
   docker compose build frontend
   ```

## Local Development Setup

### Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:
   ```env
   DATABASE_URL=sqlite:///./analysis.db
   FRONTEND_URL=http://localhost:5173
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

## Prometheus Monitoring

Prometheus is configured to collect metrics from the backend API. Key metrics include:
- Request latency
- Request count
- Error rates
- Resource usage

### Accessing Metrics

1. View raw metrics: http://localhost:8000/metrics
2. Access Prometheus UI: http://localhost:9090

## Running Tests

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### Common Docker Issues

1. **Port Conflicts**:
   ```bash
   # Check for port usage
   lsof -i :5173
   lsof -i :8000
   ```

2. **Container Cleanup**:
   ```bash
   # Remove all stopped containers
   docker container prune

   # Remove all unused images
   docker image prune -a
   ```

3. **Reset Everything**:
   ```bash
   docker compose down -v
   docker system prune -a
   ```

