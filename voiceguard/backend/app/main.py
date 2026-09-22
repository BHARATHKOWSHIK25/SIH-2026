from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.calls import router as calls_router
from app.api.v1.voice import router as voice_router
from app.api.v1.speaker import router as speaker_router
from app.api.v1.incidents import router as incidents_router
from app.api.v1.audit import router as audit_router
from app.api.v1.dashboard import router as dashboard_router
from app.websocket.stream_handler import router as ws_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="VoiceGuard AI — Real-Time Detection & Prevention of Voice Impersonation Attacks (SIH26104)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for React frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for prototype development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database schema on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Mount API Routers under /api/v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(calls_router, prefix="/api/v1")
app.include_router(voice_router, prefix="/api/v1")
app.include_router(speaker_router, prefix="/api/v1")
app.include_router(incidents_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(ws_router)

@app.get("/")
def root_status():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "problem_statement": "SIH26104",
        "docs": "/docs",
        "realtime_ws": "/ws/calls/{session_id}/stream"
    }
