import numpy as np

class VoiceActivityDetector:
    """
    Voice Activity Detection (VAD) module.
    Filters out background noise and silence before sending chunks to downstream AI models.
    """

    def __init__(self, sample_rate: int = 16000, energy_threshold: float = 0.01):
        self.sample_rate = sample_rate
        self.energy_threshold = energy_threshold

    def is_speech(self, audio_chunk: np.ndarray) -> bool:
        """
        Check if audio chunk contains human voice speech.
        """
        if len(audio_chunk) == 0:
            return False

        # Calculate Root Mean Square (RMS) energy
        rms = np.sqrt(np.mean(audio_chunk ** 2))
        
        # Calculate Zero Crossing Rate (ZCR)
        zero_crossings = np.sum(np.abs(np.diff(np.sign(audio_chunk)))) / (2 * len(audio_chunk))

        # Human speech typically has RMS above energy_threshold and ZCR within 0.02 - 0.35
        is_speech_energy = rms > self.energy_threshold
        is_speech_zcr = 0.01 <= zero_crossings <= 0.40

        return bool(is_speech_energy and is_speech_zcr)

    def extract_speech_segments(self, audio: np.ndarray, frame_duration_ms: int = 30) -> np.ndarray:
        """
        Extract only active speech frames from audio array, stripping leading/trailing silence.
        """
        frame_size = int(self.sample_rate * (frame_duration_ms / 1000.0))
        num_frames = len(audio) // frame_size
        
        speech_frames = []
        for i in range(num_frames):
            frame = audio[i * frame_size : (i + 1) * frame_size]
            if self.is_speech(frame):
                speech_frames.append(frame)
                
        if not speech_frames:
            return audio # Fallback to original audio if no speech isolated
            
        return np.concatenate(speech_frames)
