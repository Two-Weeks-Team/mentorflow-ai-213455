import os
from sqlalchemy import Column, Integer, String, JSON, DateTime, func, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Resolve DATABASE URL with automatic fixes
raw_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "sqlite:///./app.db"
if raw_url.startswith("postgresql+asyncpg://"):
    raw_url = raw_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql+psycopg://")

# Determine if we need SSL (non‑localhost & not sqlite)
use_ssl = not ("localhost" in raw_url or raw_url.startswith("sqlite"))
connect_args = {"sslmode": "require"} if use_ssl else {}

engine = create_engine(raw_url, connect_args=connect_args, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

class Session(Base):
    __tablename__ = "mf_sessions"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create tables if they don't exist (useful for demo environments)
Base.metadata.create_all(bind=engine)
