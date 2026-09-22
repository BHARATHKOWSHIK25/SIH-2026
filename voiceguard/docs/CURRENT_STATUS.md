# VoiceGuard — Current System Status & Model Transparency

**Problem Statement**: SIH26104 | **Organization**: AICTE Cyber Security Cell  

---

## 1. System Operating Modes

VoiceGuard operates under transparent, self-declaring execution modes to ensure full clarity for security analysts and SIH evaluators.

| Mode | Label | Description |
|------|-------|-------------|
| **LIVE_AI** | `LIVE AI MODE` | Native PyTorch / HuggingFace / SpeechBrain / faster-whisper neural networks executing live model inference on CPU. |
| **PARTIAL_AI** | `PARTIAL AI MODE` | Real acoustic spectral signal processing (FFT phase variance, MFCC 192-dim embeddings, pitch F0 autocorrelation, shimmer, spectral tilt) running alongside regex NLP rules. |
| **DEMO_SIMULATION** | `DEMO / SIMULATION MODE` | Synthetic threat scenario generation for offline standalone UI testing without backend connection. |
| **MODEL_UNAVAILABLE** | `MODEL UNAVAILABLE` | Explicit status returned when model weights or hardware resources are uninitialized. |

---

## 2. Component Implementation Status

```
Component                       Type            Operational Status      Model Name / Heuristic Algorithm
-------------------------------------------------------------------------------------------------------
Audio Preprocessor              REAL            ACTIVE                  16kHz Linear Resampler & SNR Calc
Voice Activity Detector (VAD)   HEURISTIC       ACTIVE                  RMS Energy + ZCR Thresholding
Deepfake Voice Detector         HEURISTIC/AI    ACTIVE (PARTIAL_AI)     FFT Phase Variance & Flatness
Speaker Identity Verifier       HEURISTIC/AI    ACTIVE (PARTIAL_AI)     192-dim MFCC Embedding + Cosine Sim
Acoustic & Prosody Analyzer     HEURISTIC       ACTIVE                  Autocorrelation F0, Shimmer, Tilt
Speech-to-Text Transcriber      REAL_AI/FALLBACKACTIVE                  faster-whisper INT8 / Acoustic STT
Social Engineering Detector     HEURISTIC       ACTIVE                  5-Category Regex Pattern Matcher
Dynamic Risk Engine             REAL_LOGIC      ACTIVE                  Multi-Signal Evidence Aggregation
Prevention Action Engine        REAL_LOGIC      ACTIVE                  Policy Workflow State Machine
Secondary Verification Engine   REAL_LOGIC      ACTIVE                  Out-of-band OTP Challenge Simulator
Security Incident Manager       REAL_LOGIC      ACTIVE                  SQLAlchemy Forensic Evidence Logger
SHA-256 Hash-Chain Audit        REAL_CRYPTO     ACTIVE                  Cryptographic Hash-Chain Ledger
Solidity AuditTrail Contract    REAL_CONTRACT   ACTIVE                  AuditTrail.sol Merkle Root Anchor
React Security Dashboard        REAL_FRONTEND   ACTIVE                  React 18 + Vite + WebSockets
```

---

## 3. End-to-End Execution Profile

- **Backend Test Status**: 8/8 Tests PASSED
- **Frontend Build Status**: Built successfully via Vite (`dist/` clean)
- **Total E2E Pipeline Latency**: **588.36 ms** per 2-second audio chunk
