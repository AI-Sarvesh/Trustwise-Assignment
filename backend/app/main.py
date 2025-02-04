import json
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .models import MLModels
from .database import SessionLocal, Analysis, init_db, get_pool_status
from datetime import datetime
from .config.base import settings
import logging
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events handler"""
    # Startup
    init_db()
    logger.info("Database initialized with connection pool")
    yield
    # Shutdown
    logger.info("Shutting down application")

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML models
ml_models = MLModels()

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AnalysisRequest(BaseModel):
    text: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Text Analysis API"}

@app.get("/pool-status")
async def pool_status():
    """Monitor connection pool status"""
    return get_pool_status()

@app.post("/analyze")
@limiter.limit("20/minute")  # Limit to 20 requests per minute
async def analyze_text(request: Request, text_input: AnalysisRequest, db: Session = Depends(get_db)):
    try:
        # Analyze emotions
        emotion_results = ml_models.analyze_emotions(text_input.text)
        
        # Log emotion results for debugging
        logger.info(f"Emotion results: {emotion_results}")
        
        # Sort emotions by score and get top 3
        sorted_emotions = sorted(emotion_results, key=lambda x: x['score'], reverse=True)[:3]
        
        # Create analysis record
        analysis = Analysis(
            text=text_input.text,
            emotion_results=json.dumps(sorted_emotions),
            hallucination_score=float(ml_models.analyze_hallucination([(text_input.text, "")])[0]),
            created_at=datetime.utcnow()
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        # Return consistent format
        return {
            "id": analysis.id,
            "text": analysis.text,
            "emotion_scores": {
                emotion['label']: emotion['score']
                for emotion in sorted_emotions
            },
            "hallucination_score": analysis.hallucination_score,
            "created_at": analysis.created_at
        }

    except Exception as e:
        logger.error(f"Error in analyze_text: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(db: Session = Depends(get_db)):
    try:
        analyses = db.query(Analysis).order_by(Analysis.created_at.desc()).all()
        results = []
        for analysis in analyses:
            try:
                # Parse stored emotions and convert to consistent format
                emotion_list = json.loads(analysis.emotion_results)
                emotion_scores = {
                    emotion['label']: emotion['score']
                    for emotion in emotion_list
                }
                
                results.append({
                    "id": analysis.id,
                    "text": analysis.text,
                    "emotion_scores": emotion_scores,
                    "hallucination_score": float(analysis.hallucination_score),
                    "created_at": analysis.created_at
                })
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing emotion results for analysis {analysis.id}: {str(e)}")
                continue

        return results
    except Exception as e:
        logger.error(f"Error in get_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

##uvicorn app.main:app --reload


