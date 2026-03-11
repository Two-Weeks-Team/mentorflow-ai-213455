import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from routes import router

app = FastAPI()


@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health", response_model=dict)
async def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <html>
    <head>
        <title>MentorFlow AI</title>
        <style>
            body { background-color: #121212; color: #e0e0e0; font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 2rem; }
            h1 { color: #4A90E2; }
            a { color: #FF6B6B; text-decoration: none; }
            .container { max-width: 800px; margin: auto; }
            .endpoint { margin-bottom: 1rem; }
            .footer { margin-top: 2rem; font-size: 0.9rem; color: #888; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MentorFlow AI</h1>
            <p>Privacy‑first AI coaching that delivers instant, structured guidance—no subscription, no guesswork.</p>
            <h2>Available API Endpoints</h2>
            <div class="endpoint"><strong>GET</strong> /health – health check</div>
            <div class="endpoint"><strong>POST</strong> /api/plan – generate a coaching plan</div>
            <div class="endpoint"><strong>POST</strong> /api/insights – get insights for a selected pathway</div>
            <h2>Tech Stack</h2>
            <ul>
                <li>Next.js 15.5.12 (React 19.0.0, TypeScript 5.7.3, Tailwind CSS 3.4.17)</li>
                <li>FastAPI 0.115.0</li>
                <li>PostgreSQL via SQLAlchemy 2.0.35</li>
                <li>DigitalOcean Serverless Inference (openai-gpt-oss-120b)</li>
            </ul>
            <p>Explore API docs: <a href="/docs">/docs</a> | <a href="/redoc">/redoc</a></p>
            <div class="footer">&copy; 2026 MentorFlow AI. All rights reserved.</div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
