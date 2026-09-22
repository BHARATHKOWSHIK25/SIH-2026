from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Incident
from app.schemas.schemas import IncidentResponse, IncidentUpdate
from incidents.manager import IncidentManager
from blockchain.audit_chain import HashChainAuditLogger

router = APIRouter(prefix="/incidents", tags=["Incidents & Forensics"])

manager = IncidentManager()
audit_logger = HashChainAuditLogger()

@router.get("", response_model=List[IncidentResponse])
def list_incidents(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    return query.order_by(Incident.created_at.desc()).all()

@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident_status(
    incident_id: str,
    update: IncidentUpdate,
    db: Session = Depends(get_db)
):
    updated = manager.update_incident(
        db=db,
        incident_id=incident_id,
        status=update.status,
        action_taken=update.action_taken
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Incident not found")

    audit_logger.log_event(
        db=db,
        event_type="INCIDENT_STATUS_UPDATED",
        payload={
            "incident_id": incident_id,
            "new_status": updated.status,
            "action_taken": updated.action_taken
        },
        session_id=updated.session_id
    )

    return updated
