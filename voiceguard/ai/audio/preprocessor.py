import io
import numpy as np
import soundfile as sf
from typing import Tuple, List

TARGET_SAMPLE_RATE = 16000

class AudioPreprocessor:
    """
    Audio Preprocessor for VoiceGuard AI pipelines.
    Normalizes, resamples, and slices audio streams into clean 16kHz mono numpy float32 arrays.
    """

    def __init__(self, target_sample_rate: int = TARGET_SAMPLE_RATE):
        self.target_sr = target_sample_rate

    def load_audio_bytes(self, audio_bytes: bytes) -> Tuple[np.ndarray, int]:
        """
        Load audio from bytes (WAV, MP3, FLAC, OGG) and convert to float32 mono array.
        """
        buffer = io.BytesIO(audio_bytes)
        try:
            data, sr = sf.read(buffer, dtype="float32")
            if data.ndim > 1:
                # Average multi-channel to mono
                data = np.mean(data, axis=1)
            
            if sr != self.target_sr:
                data = self._resample(data, sr, self.target_sr)
                sr = self.target_sr
            
            # Normalize peak amplitude
            max_amp = np.max(np.abs(data))
            if max_amp > 1e-5:
                data = data / max_amp
                
            return data.astype(np.float32), sr
        except Exception as e:
            # Fallback to zero signal on decode error
            return np.zeros(self.target_sr * 2, dtype=np.float32), self.target_sr

    def _resample(self, audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
        """
        Linear interpolation resampling for dependency-light CPU operation.
        """
        if orig_sr == target_sr:
            return audio
        duration = len(audio) / orig_sr
        target_length = int(duration * target_sr)
        orig_indices = np.linspace(0, len(audio) - 1, num=len(audio))
        target_indices = np.linspace(0, len(audio) - 1, num=target_length)
        return np.interp(target_indices, orig_indices, audio)

    def calculate_snr(self, audio: np.ndarray) -> float:
        """
        Estimate Signal-to-Noise Ratio (SNR) in dB.
        """
        if len(audio) == 0:
            return 0.0
        signal_power = np.mean(audio ** 2)
        if signal_power < 1e-8:
            return 0.0
        # Estimate noise floor from lowest 10% energy frames
        frame_len = int(self.target_sr * 0.02)
        if len(audio) < frame_len:
            return 30.0
        frames = [np.mean(audio[i:i+frame_len]**2) for i in range(0, len(audio)-frame_len, frame_len)]
        noise_power = np.percentile(frames, 10) + 1e-9
        snr_db = 10 * np.log10(signal_power / noise_power)
        return float(np.clip(snr_db, 0.0, 60.0))

    def chunk_audio(self, audio: np.ndarray, chunk_dur_sec: float = 2.0, overlap_sec: float = 0.5) -> List[np.ndarray]:
        """
        Split continuous audio array into overlapping chunks.
        """
        chunk_len = int(chunk_dur_sec * self.target_sr)
        step_len = int((chunk_dur_sec - overlap_sec) * self.target_sr)
        
        if len(audio) <= chunk_len:
            # Pad if shorter than chunk length
            padded = np.zeros(chunk_len, dtype=np.float32)
            padded[:len(audio)] = audio
            return [padded]
        
        chunks = []
        for start in range(0, len(audio) - chunk_len + 1, step_len):
            chunks.append(audio[start:start + chunk_len])
        return chunks
