# Text Analysis API

This project provides a comprehensive text analysis API built with FastAPI for the backend and a React frontend. It includes features for emotion analysis, hallucination detection, and performance monitoring using Prometheus.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Backend](#backend)
- [Frontend](#frontend)
- [Prometheus Monitoring](#prometheus-monitoring)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Emotion Analysis**: Analyze text to detect emotions.
- **Hallucination Detection**: Evaluate the reliability of the text.
- **Performance Monitoring**: Monitor API performance and resource usage with Prometheus.
- **Rate Limiting**: Control the number of requests to the API.
- **History Retrieval**: Access previous analysis results.

## Technologies

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React, Vite, Tailwind CSS
- **Database**: SQLite
- **Monitoring**: Prometheus
- **Testing**: Pytest, Locust

## Backend

The backend is built using FastAPI and provides RESTful endpoints for text analysis. It includes:

- **Endpoints**:
  - `POST /analyze`: Analyze text for emotions and hallucination scores.
  - `GET /history`: Retrieve analysis history.
  - `GET /pool-status`: Monitor database connection pool status.
  - `GET /metrics`: Expose metrics for Prometheus.

### Setup

1. Navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file.

## Frontend

The frontend is built with React and Vite, providing a user-friendly interface for interacting with the API. It includes:

- **Components**:
  - Text input for analysis.
  - Display of analysis results and history.
  - Graphs for visualizing hallucination scores and emotions.

### Setup

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Prometheus Monitoring

Prometheus is used for monitoring the backend API's performance and resource usage. The configuration file is located in the `prometheus` directory.

### Setup

1. Navigate to the `prometheus` directory.
2. Start Prometheus with the configuration:
   ```bash
   prometheus --config.file=prometheus.yml
   ```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Follow the setup instructions for both the backend and frontend.

## Usage

1. Start the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
2. Start the frontend server as described above.
3. Access the application at `http://localhost:5173`.

## Running Tests

To run tests for the backend, navigate to the `backend` directory and execute:
To ensure the backend is functioning correctly, you can run the tests using Pytest. Follow these steps:

1. **Navigate to the Backend Directory**:
   Open your terminal and change to the backend directory:
   ```bash
   cd backend
   ```

2. **Run Tests**:
   Execute the following command to run all tests:
   ```bash
   pytest
   ```
   This command will discover and run all test files that match the pattern `test_*.py` or `*_test.py` in the backend directory.

3. **View Test Results**:
   After running the tests, Pytest will provide a summary of the test results in the terminal. You will see how many tests passed, failed, or were skipped.

4. **Running Specific Tests**:
   If you want to run a specific test file, you can specify the file name:
   ```bash
   pytest tests/test_file.py
   ```

5. **Running Tests with Coverage**:
   To check the test coverage, you can use the `pytest-cov` plugin. First, ensure it is installed:
   ```bash
   pip install pytest-cov
   ```
   Then run:
   ```bash
   pytest --cov=app
   ```
   This will show you the coverage report for the `app` module.
