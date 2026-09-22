import hashlib
import json
import datetime
from typing import Dict, Any, Tuple, Optional, List
from sqlalchemy.orm import Session
from app.models.models import AuditEvent
from app.schemas.schemas import AuditVerifyResponse

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

class HashChainAuditLogger:
    """
    Cryptographic SHA-256 Hash-Chain Audit Trail Engine.
    Provides tamper-evident audit logging for VoiceGuard security decisions.
    Every event contains the cryptographic SHA-256 hash of the preceding event,
    forming an immutable block chain.
    """

    def compute_event_hash(
        self,
        previous_hash: str,
        timestamp_str: str,
        event_type: str,
        payload_json: Dict[str, Any]
    ) -> str:
        """
        Compute canonical SHA-256 hash of an audit event.
        """
        canonical_payload = json.dumps(payload_json, sort_keys=True)
        payload_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
        
        raw_string = f"{previous_hash}|{timestamp_str}|{event_type}|{payload_hash}"
        return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()

    def log_event(
        self,
        db: Session,
        event_type: str,
        payload: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> AuditEvent:
        """
        Append a new audit event to the hash chain in database.
        """
        latest = db.query(AuditEvent).order_by(AuditEvent.event_index.desc()).first()

        if latest is None:
            previous_hash = GENESIS_HASH
            next_index = 1
        else:
            previous_hash = latest.event_hash
            next_index = latest.event_index + 1

        now = datetime.datetime.utcnow()
        timestamp_str = now.isoformat()

        event_hash = self.compute_event_hash(
            previous_hash=previous_hash,
            timestamp_str=timestamp_str,
            event_type=event_type,
            payload_json=payload
        )

        event = AuditEvent(
            event_index=next_index,
            previous_hash=previous_hash,
            event_hash=event_hash,
            event_type=event_type,
            session_id=session_id,
            payload_json=payload,
            timestamp=now
        )

        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def verify_chain_integrity(self, db: Session) -> AuditVerifyResponse:
        """
        Verify complete audit chain integrity from Genesis (Index 1) to Latest.
        Detects any data tampering or missing links.
        """
        events = db.query(AuditEvent).order_by(AuditEvent.event_index.asc()).all()
        if not events:
            return AuditVerifyResponse(
                total_events=0,
                is_valid=True,
                broken_at_index=None,
                message="Audit trail is empty (Genesis state)."
            )

        expected_prev_hash = GENESIS_HASH

        for idx, event in enumerate(events):
            # Check 1: Previous hash matches expected chain hash
            if event.previous_hash != expected_prev_hash:
                return AuditVerifyResponse(
                    total_events=len(events),
                    is_valid=False,
                    broken_at_index=event.event_index,
                    message=f"Hash-chain broken at index {event.event_index}: Previous hash mismatch!"
                )

            # Check 2: Re-calculate hash of current event payload
            recalculated_hash = self.compute_event_hash(
                previous_hash=event.previous_hash,
                timestamp_str=event.timestamp.isoformat(),
                event_type=event.event_type,
                payload_json=event.payload_json
            )

            if recalculated_hash != event.event_hash:
                return AuditVerifyResponse(
                    total_events=len(events),
                    is_valid=False,
                    broken_at_index=event.event_index,
                    message=f"Hash-chain broken at index {event.event_index}: Event payload hash altered!"
                )

            expected_prev_hash = event.event_hash

        return AuditVerifyResponse(
            total_events=len(events),
            is_valid=True,
            broken_at_index=None,
            message="Audit chain verification PASSED. All records are cryptographically intact."
        )
