from sqlalchemy import create_engine, Column, Integer, Text, Float, DateTime, Index, String
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings
import os
from datetime import datetime
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the database directory if it doesn't exist
db_path = settings.DATABASE_URL.replace('sqlite:///', '')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # Maximum number of connections in the pool
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Enable connection health checks
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Context manager for database sessions
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    emotion_results = Column(String)  # JSON string
    hallucination_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Add index for timestamp queries
    __table_args__ = (
        Index('idx_created_at', created_at.desc()),
    )

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

# Initialize the database
init_db()

# Connection pool monitoring
def get_pool_status():
    """Get current status of the connection pool"""
    return {
        "pool_size": engine.pool.size(),
        "checked_out": engine.pool.checkedin(),
        "overflow": engine.pool.overflow(),
        "checkedout": engine.pool.checkedout(),
    } 