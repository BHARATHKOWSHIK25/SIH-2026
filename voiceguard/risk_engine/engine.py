import logging
import numpy as np
from typing import Dict, Any, List, Tuple
from app.config import settings
from app.schemas.schemas import SignalScores, DynamicRiskResponse
from risk_engine.policies import RiskPolicy

logger = logging.getLogger("VoiceGuard.RiskEngine")

class DynamicRiskEngine:
    """
    Dynamic Impersonation Risk Calculation & Multi-Signal Evidence Fusion Engine.
    Fuses deepfake probability, speaker verification mismatch, acoustic anomalies,
    transcription intent / social engineering scores, and transaction context.
    Strictly enforces the Multi-Signal Evidence Rule.
    """

    def __init__(self):
        self.w_deepfake = settings.WEIGHT_DEEPFAKE           # 0.30
        self.w_speaker = settings.WEIGHT_SPEAKER_MISMATCH    # 0.25
        self.w_social_eng = settings.WEIGHT_SOCIAL_ENG       # 0.25
        self.w_tx = settings.WEIGHT_TRANSACTION_RISK         # 0.15
        self.w_context = settings.WEIGHT_CONTEXT_RISK        # 0.05

    def calculate_risk(
        self,
        signals: SignalScores,
        detected_intents: List[str] = [],
        risk_indicators: List[str] = [],
        previous_reasons: List[str] = []
    ) -> DynamicRiskResponse:
        """
        Calculate overall dynamic impersonation risk score and risk level.
        Enforces Multi-Signal Evidence Rule.
        """
        deepfake_risk = signals.deepfake_prob * 100.0
        speaker_mismatch_risk = (1.0 - signals.speaker_similarity) * 100.0
        social_eng_risk = signals.social_engineering_score
        acoustic_prosody_risk = ((signals.acoustic_anomaly + signals.prosody_anomaly) / 2.0) * 100.0
        tx_risk = signals.transaction_risk
        context_risk = signals.context_risk

        # Weighted Linear Fusion
        raw_score = (
            (self.w_deepfake * deepfake_risk) +
            (self.w_speaker * speaker_mismatch_risk) +
            (self.w_social_eng * social_eng_risk) +
            (0.10 * acoustic_prosody_risk) +
            (self.w_tx * tx_risk) +
            (self.w_context * context_risk)
        )

        calculated_score = float(np.clip(raw_score, 0.0, 100.0))

        # --- MULTI-SIGNAL EVIDENCE AGGREGATION RULE ENFORCEMENT ---
        # Rule: No single weak signal shall produce a CRITICAL decision.
        # CRITICAL (>85.0) requires at least TWO strong independent signals.
        strong_signals_count = 0
        reasons = list(previous_reasons)

        if signals.deepfake_prob >= 0.65:
            strong_signals_count += 1
            reasons.append(f"Synthetic voice detected with high confidence ({int(signals.deepfake_prob*100)}%).")

        if signals.speaker_similarity <= 0.40:
            strong_signals_count += 1
            reasons.append(f"Speaker identity mismatch detected (Similarity: {int(signals.speaker_similarity*100)}%).")

        if signals.social_engineering_score >= 50.0:
            strong_signals_count += 1
            reasons.append(f"High-risk social engineering keywords detected ({int(signals.social_engineering_score)} pts).")

        if signals.acoustic_anomaly >= 0.60 or signals.prosody_anomaly >= 0.60:
            strong_signals_count += 1
            reasons.append("Significant physical acoustic/prosodic vocal anomaly detected.")

        if signals.transaction_risk >= 70.0:
            strong_signals_count += 1
            reasons.append("High-value unauthorized financial transaction intent.")

        # Cap score at 84.0 (HIGH) if strong_signals_count < 2
        if calculated_score >= settings.THRESHOLD_CRITICAL and strong_signals_count < 2:
            logger.info("Risk score capped at 84.0 (HIGH) due to Multi-Signal Evidence Rule (requires >= 2 strong signals for CRITICAL).")
            final_score = 84.0
        else:
            final_score = calculated_score

        # Determine Risk Level
        if final_score >= settings.THRESHOLD_CRITICAL:
            risk_level = RiskPolicy.CRITICAL
        elif final_score >= settings.THRESHOLD_HIGH:
            risk_level = RiskPolicy.HIGH
        elif final_score >= settings.THRESHOLD_MEDIUM:
            risk_level = RiskPolicy.MEDIUM
        else:
            risk_level = RiskPolicy.LOW

        policy = RiskPolicy.get_policy(risk_level)

        # Confidence calculation
        confidence = float(np.clip(0.80 + (strong_signals_count * 0.05), 0.75, 0.98))

        return DynamicRiskResponse(
            risk_score=round(final_score, 1),
            risk_level=risk_level,
            confidence=round(confidence, 2),
            model_status="PARTIAL_AI",
            signals=signals,
            detected_intents=detected_intents,
            risk_indicators=risk_indicators,
            reasons=list(set(reasons)),
            recommended_action=policy["recommended_action"]
        )
