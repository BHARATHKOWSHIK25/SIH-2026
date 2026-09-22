import re
from typing import Dict, List, Tuple, Any

class SocialEngineeringDetector:
    """
    Social Engineering & Impersonation Attack Intent Detector.
    Scans conversation transcripts for high-risk psychological manipulation tactics:
    - Artificial Urgency
    - Authority & Executive Impersonation
    - Secrecy & Isolation Pressure
    - Unauthorized Financial Transaction Requests
    - Credential & OTP Harvesting
    """

    PATTERNS: Dict[str, Dict[str, Any]] = {
        "URGENCY": {
            "weight": 25.0,
            "keywords": [
                r"\b(immediately|right now|urgent|urgently|emergency|asap|don't delay|within 5 minutes|turant|jaldi)\b"
            ],
            "description": "Artificial urgency pressure detected"
        },
        "AUTHORITY": {
            "weight": 25.0,
            "keywords": [
                r"\b(ceo|cfo|chief executive|bank manager|rbi|cyber cell|police|income tax|managing director|head office|auditor)\b"
            ],
            "description": "High-authority executive or regulator impersonation detected"
        },
        "SECRECY": {
            "weight": 20.0,
            "keywords": [
                r"\b(don't tell anyone|do not tell anyone|keep this confidential|between us|off the record|don't verify|skip protocol|secret|gupt)\b"
            ],
            "description": "Secrecy / isolation pressure detected"
        },
        "FINANCIAL_TRANSACTION": {
            "weight": 30.0,
            "keywords": [
                r"\b(transfer money|wire transfer|neft|rtgs|upi|send funds|bank account|vendor payment|transfer rupees|pay now)\b"
            ],
            "description": "High-value financial transfer request detected"
        },
        "CREDENTIAL_HARVESTING": {
            "weight": 35.0,
            "keywords": [
                r"\b(otp|pin|password|cvv|verification code|one time password|login details|secret key)\b"
            ],
            "description": "Sensitive credential / OTP harvesting attempt detected"
        }
    }

    def analyze_transcript(self, transcript: str) -> Tuple[float, List[str], List[str], List[str]]:
        """
        Analyze transcript string for social engineering markers.
        Returns:
        - social_eng_score: float [0..100]
        - detected_intents: List[str]
        - risk_indicators: List[str]
        - reasons: List[str]
        """
        if not transcript or len(transcript.strip()) == 0:
            return 0.0, [], [], []

        text_lower = transcript.lower()
        score = 0.0
        detected_intents = []
        risk_indicators = []
        reasons = []

        for category, config in self.PATTERNS.items():
            matched_in_category = False
            for pattern in config["keywords"]:
                matches = re.findall(pattern, text_lower)
                if matches:
                    matched_terms = list(set([m[0] if isinstance(m, tuple) else m for m in matches]))
                    risk_indicators.extend(matched_terms)
                    matched_in_category = True
            
            if matched_in_category:
                score += config["weight"]
                detected_intents.append(category)
                reasons.append(config["description"])

        final_score = float(min(100.0, score))
        return final_score, detected_intents, risk_indicators, reasons
