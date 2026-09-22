import uuid
import random
import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import VerificationRequest, CallSession

class VerificationEngine:
    """
    Secondary Out-of-Band Verification Engine.
    Manages MFA step-up verification requests (OTP, Out-of-band Callback, Supervisor Over-ride).
    """

    def create_verification_challenge(
        self,
        db: Session,
        session_id: str,
        verification_type: str = "OTP_CHALLENGE"
    ) -> VerificationRequest:
        verification_id = f"VRF-{uuid.uuid4().hex[:8].upper()}"
        code = f"{random.randint(100000, 999999)}"

        vrf = VerificationRequest(
            id=verification_id,
            session_id=session_id,
            verification_type=verification_type,
            status="PENDING",
            challenge_code=code,
            created_at=datetime.datetime.utcnow()
        )
        db.add(vrf)
        db.commit()
        db.refresh(vrf)
        return vrf

    def resolve_verification(
        self,
        db: Session,
        verification_id: str,
        provided_code: str
    ) -> Tuple[bool, str]:
        vrf = db.query(VerificationRequest).filter(VerificationRequest.id == verification_id).first()
        if not vrf:
            return False, "VERIFICATION_NOT_FOUND"

        if vrf.status != "PENDING":
            return False, f"VERIFICATION_ALREADY_{vrf.status}"

        if vrf.challenge_code and provided_code != vrf.challenge_code:
            vrf.status = "FAILED"
            vrf.resolved_at = datetime.datetime.utcnow()
            db.commit()
            return False, "INVALID_CHALLENGE_CODE"

        vrf.status = "PASSED"
        vrf.resolved_at = datetime.datetime.utcnow()

        # Update call session back to ACTIVE if held
        call_session = db.query(CallSession).filter(CallSession.id == vrf.session_id).first()
        if call_session and call_session.status == "ON_HOLD":
            call_session.status = "ACTIVE"

        db.commit()
        return True, "VERIFICATION_SUCCESSFUL"
