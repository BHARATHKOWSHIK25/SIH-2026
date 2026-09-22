from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import AuditEvent
from app.schemas.schemas import AuditEventResponse, AuditVerifyResponse
from blockchain.audit_chain import HashChainAuditLogger

router = APIRouter(prefix="/audit", tags=["Blockchain & Audit Trail"])

audit_logger = HashChainAuditLogger()

@router.get("/events", response_model=List[AuditEventResponse])
def get_audit_trail_events(db: Session = Depends(get_db)):
    return db.query(AuditEvent).order_by(AuditEvent.event_index.asc()).all()

@router.post("/verify", response_model=AuditVerifyResponse)
def verify_audit_chain_integrity(db: Session = Depends(get_db)):
    return audit_logger.verify_chain_integrity(db)
