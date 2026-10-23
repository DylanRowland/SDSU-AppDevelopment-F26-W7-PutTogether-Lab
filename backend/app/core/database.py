"""SQLAlchemy engine and request-scoped database sessions."""

# Generator lets FastAPI receive a session and then close it afterward.
from collections.abc import Generator

# HTTPException turns missing configuration into a readable API response.
from fastapi import HTTPException

# SQLAlchemy provides the engine, session type, and session factory.
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Read the connection string from the shared configuration module.
from app.core.config import DATABASE_URL

# Create the engine only when a URL exists. The URL is supplied by Compose.
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None

# SessionLocal creates one database session for each API request.
SessionLocal = (
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
    if engine
    else None
)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session to a route and close it afterward."""

    # This makes an unconnected lab setup fail with a useful 503 response.
    if SessionLocal is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not configured. This is an intentional lab breakpoint.",
        )

    # Open a session for the current request.
    db = SessionLocal()
    try:
        # FastAPI pauses here while the route uses this session.
        yield db
    finally:
        # Always release the connection when the request is complete.
        db.close()
