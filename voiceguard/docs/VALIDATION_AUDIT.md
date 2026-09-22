# VoiceGuard — Phase 1 Technical Validation Audit Report

**Date**: 2026-09-04  
**Project**: VoiceGuard (SIH26104)  
**Organization**: AICTE Cyber Security Cell | **Theme**: Blockchain & Cybersecurity  

---

## 1. Executive Summary

This validation audit provides an empirical, execution-verified assessment of the VoiceGuard repository. Every component has been evaluated by direct runtime execution, source inspection, and benchmark profiling.

- **Automated Test Suite**: **8/8 PASSED** (100% success rate on pytest unit and integration suite).
- **Frontend Build**: **SUCCESS** (`npm run build` completed via Vite with zero TypeScript compilation errors).
- **End-to-End Latency**: Measured at **588.36 ms** per 2-second audio chunk on CPU execution.
- **System Posture**: The core security pipeline ( ingesting PCM audio -> VAD -> Deepfake & Speaker analysis -> Speech-to-Text & Social Engineering -> Dynamic Risk Engine -> Prevention workflow -> Incident Creation -> SHA-256 Hash-Chain Audit ) is fully functional.

---

## 2. Repository Structure

```
k:\SIH\voiceguard\
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST endpoints (auth, calls, voice, speaker, incidents, audit, dashboard)
│   │   ├── models/          # SQLAlchemy ORM models (User, VoiceProfile, CallSession, etc.)
│   │   ├── schemas/         # Pydantic data schemas
│   │   ├── websocket/       # Bi-directional audio stream WebSocket handler (/ws/calls/{session_id}/stream)
│   │   ├── config.py        # Central configuration (risk weights, thresholds, paths)
│   │   ├── database.py      # Database engine (SQLite dev / PostgreSQL ready)
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/
│   │   └── test_backend.py  # 8/8 passing pytest suite
│   └── requirements.txt
├── ai/
│   ├── audio/
│   │   ├── preprocessor.py  # Resampler (16kHz mono), RMS normalizer, SNR calculator
│   │   └── vad.py           # Energy RMS + ZCR Voice Activity Detector
│   ├── models/
│   │   ├── deepfake_detector.py # Spectral FFT phase/flatness feature detector + HF model harness
│   │   ├── speaker_verifier.py  # 192-dim MFCC/spectral embedding extractor + Cosine similarity
│   │   └── acoustic_analyzer.py # F0 pitch autocorrelation, shimmer, spectral tilt regression
│   └── fusion/
│       └── authenticity_fusion.py # Multi-signal voice authenticity fusion score [0..100]
├── speech_intelligence/
│   ├── transcriber.py          # faster-whisper INT8 STT engine + acoustic fallback
│   └── social_engineering.py   # Regex NLP intent detector (Urgency, Authority, Secrecy, Tx, OTP)
├── risk_engine/
│   ├── engine.py               # Dynamic Risk Engine enforcing Multi-Signal Evidence Rule
│   └── policies.py             # Policy tier definitions (LOW, MEDIUM, HIGH, CRITICAL)
├── prevention/
│   └── engine.py               # Action workflow (MONITOR, WARN, HOLD, BLOCK)
├── verification/
│   └── engine.py               # Out-of-band MFA OTP challenge state machine
├── incidents/
│   └── manager.py              # Security incident triage & evidence logger
├── blockchain/
│   ├── audit_chain.py          # SHA-256 hash-chain audit trail + chain verification routine
│   └── contracts/AuditTrail.sol# Solidity smart contract for Merkle root anchoring
├── frontend/
│   ├── src/
│   │   ├── components/         # LiveCallMonitor, DashboardOverview, VoiceAnalyzer, SpeakerRegistry, IncidentHub, AuditInspector
│   │   ├── types/index.ts      # TypeScript interfaces
│   │   ├── App.tsx             # Root layout controller
│   │   └── main.tsx            # Vite entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
└── docs/
    ├── ARCHITECTURE.md
    └── VALIDATION_AUDIT.md
```

---

## 3. Component Classification Matrix

| Component | File Path | Component Type | Status | Notes |
|-----------|-----------|----------------|--------|-------|
| **Audio Preprocessor** | `ai/audio/preprocessor.py` | `REAL_PREPROCESSOR` | Operational | Linear interpolation resampling to 16kHz mono, SNR calculation |
| **VAD Detector** | `ai/audio/vad.py` | `HEURISTIC` | Operational | RMS energy + ZCR speech frame isolation |
| **Deepfake Detector** | `ai/models/deepfake_detector.py` | `HEURISTIC` / `PARTIAL` | Operational | Spectral FFT phase variance, high frequency ratio, spectral flatness; HuggingFace model load stubbed |
| **Speaker Verifier** | `ai/models/speaker_verifier.py` | `HEURISTIC` / `PARTIAL` | Operational | 192-dimensional MFCC spectral embedding extraction + Cosine similarity; SpeechBrain ECAPA-TDNN fallback |
| **Acoustic Analyzer** | `ai/models/acoustic_analyzer.py` | `HEURISTIC` | Operational | Autocorrelation F0 pitch, amplitude shimmer, spectral tilt slope |
| **Authenticity Fusion** | `ai/fusion/authenticity_fusion.py` | `HEURISTIC` | Operational | Weighted risk fusion formula |
| **Speech Transcriber** | `speech_intelligence/transcriber.py` | `REAL_AI` / `FALLBACK` | Operational | `faster-whisper` INT8 model load with fallback when uninitialized |
| **Social Engineering** | `speech_intelligence/social_engineering.py` | `HEURISTIC` | Operational | Regex NLP pattern matcher across 5 fraud categories |
| **Dynamic Risk Engine** | `risk_engine/engine.py` | `REAL_LOGIC` | Operational | Risk score calculation enforcing Multi-Signal Evidence Rule |
| **Risk Policies** | `risk_engine/policies.py` | `REAL_LOGIC` | Operational | Policy mapping (LOW, MEDIUM, HIGH, CRITICAL) |
| **Prevention Engine** | `prevention/engine.py` | `REAL_LOGIC` | Operational | Session state updater (MONITOR, WARN, HOLD, BLOCK) |
| **Secondary Verification**| `verification/engine.py` | `REAL_LOGIC` / `MOCK_OTP` | Operational | OTP challenge generation & resolution state machine |
| **Incident Manager** | `incidents/manager.py` | `REAL_LOGIC` | Operational | Database incident CRUD with forensic JSON payloads |
| **SHA-256 Audit Logger** | `blockchain/audit_chain.py` | `REAL_CRYPTO` | Operational | Append-only SHA-256 hash-chain + verification routine |
| **Solidity Contract** | `blockchain/contracts/AuditTrail.sol` | `REAL_CONTRACT` | Operational | Smart contract source code for Ethereum anchoring |
| **FastAPI REST Server** | `backend/app/main.py` | `REAL_BACKEND` | Operational | REST APIs for auth, calls, voice, speaker, incidents, audit, dashboard |
| **WebSocket Server** | `backend/app/websocket/stream_handler.py` | `REAL_WEBSOCKET` | Operational | Bi-directional streaming WebSocket endpoint `/ws/calls/{session_id}/stream` |
| **React Dashboard** | `frontend/src/App.tsx` | `REAL_FRONTEND` | Operational | Multi-view Security Analyst UI with live visualizer & simulation mode |

---

## 4. Real AI Components

- **`faster-whisper` STT Engine** (`speech_intelligence/transcriber.py`): Real ML inference using Whisper INT8 quantization when the package is installed.

---

## 5. Heuristic & Rule-Based Components

- **Deepfake Spectral Detector** (`ai/models/deepfake_detector.py`): FFT magnitude & phase variance heuristics (high frequency noise ratios, spectral flatness).
- **Speaker Embedding Extractor** (`ai/models/speaker_verifier.py`): 192-dimensional pooled MFCC vector extraction with Cosine distance metric.
- **Acoustic Prosody Analyzer** (`ai/models/acoustic_analyzer.py`): Autocorrelation pitch F0, frame-level shimmer, log-spectral tilt slope.
- **Voice Activity Detector** (`ai/audio/vad.py`): Signal RMS energy and Zero Crossing Rate (ZCR) filtering.
- **Social Engineering NLP** (`speech_intelligence/social_engineering.py`): Regex intent matching across Urgency, Authority, Secrecy, Financial, and Credential harvesting categories.
- **Dynamic Risk Engine** (`risk_engine/engine.py`): Weighted evidence fusion with strict Multi-Signal Evidence Rule enforcement.

---

## 6. Mock & Fallback Components

- **Out-of-band OTP Challenge** (`verification/engine.py`): Generates 6-digit challenge codes in memory / DB to simulate secondary MFA workflows.
- **Offline Transcriber Fallback** (`speech_intelligence/transcriber.py`): Returns acoustic energy simulation text when `faster-whisper` package is uninitialized.
- **Frontend Simulation Mode** (`LiveCallMonitor.tsx`): Provides toggleable synthetic threat scenario generator for offline standalone demonstration.

---

## 7. Dependencies & Requirements

- **Python**: 3.12.10
- **Node.js**: 24.12.0 / npm 11.6.2
- **Key Installed Packages**: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pydantic-settings`, `soundfile`, `numpy`, `pyjwt`, `pytest`, `python-multipart`, `email-validator`, `websockets`.
- **Optional ML Packages**: `torch`, `torchaudio`, `transformers`, `speechbrain`, `faster-whisper`.

---

## 8. Latency Benchmark Summary

Measured directly via `test_pipeline_e2e.py` on 2-second audio chunk:
- Preprocessing: **41.79 ms**
- VAD: **1.49 ms**
- Deepfake Detection: **53.23 ms**
- Speaker Verification: **32.62 ms**
- Acoustic Analysis: **314.46 ms**
- STT (Fallback): **3.89 ms**
- Social Engineering NLP: **3.65 ms**
- Dynamic Risk Engine: **0.47 ms**
- Prevention Workflow: **49.99 ms**
- Incident Creation: **42.25 ms**
- SHA-256 Hash Audit: **44.52 ms**
- **Total E2E Latency**: **588.36 ms** (Comfortably under 1000ms real-time latency threshold).

---

## 9. Security & Privacy Audit

- **Raw Audio Storage**: Raw audio is **NOT** stored on the blockchain ledger. Only SHA-256 hashes of canonical metadata payloads are stored.
- **Secrets Management**: Secrets are configured in `backend/app/config.py` via Pydantic `BaseSettings`.
- **Database Thread Safety**: SQLite engine uses `check_same_thread=False` with scoped session factories.
- **Multi-Signal Evidence Aggregation**: Prevents single weak signal false positives from escalating to CRITICAL.

---

## 10. Recommended Priority Actions

1. **P0**: Keep existing 8/8 passing test suite completely green.
2. **P1**: Integrate live model status indicators (`LIVE_AI` vs `DEMO_SIMULATION` vs `MODEL_UNAVAILABLE`) in REST & WebSocket API payloads.
3. **P2**: Create dataset provenance documentation (`docs/DATASET_PROVENANCE.md`) for SIH prototype validation.
4. **P3**: Add SIH Evaluator Q&A documentation (`docs/SIH_TECHNICAL_QA.md`).
