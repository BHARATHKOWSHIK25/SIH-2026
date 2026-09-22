# ADR-003: Deepfake Detection Model

**Status**: Accepted (pending benchmark at Step 7)  
**Date**: 2026-09-04  
**Decision**: HuggingFace pretrained wav2vec2-based audio deepfake detector

## Context

VoiceGuard requires a model that:
1. Classifies audio as genuine or synthetic
2. Outputs a probability score (not just binary)
3. Runs on CPU with acceptable latency (<1s per 3-second chunk)
4. Is pretrained on voice anti-spoofing data (ASVspoof or equivalent)
5. Accepts 16kHz mono waveform input
6. Is available without training infrastructure

## Decision

Use a **pretrained wav2vec2-based audio deepfake detector** from HuggingFace (e.g., `garystafford/wav2vec2-deepfake-voice-detector` or similar validated checkpoint).

Behind a **model abstraction layer** so the actual model can be swapped without changing business logic.

## Alternatives Considered

| Alternative | Reason Deferred |
|-------------|----------------|
| Custom ResNet-18 on Mel spectrograms | No pretrained checkpoint for deepfake detection; requires training from scratch |
| AASIST | Complex architecture; requires custom model loading (not standard HuggingFace API) |
| Res2TCNGuard | Potentially lighter; evaluate as fallback if wav2vec2 is too slow on CPU |
| Spectra-0 (wav2vec2 + ECAPA-TDNN) | Heavy model; may be too slow on CPU |

## Rationale

- **Pretrained and validated**: Published model with known benchmark results.
- **HuggingFace API**: Standard `AutoModelForAudioClassification` loading.
- **Probability output**: `softmax` over [real, fake] logits gives continuous probability.
- **CPU compatible**: Can run in `eval()` mode with `torch.no_grad()`.

## Risks

- **CPU latency unknown**: wav2vec2 base has ~95M params. Estimated 300–800ms per 3s chunk on CPU. **MUST BENCHMARK before integration (Step 7).**
- **May not generalize to Indian languages**: Model likely trained on English-only data.
- **May not generalize to novel TTS methods**: Limited to attack types in training data.

## Fallback Plan

If CPU latency exceeds 1.5s per 3s chunk:
1. Try ONNX export with INT8 quantization
2. Try lighter model (Res2TCNGuard or custom CNN)
3. Use async processing (analyze previous chunk while recording next)

## Tradeoffs

- **Accuracy vs. Latency**: wav2vec2 is more accurate than simple CNN but slower on CPU.
- **Model size**: ~380MB disk, ~500MB RAM.

## Limitations

- Requires PyTorch CPU installation (~800MB–1.5GB disk).
- Performance claims must be validated by actual benchmarking, not assumed.
- May produce high false positive rates on degraded audio (telephone quality, compression).
