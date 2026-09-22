import numpy as np
from typing import Dict, Any, Tuple

class AuthenticityFusionEngine:
    """
    Voice Authenticity Fusion Engine.
    Fuses multiple low-level audio signals (Deepfake score, Speaker match, Acoustic & Prosodic anomalies)
    into a unified Voice Authenticity Risk Score [0..100].
    """

    def __init__(
        self,
        weight_deepfake: float = 0.50,
        weight_speaker_mismatch: float = 0.30,
        weight_acoustic: float = 0.10,
        weight_prosody: float = 0.10
    ):
        self.w_deepfake = weight_deepfake
        self.w_speaker = weight_speaker_mismatch
        self.w_acoustic = weight_acoustic
        self.w_prosody = weight_prosody

    def compute_voice_authenticity_risk(
        self,
        deepfake_prob: float,
        speaker_similarity: float,
        acoustic_anomaly: float,
        prosody_anomaly: float
    ) -> Tuple[float, float, str]:
        """
        Compute voice authenticity risk score [0..100], confidence, and classification.
        """
        # Speaker mismatch score = (1.0 - speaker_similarity)
        speaker_mismatch = 1.0 - speaker_similarity

        raw_risk = (
            (self.w_deepfake * deepfake_prob) +
            (self.w_speaker * speaker_mismatch) +
            (self.w_acoustic * acoustic_anomaly) +
            (self.w_prosody * prosody_anomaly)
        )

        risk_score = float(np.clip(raw_risk * 100.0, 0.0, 100.0))

        # Overall confidence estimation
        confidence = float(np.clip(0.85 + (abs(deepfake_prob - 0.5) * 0.2), 0.70, 0.98))

        if risk_score >= 70.0:
            status = "HIGH_SYNTHETIC_RISK"
        elif risk_score >= 40.0:
            status = "SUSPICIOUS_VOICE"
        else:
            status = "AUTHENTIC_VOICE"

        return risk_score, confidence, status
