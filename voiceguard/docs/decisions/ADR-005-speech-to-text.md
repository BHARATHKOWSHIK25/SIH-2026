# ADR-005: Speech-to-Text Engine

**Status**: Accepted  
**Date**: 2026-09-04  
**Decision**: faster-whisper with Whisper base model, INT8 quantization

## Context

VoiceGuard requires speech-to-text for:
1. Transcribing conversations for social engineering detection
2. Near-real-time transcription during live calls
3. Multilingual support (English, Hindi, Telugu, Tamil, Kannada)
4. Language identification
5. Timestamped segments

## Decision

Use **faster-whisper** (CTranslate2 backend) with the **base** model and INT8 quantization.

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|----------------|
| openai-whisper (PyTorch) | 2–4x slower on CPU than faster-whisper |
| whisper.cpp | Requires C++ compilation; less Python-native |
| Google Cloud Speech-to-Text | Requires API key, internet, cost |
| Vosk | Good offline but weaker multilingual support for Indian languages |
| Azure Speech | Cloud dependency, cost |

## Rationale

- **2–4x faster than vanilla Whisper**: CTranslate2 optimizes for CPU with INT8.
- **INT8 quantization**: Reduces memory and latency with minimal accuracy loss.
- **Multilingual**: Whisper base supports 99 languages including Hindi, Telugu, Tamil, Kannada.
- **Python native**: `pip install faster-whisper`.
- **No FFmpeg required**: Uses PyAV internally.
- **Compatible with Python 3.12**: CTranslate2 has wheels.

## Performance (ESTIMATES — must benchmark)

| Metric | Whisper base INT8 |
|--------|-------------------|
| Model size | ~80MB (INT8) |
| RAM usage | ~200MB |
| RTF on modern CPU | ~0.5–1.0 (real-time to 2x real-time) |
| Languages | 99 including Indian languages |

## Configuration

```python
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_array, language=None)  # auto-detect
```

## Tradeoffs

- **base vs. small**: `base` (74M params) is faster but less accurate than `small` (244M params). Configurable via settings.
- **Chunk processing**: Whisper processes in 30-second windows. For streaming, we process accumulated chunks and handle partial results.

## Limitations

- Transcription accuracy on Indian accents may vary (not benchmarked).
- Code-switching (Hindi + English in same sentence) may produce mixed results.
- Low audio quality significantly impacts accuracy.
- Do not trust low-confidence transcriptions for high-risk decisions.
