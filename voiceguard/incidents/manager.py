import uuid
import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import Incident, CallSession
from app.schemas.schemas import DynamicRiskResponse

class IncidentManager:
    """
    Security Incident & Forensic Evidence Management System.
    """

    def create_incident_from_risk(
        self,
        db: Session,
        session_id: str,
        risk_response: DynamicRiskResponse,
        transcript_excerpt: Optional[str] = None
    ) -> Incident:
        # Check if an open incident already exists for this session
        existing = db.query(Incident).filter(
            Incident.session_id == session_id,
            Incident.status.in_(["OPEN", "UNDER_INVESTIGATION"])
        ).first()

        evidence = {
            "risk_score": risk_response.risk_score,
            "risk_level": risk_response.risk_level,
            "confidence": risk_response.confidence,
            "signals": risk_response.signals.dict(),
            "detected_intents": risk_response.detected_intents,
            "risk_indicators": risk_response.risk_indicators,
            "reasons": risk_response.reasons,
            "transcript_excerpt": transcript_excerpt or ""
        }

        if existing:
            # Update existing incident with elevated evidence
            if risk_response.risk_score > existing.risk_score:
                existing.risk_score = risk_response.risk_score
                existing.risk_level = risk_response.risk_level
                existing.evidence_json = evidence
                db.commit()
                db.refresh(existing)
            return existing

        incident_id = f"INC-{uuid.uuid4().hex[:8].upper()}"
        title = f"{risk_response.risk_level} Risk Voice Impersonation Alert"
        description = f"Detected {risk_response.risk_level} risk level voice security event on call session {session_id}."

        incident = Incident(
            id=incident_id,
            session_id=session_id,
            risk_score=risk_response.risk_score,
            risk_level=risk_response.risk_level,
            status="OPEN",
            title=title,
            description=description,
            evidence_json=evidence,
            action_taken=risk_response.recommended_action,
            created_at=datetime.datetime.utcnow()
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident

    def update_incident(
        self,
        db: Session,
        incident_id: str,
        status: Optional[str] = None,
        action_taken: Optional[str] = None
    ) -> Optional[Incident]:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            return None

        if status:
            incident.status = status
            if status in ["RESOLVED", "FALSE_POSITIVE"]:
                incident.resolved_at = datetime.datetime.utcnow()
        if action_taken:
            incident.action_taken = action_taken

        db.commit()
        db.refresh(incident)
        return incident
