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
## Deployment Instructions

### Preparing for Deployment

1. **Update API URLs**:

   In `frontend/src/api/index.js`:
   ```javascript
   // Replace these URLs with your deployed backend URLs
   const ANALYZE_URL = 'https://your-backend-domain/analyze';
   const HISTORY_URL = 'https://your-backend-domain/history';
   ```

2. **Update CORS Settings**:

   In `backend/app/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://your-frontend-domain",
           "https://*.your-domain.com"  # If using subdomains
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"]
   )
   ```

### Docker Image Usage

1. **Pull the Docker Images**:
   ```bash
   docker pull aisarvesh/text-analysis-backend:latest
   docker pull aisarvesh/text-analysis-frontend:latest
   ```

2. **Run the Containers**:
   ```bash
   # Run backend
   docker run -d -p 8000:8000 \
     -e DATABASE_URL=sqlite:///./analysis.db \
     -e FRONTEND_URL=https://your-frontend-domain \
     aisarvesh/text-analysis-backend:latest

   # Run frontend
   docker run -d -p 5173:5173 \
     -e VITE_API_URL=https://your-backend-domain \
     aisarvesh/text-analysis-frontend:latest
   ```

3. **Environment Variables**:

   Backend:
   - `DATABASE_URL`: Your database connection string
   - `FRONTEND_URL`: Your frontend application URL

   Frontend:
   - `VITE_API_URL`: Your backend API URL

### Deployment Checklist

1. [ ] Update API URLs in frontend code
2. [ ] Update CORS settings in backend
3. [ ] Configure environment variables
4. [ ] Set up SSL/TLS certificates
5. [ ] Configure domain names
6. [ ] Set up database (if using external database)
7. [ ] Test API connectivity
8. [ ] Verify CORS settings
9. [ ] Check security headers

### Production Considerations

1. **SSL/TLS**: Ensure both frontend and backend use HTTPS
2. **Database**: Consider using a production-grade database instead of SQLite
3. **Monitoring**: Set up proper monitoring and logging
4. **Backups**: Implement regular database backups
5. **Rate Limiting**: Adjust rate limits based on your needs
6. **Security**: Review and implement security best practices

### Troubleshooting Deployment

1. **CORS Issues**:
   - Verify frontend URL in backend CORS settings
   - Check for exact URL matches (including http/https)
   - Use browser dev tools to inspect CORS errors

2. **API Connection**:
   - Verify API URLs are correct
   - Check network tab in browser dev tools
   - Ensure ports are properly exposed

3. **Database Issues**:
   - Verify database connection string
   - Check database permissions
   - Ensure migrations are applied

4. **Container Health**:
   ```bash
   # Check container logs
   docker logs <container_id>

   # Check container status
   docker ps -a
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

