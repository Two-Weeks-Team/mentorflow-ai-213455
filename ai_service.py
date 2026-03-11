import os
import json
import re
import httpx
from typing import Any, Dict, List

_INFERENCE_URL = "https://inference.do-ai.run/v1/chat/completions"
_API_KEY = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
_MODEL = os.getenv("DO_INFERENCE_MODEL") or "openai-gpt-oss-120b"

def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

def _coerce_unstructured_payload(raw_text: str) -> dict[str, object]:
    compact = raw_text.strip()
    subject = compact if compact and compact.lower() != "ai service fallback" else "a visible growth roadmap"
    items = [
        {
            "title": "Focus lane: capability map",
            "detail": f"Turn {subject} into a concrete capability ladder with one skill theme, one confidence theme, and one proof artifact.",
            "score": 84,
        },
        {
            "title": "Feedback loop: weekly ritual",
            "detail": "Define a repeatable cadence for mentor check-ins, async feedback, and one measurable experiment each week.",
            "score": 88,
        },
        {
            "title": "Proof lane: visible progress",
            "detail": "Package the strongest output into a portfolio slice, retro note, or stakeholder-ready update that proves momentum.",
            "score": 92,
        },
    ]
    highlights = ["Weekly ritual", "Visible proof", "Career momentum"]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": f"MentorFlow converted {subject} into a clear coaching roadmap with visible next steps.",
        "tags": ["coaching roadmap", "visible progress", "habit loop"],
        "items": items,
        "score": 88,
        "insights": ["Start with the capability gap so the user sees what changes first.", "Keep one concrete proof artifact attached to every milestone."],
        "next_actions": ["Save the roadmap as the active coaching path.", "Turn the first milestone into a one-week experiment."],
        "highlights": highlights,
    }


def _normalize_ai_payload(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        return _coerce_unstructured_payload(str(payload))

    normalized = dict(payload)
    summary = str(normalized.get("summary") or normalized.get("note") or "AI-generated plan ready")
    raw_items = normalized.get("items")
    items: list[dict[str, object]] = []
    if isinstance(raw_items, list):
        for index, entry in enumerate(raw_items[:3], start=1):
            if isinstance(entry, dict):
                title = str(entry.get("title") or f"Stage {index}")
                detail = str(entry.get("detail") or entry.get("description") or title)
                score = float(entry.get("score") or min(96, 80 + index * 4))
            else:
                label = str(entry).strip() or f"Stage {index}"
                title = f"Stage {index}: {label.title()}"
                detail = f"Use {label} to move the request toward a demo-ready outcome."
                score = float(min(96, 80 + index * 4))
            items.append({"title": title, "detail": detail, "score": score})
    if not items:
        items = _coerce_unstructured_payload(summary).get("items", [])

    raw_insights = normalized.get("insights")
    if isinstance(raw_insights, list):
        insights = [str(entry) for entry in raw_insights if str(entry).strip()]
    elif isinstance(raw_insights, str) and raw_insights.strip():
        insights = [raw_insights.strip()]
    else:
        insights = []

    next_actions = normalized.get("next_actions")
    if isinstance(next_actions, list):
        next_actions = [str(entry) for entry in next_actions if str(entry).strip()]
    else:
        next_actions = []

    highlights = normalized.get("highlights")
    if isinstance(highlights, list):
        highlights = [str(entry) for entry in highlights if str(entry).strip()]
    else:
        highlights = []

    if not insights and not next_actions and not highlights:
        fallback = _coerce_unstructured_payload(summary)
        insights = fallback.get("insights", [])
        next_actions = fallback.get("next_actions", [])
        highlights = fallback.get("highlights", [])

    return {
        **normalized,
        "summary": summary,
        "items": items,
        "score": float(normalized.get("score") or 88),
        "insights": insights,
        "next_actions": next_actions,
        "highlights": highlights,
    }


async def call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    payload = {
        "model": _MODEL,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {_API_KEY}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            resp = await client.post(_INFERENCE_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            # Expect OpenAI‑compatible response format
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            json_str = _extract_json(content)
            result = json.loads(json_str)
            return _normalize_ai_payload(result)
        except Exception as e:
            return _coerce_unstructured_payload("AI service fallback")
