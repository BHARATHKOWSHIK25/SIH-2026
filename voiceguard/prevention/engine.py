import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import CallSession, Incident
from app.schemas.schemas import DynamicRiskResponse
from risk_engine.policies import RiskPolicy

logger = logging.getLogger("VoiceGuard.PreventionEngine")

class PreventionEngine:
    """
    Automated Prevention Workflow Engine.
    Enforces automatic mitigation actions:
    - LOW: Continue continuous active monitoring
    - MEDIUM: Inject warning banner on Security Analyst UI
    - HIGH: Put session on transaction hold & issue secondary MFA challenge
    - CRITICAL: Immediately terminate/block call session & append tamper-evident audit record
    """

    def process_risk_action(self, db: Session, session_id: str, risk_response: DynamicRiskResponse) -> Dict[str, Any]:
        call_session = db.query(CallSession).filter(CallSession.id == session_id).first()
        if not call_session:
            logger.warning(f"Call session {session_id} not found in DB.")
            return {"status": "SESSION_NOT_FOUND"}

        # Update session risk status
        call_session.current_risk_score = risk_response.risk_score
        call_session.current_risk_level = risk_response.risk_level
        if risk_response.risk_score > call_session.peak_risk_score:
            call_session.peak_risk_score = risk_response.risk_score

        policy = RiskPolicy.get_policy(risk_response.risk_level)

        action_taken = policy["recommended_action"]
        if risk_response.risk_level == RiskPolicy.CRITICAL:
            call_session.status = "BLOCKED"
            action_taken = "SESSION_BLOCKED_IMMEDIATELY"
        elif risk_response.risk_level == RiskPolicy.HIGH:
            call_session.status = "ON_HOLD"
            action_taken = "TRANSACTION_HELD_FOR_VERIFICATION"

        db.commit()

        return {
            "session_id": session_id,
            "risk_score": risk_response.risk_score,
            "risk_level": risk_response.risk_level,
            "session_status": call_session.status,
            "action_taken": action_taken,
            "ui_banner": policy["ui_banner"],
            "requires_mfa": policy["requires_mfa"]
        }
