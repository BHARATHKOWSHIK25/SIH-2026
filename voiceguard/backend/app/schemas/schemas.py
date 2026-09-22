from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# User & Auth Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: str = "analyst"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


# Voice Profile Schemas
class VoiceProfileCreate(BaseModel):
    speaker_id: str
    speaker_name: str

class VoiceProfileResponse(BaseModel):
    id: int
    speaker_id: str
    speaker_name: str
    audio_sample_path: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class SpeakerVerifyRequest(BaseModel):
    speaker_id: str

class SpeakerVerifyResponse(BaseModel):
    speaker_id: str
    similarity_score: float
    is_match: bool
    confidence: float


# Call Session Schemas
class CallStartRequest(BaseModel):
    caller_id: str
    callee_id: str
    expected_speaker_id: Optional[str] = None

class CallStartResponse(BaseModel):
    session_id: str
    caller_id: str
    callee_id: str
    status: str
    start_time: datetime

class CallSessionResponse(BaseModel):
    id: str
    caller_id: str
    callee_id: str
    expected_speaker_id: Optional[str]
    status: str
    current_risk_score: float
    current_risk_level: str
    peak_risk_score: float
    start_time: datetime
    end_time: Optional[datetime] = None
    transcript_summary: Optional[str] = None

    model_config = {"from_attributes": True}


# Analysis & Risk Schemas
class SignalScores(BaseModel):
    deepfake_prob: float = Field(..., ge=0.0, le=1.0, description="Synthetic voice probability")
    speaker_similarity: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity with target voice profile")
    acoustic_anomaly: float = Field(..., ge=0.0, le=1.0, description="Spectral/harmonic anomaly score")
    prosody_anomaly: float = Field(..., ge=0.0, le=1.0, description="Pitch & rhythm stability anomaly score")
    social_engineering_score: float = Field(..., ge=0.0, le=100.0, description="Urgency/authority/credential risk score")
    transaction_risk: float = Field(0.0, ge=0.0, le=100.0)
    context_risk: float = Field(0.0, ge=0.0, le=100.0)

class DynamicRiskResponse(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=100.0)
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    confidence: float
    model_status: str = "PARTIAL_AI" # LIVE_AI, PARTIAL_AI, DEMO_SIMULATION, MODEL_UNAVAILABLE
    signals: SignalScores
    detected_intents: List[str] = []
    risk_indicators: List[str] = []
    reasons: List[str] = []
    recommended_action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AudioAnalysisResponse(BaseModel):
    segment_id: int
    chunk_index: int
    transcript: str
    language: str
    risk: DynamicRiskResponse


# WebSocket Message Schemas
class WSStreamMessage(BaseModel):
    event: str # audio_chunk, ping, end_call
    chunk_index: Optional[int] = 0
    audio_base64: Optional[str] = None

class WSRiskUpdate(BaseModel):
    event: str = "risk_update"
    session_id: str
    chunk_index: int
    transcript: str
    risk_score: float
    risk_level: str
    confidence: float
    signals: SignalScores
    recommended_action: str
    timestamp: str


# Incident Schemas
class IncidentCreate(BaseModel):
    session_id: str
    risk_score: float
    risk_level: str
    title: str
    description: Optional[str] = None
    evidence_json: Optional[Dict[str, Any]] = None

class IncidentUpdate(BaseModel):
    status: Optional[str] = None # OPEN, UNDER_INVESTIGATION, RESOLVED, FALSE_POSITIVE
    action_taken: Optional[str] = None

class IncidentResponse(BaseModel):
    id: str
    session_id: str
    risk_score: float
    risk_level: str
    status: str
    title: str
    description: Optional[str] = None
    evidence_json: Optional[Dict[str, Any]] = None
    action_taken: str
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# Verification Schemas
class VerificationCreate(BaseModel):
    session_id: str
    verification_type: str = "OTP_CHALLENGE"

class VerificationResolve(BaseModel):
    status: str # PASSED, FAILED
    challenge_code: Optional[str] = None

class VerificationResponse(BaseModel):
    id: str
    session_id: str
    verification_type: str
    status: str
    challenge_code: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# Audit Schemas
class AuditEventResponse(BaseModel):
    event_index: int
    previous_hash: str
    event_hash: str
    event_type: str
    session_id: Optional[str] = None
    payload_json: Dict[str, Any]
    timestamp: datetime

    class Config:
        from_attributes = True

class AuditVerifyResponse(BaseModel):
    total_events: int
    is_valid: bool
    broken_at_index: Optional[int] = None
    message: str


# Dashboard Schemas
class DashboardOverview(BaseModel):
    total_calls_analyzed: int
    total_incidents_flagged: int
    active_calls_count: int
    synthetic_voices_detected: int
    avg_risk_score: float
    recent_incidents: List[IncidentResponse]
    blockchain_hash_head: str
