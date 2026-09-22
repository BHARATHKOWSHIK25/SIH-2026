import uuid
import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import CallSession
from app.schemas.schemas import CallStartRequest, CallStartResponse, CallSessionResponse

router = APIRouter(prefix="/calls", tags=["Call Sessions"])

@router.post("/start", response_model=CallStartResponse)
def start_call_session(req: CallStartRequest, db: Session = Depends(get_db)):
    session_id = f"CALL-{uuid.uuid4().hex[:8].upper()}"
    call = CallSession(
        id=session_id,
        caller_id=req.caller_id,
        callee_id=req.callee_id,
        expected_speaker_id=req.expected_speaker_id,
        status="ACTIVE",
        current_risk_score=0.0,
        current_risk_level="LOW",
        start_time=datetime.datetime.utcnow()
    )
    db.add(call)
    db.commit()
    db.refresh(call)
    return CallStartResponse(
        session_id=call.id,
        caller_id=call.caller_id,
        callee_id=call.callee_id,
        status=call.status,
        start_time=call.start_time
    )

@router.get("", response_model=List[CallSessionResponse])
def list_call_sessions(db: Session = Depends(get_db)):
    return db.query(CallSession).order_by(CallSession.start_time.desc()).all()

@router.get("/{session_id}", response_model=CallSessionResponse)
def get_call_session(session_id: str, db: Session = Depends(get_db)):
    call = db.query(CallSession).filter(CallSession.id == session_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call session not found")
    return call

@router.post("/{session_id}/end", response_model=CallSessionResponse)
def end_call_session(session_id: str, db: Session = Depends(get_db)):
    call = db.query(CallSession).filter(CallSession.id == session_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call session not found")
    
    if call.status in ["ACTIVE", "ON_HOLD"]:
        call.status = "ENDED"
        call.end_time = datetime.datetime.utcnow()
        db.commit()
        db.refresh(call)
    return call
