// Use localhost when running in browser, and backend service name when in Docker
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'; 