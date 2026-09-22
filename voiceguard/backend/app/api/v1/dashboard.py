from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import CallSession, Incident, AuditEvent, AnalysisResult
from app.schemas.schemas import DashboardOverview, IncidentResponse
from blockchain.audit_chain import HashChainAuditLogger, GENESIS_HASH

router = APIRouter(prefix="/dashboard", tags=["Security Dashboard"])

audit_logger = HashChainAuditLogger()

@router.get("/overview", response_model=DashboardOverview)
def get_dashboard_overview(db: Session = Depends(get_db)):
    total_calls = db.query(CallSession).count()
    active_calls = db.query(CallSession).filter(CallSession.status.in_(["ACTIVE", "ON_HOLD"])).count()
    total_incidents = db.query(Incident).count()
    
    synthetic_detected = db.query(AnalysisResult).filter(AnalysisResult.deepfake_prob >= 0.65).count()
    
    avg_score_res = db.query(func.avg(CallSession.peak_risk_score)).scalar()
    avg_risk = float(avg_score_res) if avg_score_res is not None else 0.0

    recent_incidents = db.query(Incident).order_by(Incident.created_at.desc()).limit(5).all()

    latest_audit = db.query(AuditEvent).order_by(AuditEvent.event_index.desc()).first()
    head_hash = latest_audit.event_hash if latest_audit else GENESIS_HASH

    return DashboardOverview(
        total_calls_analyzed=total_calls,
        total_incidents_flagged=total_incidents,
        active_calls_count=active_calls,
        synthetic_voices_detected=synthetic_detected,
        avg_risk_score=round(avg_risk, 1),
        recent_incidents=[IncidentResponse.from_orm(inc) for inc in recent_incidents],
        blockchain_hash_head=head_hash
    )
