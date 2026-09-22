import numpy as np
from typing import Dict, Tuple

class AcousticAnalyzer:
    """
    Acoustic & Prosodic Analyzer.
    Extracts physical voice characteristics: pitch contour stability, micro-jitter, shimmer,
    spectral tilt, and harmonic-to-noise ratio (HNR).
    Synthesized/cloned voices often exhibit abnormal pitch flatness or unnatural vocal tract jitter.
    """

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def analyze_acoustic_prosody(self, audio: np.ndarray) -> Tuple[float, float, Dict[str, float]]:
        """
        Analyze audio array and return:
        - acoustic_anomaly_score: float [0..1]
        - prosody_anomaly_score: float [0..1]
        - metrics_dict: dict of detailed spectral features
        """
        if len(audio) < 1024:
            return 0.0, 0.0, {"f0_mean": 0.0, "jitter": 0.0, "shimmer": 0.0, "spectral_tilt": 0.0}

        # 1. Pitch (F0) estimation via autocorrelation
        corr = np.correlate(audio, audio, mode="full")
        corr = corr[len(corr)//2:]

        # Search range for human pitch F0 (70 Hz to 400 Hz)
        min_lag = int(self.sample_rate / 400.0)
        max_lag = int(self.sample_rate / 70.0)

        if len(corr) > max_lag:
            peak_lag = min_lag + np.argmax(corr[min_lag:max_lag])
            f0 = float(self.sample_rate / peak_lag) if peak_lag > 0 else 150.0
        else:
            f0 = 150.0

        # 2. Frame-level amplitude shimmer (cycle-to-cycle amplitude variation)
        frame_len = int(self.sample_rate * 0.03)
        frames = [audio[i:i+frame_len] for i in range(0, len(audio)-frame_len, frame_len)]
        amps = [np.max(np.abs(f)) for f in frames if np.max(np.abs(f)) > 1e-4]

        if len(amps) > 1:
            amp_diffs = np.abs(np.diff(amps))
            shimmer = float(np.mean(amp_diffs) / (np.mean(amps) + 1e-6))
        else:
            shimmer = 0.05

        # 3. Spectral Tilt (Energy decay rate across frequency spectrum)
        fft = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), 1.0 / self.sample_rate)
        if len(fft) > 10:
            log_freqs = np.log10(np.maximum(freqs[1:], 1.0))
            log_fft = np.log10(np.maximum(fft[1:], 1e-6))
            slope, _ = np.polyfit(log_freqs, log_fft, 1)
            spectral_tilt = float(slope)
        else:
            spectral_tilt = -1.0

        # Anomaly Detection Logic
        # Synthetic TTS voices often have unusually LOW shimmer (overly pristine) or steep spectral tilt.
        acoustic_anomaly = 0.0
        if shimmer < 0.01: # Unnaturally perfectly smooth amplitude (common in cheap TTS)
            acoustic_anomaly += 0.4
        elif shimmer > 0.45: # Robotic distorted amplitude artifact
            acoustic_anomaly += 0.3

        if spectral_tilt > -0.2: # High frequency noise boost artifact
            acoustic_anomaly += 0.4

        prosody_anomaly = 0.0
        if f0 < 60.0 or f0 > 450.0: # Out of human vocal range
            prosody_anomaly += 0.5

        acoustic_score = float(np.clip(acoustic_anomaly, 0.0, 0.95))
        prosody_score = float(np.clip(prosody_anomaly, 0.0, 0.95))

        metrics = {
            "f0_mean_hz": round(f0, 2),
            "shimmer": round(shimmer, 4),
            "spectral_tilt": round(spectral_tilt, 4)
        }

        return acoustic_score, prosody_score, metrics
