import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="analyst") # admin, analyst, operator
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    voice_profiles = relationship("VoiceProfile", back_populates="owner")


class VoiceProfile(Base):
    __tablename__ = "voice_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    speaker_name = Column(String(255), index=True, nullable=False)
    speaker_id = Column(String(100), unique=True, index=True, nullable=False)
    embedding_json = Column(Text, nullable=False)  # JSON representation of 192-dim vector
    audio_sample_path = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="voice_profiles")


class CallSession(Base):
    __tablename__ = "call_sessions"

    id = Column(String(100), primary_key=True, index=True) # UUID
    caller_id = Column(String(100), nullable=False, index=True)
    callee_id = Column(String(100), nullable=False, index=True)
    expected_speaker_id = Column(String(100), ForeignKey("voice_profiles.speaker_id"), nullable=True)
    status = Column(String(50), default="ACTIVE") # ACTIVE, ENDED, BLOCKED, ON_HOLD
    current_risk_score = Column(Float, default=0.0)
    current_risk_level = Column(String(20), default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    peak_risk_score = Column(Float, default=0.0)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    transcript_summary = Column(Text, nullable=True)

    segments = relationship("AudioSegment", back_populates="session", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="session", cascade="all, delete-orphan")
    verifications = relationship("VerificationRequest", back_populates="session", cascade="all, delete-orphan")


class AudioSegment(Base):
    __tablename__ = "audio_segments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), ForeignKey("call_sessions.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    duration_sec = Column(Float, nullable=False)
    audio_path = Column(String(500), nullable=True)
    transcript = Column(Text, nullable=True)
    language = Column(String(10), default="en")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("CallSession", back_populates="segments")
    analysis = relationship("AnalysisResult", back_populates="segment", uselist=False, cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, ForeignKey("audio_segments.id"), nullable=False, unique=True, index=True)
    deepfake_prob = Column(Float, default=0.0)          # 0..1
    speaker_similarity = Column(Float, default=1.0)     # 0..1
    acoustic_anomaly = Column(Float, default=0.0)       # 0..1
    prosody_anomaly = Column(Float, default=0.0)        # 0..1
    social_engineering_score = Column(Float, default=0.0)# 0..100
    detected_intents = Column(JSON, default=list)        # list of strings
    risk_score = Column(Float, default=0.0)              # 0..100
    risk_level = Column(String(20), default="LOW")      # LOW, MEDIUM, HIGH, CRITICAL
    confidence = Column(Float, default=0.9)              # 0..1
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    segment = relationship("AudioSegment", back_populates="analysis")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String(100), primary_key=True, index=True) # INC-XXXX
    session_id = Column(String(100), ForeignKey("call_sessions.id"), nullable=False, index=True)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    status = Column(String(50), default="OPEN") # OPEN, UNDER_INVESTIGATION, RESOLVED, FALSE_POSITIVE
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    evidence_json = Column(JSON, nullable=True)
    action_taken = Column(String(100), default="ALERT_GENERATED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    session = relationship("CallSession", back_populates="incidents")


class VerificationRequest(Base):
    __tablename__ = "verification_requests"

    id = Column(String(100), primary_key=True, index=True) # VRF-XXXX
    session_id = Column(String(100), ForeignKey("call_sessions.id"), nullable=False, index=True)
    verification_type = Column(String(50), default="OTP_CHALLENGE") # CALLBACK, OTP_CHALLENGE, SUPERVISOR_OVERRIDE
    status = Column(String(50), default="PENDING") # PENDING, PASSED, FAILED, EXPIRED
    challenge_code = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    session = relationship("CallSession", back_populates="verifications")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    event_index = Column(Integer, primary_key=True, index=True)
    previous_hash = Column(String(64), nullable=False)
    event_hash = Column(String(64), nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    session_id = Column(String(100), nullable=True, index=True)
    payload_json = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
