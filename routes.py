from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from models import Session, SessionLocal
from ai_service import call_inference

router = APIRouter()

class PlanRequest(BaseModel):
    query: str
    preferences: List[str] = Field(default_factory=list)

class PlanResponse(BaseModel):
    summary: str
    items: List[str]
    score: float
    note: str | None = None

class InsightsRequest(BaseModel):
    selection: str
    context: str

class InsightsResponse(BaseModel):
    insights: str
    next_actions: List[str]
    highlights: List[str]
    note: str | None = None

@router.post("/api/plan", response_model=PlanResponse)
async def generate_plan(req: PlanRequest):
    messages = [
        {"role": "system", "content": "You are a concise coaching plan generator. Return JSON with keys: summary (string), items (list of strings), score (float)."},
        {"role": "user", "content": f"Generate a plan for: {req.query}. Preferences: {', '.join(req.preferences)}"}
    ]
    result = await call_inference(messages)
    # Persist the request/response for audit
    db = SessionLocal()
    try:
        db_session = Session(query=req.query, result=result)
        db.add(db_session)
        db.commit()
    finally:
        db.close()
    return result

@router.post("/api/insights", response_model=InsightsResponse)
async def generate_insights(req: InsightsRequest):
    messages = [
        {"role": "system", "content": "You are an insights extractor for coaching selections. Return JSON with keys: insights (string), next_actions (list of strings), highlights (list of strings)."},
        {"role": "user", "content": f"Selection: {req.selection}. Context: {req.context}. Provide insights."}
    ]
    result = await call_inference(messages)
    db = SessionLocal()
    try:
        db_session = Session(query=req.selection, result=result)
        db.add(db_session)
        db.commit()
    finally:
        db.close()
    return result
