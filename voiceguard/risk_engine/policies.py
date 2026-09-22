from typing import Dict, Any

class RiskPolicy:
    """
    Policy enforcement rules based on Dynamic Impersonation Risk Tiers.
    """

    LOW = "LOW"             # Risk Score < 30
    MEDIUM = "MEDIUM"       # Risk Score 30 - 50
    HIGH = "HIGH"           # Risk Score 51 - 84
    CRITICAL = "CRITICAL"   # Risk Score >= 85

    ACTIONS = {
        LOW: {
            "recommended_action": "CONTINUE_MONITORING",
            "ui_banner": None,
            "requires_mfa": False,
            "block_transaction": False,
            "create_incident": False
        },
        MEDIUM: {
            "recommended_action": "WARN_OPERATOR",
            "ui_banner": "WARNING: Potential acoustic anomaly or unverified speaker identity.",
            "requires_mfa": False,
            "block_transaction": False,
            "create_incident": False
        },
        HIGH: {
            "recommended_action": "HOLD_TRANSACTION_AND_VERIFY",
            "ui_banner": "HIGH RISK: Suspected synthetic voice or social engineering attack. Secondary verification required.",
            "requires_mfa": True,
            "block_transaction": True,
            "create_incident": True
        },
        CRITICAL: {
            "recommended_action": "BLOCK_SESSION_IMMEDIATELY",
            "ui_banner": "CRITICAL RISK DETECTED: Impersonation attack in progress! Call blocked, incident logged to blockchain.",
            "requires_mfa": True,
            "block_transaction": True,
            "create_incident": True
        }
    }

    @classmethod
    def get_policy(cls, risk_level: str) -> Dict[str, Any]:
        return cls.ACTIONS.get(risk_level, cls.ACTIONS[cls.LOW])
