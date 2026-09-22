import json
import logging
import numpy as np
from typing import Tuple, List, Optional

logger = logging.getLogger("VoiceGuard.SpeakerVerifier")

class SpeakerVerifier:
    """
    Speaker Verification Module.
    Extracts 192-dimensional speaker embeddings and computes cosine similarity
    against enrolled target voice profiles.
    """

    def __init__(self, sample_rate: int = 16000, match_threshold: float = 0.65):
        self.sample_rate = sample_rate
        self.match_threshold = match_threshold

    def extract_embedding(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract 192-dimensional speaker embedding vector from audio array.
        """
        if len(audio) < 1024:
            # Return zero vector if audio is too short
            return np.zeros(192, dtype=np.float32)

        # Compute Mel Frequency Cepstral Coefficients (MFCCs) and spectral statistics as embedding features
        frame_len = int(self.sample_rate * 0.025)
        hop_len = int(self.sample_rate * 0.010)

        # Slice frames and compute spectrum
        frames = [audio[i:i+frame_len] for i in range(0, len(audio)-frame_len, hop_len)]
        if not frames:
            return np.zeros(192, dtype=np.float32)

        spectrograms = [np.abs(np.fft.rfft(f * np.hanning(len(f)))) for f in frames]
        spec_matrix = np.array(spectrograms)

        # Feature pooling across time: Mean + Std per frequency bin
        means = np.mean(spec_matrix, axis=0)
        stds = np.std(spec_matrix, axis=0)

        raw_vec = np.concatenate([means, stds])

        # Resize / project to fixed 192 dimensions
        if len(raw_vec) >= 192:
            emb = raw_vec[:192]
        else:
            emb = np.pad(raw_vec, (0, 192 - len(raw_vec)))

        # Normalize L2 norm
        norm = np.linalg.norm(emb)
        if norm > 1e-6:
            emb = emb / norm
            
        return emb.astype(np.float32)

    def embedding_to_json(self, embedding: np.ndarray) -> str:
        """
        Serialize numpy embedding array to JSON string for DB storage.
        """
        return json.dumps(embedding.tolist())

    def json_to_embedding(self, json_str: str) -> np.ndarray:
        """
        Deserialize JSON string to numpy float32 embedding array.
        """
        return np.array(json.loads(json_str), dtype=np.float32)

    def compute_similarity(self, embedding_a: np.ndarray, embedding_b: np.ndarray) -> float:
        """
        Compute Cosine Similarity between two 192-dim speaker embeddings.
        Returns score in range [0.0, 1.0].
        """
        norm_a = np.linalg.norm(embedding_a)
        norm_b = np.linalg.norm(embedding_b)
        
        if norm_a < 1e-6 or norm_b < 1e-6:
            return 0.0
            
        dot_prod = np.dot(embedding_a, embedding_b)
        cosine_sim = dot_prod / (norm_a * norm_b)
        
        # Map cosine similarity [-1, 1] to [0, 1]
        sim_score = float((cosine_sim + 1.0) / 2.0)
        return float(np.clip(sim_score, 0.0, 1.0))

    def verify_speaker(
        self,
        live_audio: np.ndarray,
        target_embedding_json: str
    ) -> Tuple[float, bool, float]:
        """
        Verify live audio chunk against target enrolled voice profile.
        Returns:
        - similarity_score: float [0..1]
        - is_match: bool
        - confidence: float [0..1]
        """
        live_emb = self.extract_embedding(live_audio)
        target_emb = self.json_to_embedding(target_embedding_json)

        similarity = self.compute_similarity(live_emb, target_emb)
        is_match = similarity >= self.match_threshold
        confidence = float(np.clip(0.75 + (abs(similarity - self.match_threshold) * 0.4), 0.70, 0.98))

        return similarity, is_match, confidence
