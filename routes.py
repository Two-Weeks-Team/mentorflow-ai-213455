from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, List
from models import Session, SessionLocal
from ai_service import call_inference

router = APIRouter()

class PlanRequest(BaseModel):
    query: str
    preferences: Any = Field(default_factory=list)

class PlanResponse(BaseModel):
    summary: str
    items: list[dict[str, object]]
    score: float
    note: str | None = None

class InsightsRequest(BaseModel):
    selection: str
    context: str

class InsightsResponse(BaseModel):
    insights: list[str]
    next_actions: List[str]
    highlights: List[str]
    note: str | None = None

@router.post("/plan", response_model=PlanResponse)
async def generate_plan(req: PlanRequest):
    if isinstance(req.preferences, list):
        preference_items = [str(entry) for entry in req.preferences if str(entry).strip()]
    elif isinstance(req.preferences, str) and req.preferences.strip():
        preference_items = [part.strip() for part in req.preferences.split(",") if part.strip()]
    else:
        preference_items = []
    messages = [
        {"role": "system", "content": "You are a concise coaching plan generator. Return JSON with keys: summary (string), items (list of objects with title, detail, score), score (float)."},
        {"role": "user", "content": f"Generate a plan for: {req.query}. Preferences: {', '.join(preference_items)}"}
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

@router.post("/insights", response_model=InsightsResponse)
async def generate_insights(req: InsightsRequest):
    messages = [
        {"role": "system", "content": "You are an insights extractor for coaching selections. Return JSON with keys: insights (list of strings), next_actions (list of strings), highlights (list of strings)."},
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
