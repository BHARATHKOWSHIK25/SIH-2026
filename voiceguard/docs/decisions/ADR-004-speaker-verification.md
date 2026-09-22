# ADR-004: Speaker Verification Model

**Status**: Accepted (pending installation validation)  
**Date**: 2026-09-04  
**Decision**: SpeechBrain ECAPA-TDNN pretrained on VoxCeleb

## Context

VoiceGuard requires speaker verification that:
1. Extracts a speaker embedding from audio
2. Compares current speaker against a registered profile
3. Returns a similarity score and identity decision
4. Runs on CPU with acceptable latency
5. Is separate from deepfake detection (independent security signal)

## Decision

Use **SpeechBrain's ECAPA-TDNN** pretrained on VoxCeleb (`spkrec-ecapa-voxceleb`).

## Alternatives Considered

| Alternative | Reason Deferred |
|-------------|----------------|
| resemblyzer | Lighter (~5MB) but less accurate; good fallback |
| pyannote.audio | Heavier dependency; designed for diarization not verification |
| Custom embedding model | Requires training data and infrastructure |
| x-vector (Kaldi) | Requires Kaldi installation; complex setup on Windows |

## Rationale

- **State-of-the-art**: ECAPA-TDNN is the current standard for speaker verification.
- **192-dim embeddings**: Compact but discriminative.
- **~14M parameters**: Manageable on CPU.
- **Pretrained on VoxCeleb**: Large-scale speaker recognition dataset.
- **SpeechBrain API**: Clean Python interface for embedding extraction.

## Risks

- **SpeechBrain installation**: Heavy dependency tree. May conflict with Python 3.12 on Windows.
- **Download size**: Model weights + dependencies ~500MB+.

## Fallback Plan

If SpeechBrain fails to install:
1. Use `resemblyzer` (GE2E-based, ~5MB model, pip install)
2. Use standalone ECAPA checkpoint loaded directly with PyTorch

## Verification Flow

```
Enrollment: audio → ECAPA → 192-dim embedding → store
Verification: audio → ECAPA → 192-dim embedding → cosine_similarity(stored, current) → score
```

## Thresholds (UNCALIBRATED DEFAULTS)

| Status | Similarity Range |
|--------|-----------------|
| MATCH | ≥ 0.70 |
| UNCERTAIN | 0.40 – 0.69 |
| MISMATCH | < 0.40 |

These must be calibrated on validation data.

## Limitations

- Speaker verification does NOT prove voice is genuine (a cloned voice may produce high similarity).
- This is why deepfake detection and speaker verification must remain independent signals.
- Performance degrades with short audio (<2 seconds).
