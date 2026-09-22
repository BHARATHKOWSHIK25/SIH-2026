# 🛡️ VoiceGuard AI — Real-Time Voice Impersonation Detection & Prevention

> **Smart India Hackathon 2026 | Problem Statement: SIH26104**
> **Organization: AICTE Cyber Security Cell**

<p align="center">
  <img src="https://img.shields.io/badge/SIH-2026-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.11+-green?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/AI%2FML-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch" />
  <img src="https://img.shields.io/badge/Blockchain-Ethereum-3C3C3D?style=for-the-badge&logo=ethereum" />
</p>

---

## 📌 Problem Statement

Voice impersonation and deepfake audio attacks are an emerging threat in cybersecurity — targeting financial institutions, government agencies, and critical infrastructure. Adversaries clone voices using AI tools to bypass speaker authentication systems, authorize fraudulent transactions, and manipulate personnel over live phone calls.

**VoiceGuard AI** is a real-time, multi-layered defense system that detects, prevents, and audits voice impersonation attacks the moment they occur — before damage is done.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎙️ **Real-Time Deepfake Detection** | FFT phase variance & spectral flatness analysis on live audio streams |
| 🧬 **Speaker Identity Verification** | 192-dim MFCC embedding + cosine similarity scoring |
| 🧠 **Social Engineering Detection** | 5-category NLP regex pattern matcher for manipulation tactics |
| ⚡ **Dynamic Risk Engine** | Multi-signal evidence aggregation with a policy workflow state machine |
| 🔐 **Blockchain Audit Trail** | SHA-256 hash-chain ledger anchored to Ethereum via AuditTrail.sol |
| 📊 **Live Security Dashboard** | React 18 + WebSocket real-time monitoring UI |
| 🔔 **Automated Prevention Actions** | Out-of-band OTP challenge, call flagging, and incident escalation |
| 🗣️ **Speech-to-Text** | faster-whisper INT8 transcription for forensic logging |

---

## 🏗️ Architecture Overview

`
┌─────────────────────────────────────────────────────────────────────┐
│                        VoiceGuard AI System                         │
├─────────────┬──────────────┬────────────────┬───────────────────────┤
│  Frontend   │   Backend    │    AI Engine   │     Blockchain        │
│  (React 18) │  (FastAPI)   │  (PyTorch/ML)  │  (Solidity/Ethereum)  │
├─────────────┼──────────────┼────────────────┼───────────────────────┤
│ Dashboard   │ REST API     │ Audio Preproc  │ AuditTrail.sol        │
│ LiveMonitor │ WebSocket    │ VAD            │ SHA-256 Hash Chain    │
│ AuditLog    │ Auth (JWT)   │ Deepfake Det.  │ Merkle Root Anchoring │
│ Incidents   │ SQLAlchemy   │ Speaker Verif. │                       │
│ VoiceAnalyz │ Alembic      │ Acoustic Anlyz │                       │
│ SpeakerReg  │              │ STT (Whisper)  │                       │
└─────────────┴──────────────┴────────────────┴───────────────────────┘
`

---

## 📁 Project Structure

`
SIH-2026/
└── voiceguard/
    ├── ai/                          # AI & ML Models
    │   ├── audio/                   # Audio preprocessor & VAD
    │   ├── models/                  # Deepfake detector, speaker verifier, acoustic analyzer
    │   └── fusion/                  # Authenticity fusion engine
    ├── backend/                     # FastAPI Backend
    │   ├── app/
    │   │   ├── api/v1/              # REST endpoints (auth, calls, voice, speaker, incidents, audit)
    │   │   ├── models/              # SQLAlchemy ORM models
    │   │   ├── schemas/             # Pydantic schemas
    │   │   └── websocket/           # Real-time WebSocket stream handler
    │   └── requirements.txt
    ├── blockchain/                  # Blockchain Audit Layer
    │   ├── audit_chain.py           # SHA-256 hash-chain ledger
    │   └── contracts/AuditTrail.sol # Solidity smart contract
    ├── frontend/                    # React Dashboard
    │   └── src/
    │       └── components/
    │           ├── DashboardOverview.tsx
    │           ├── LiveCallMonitor.tsx
    │           ├── VoiceAnalyzer.tsx
    │           ├── AuditInspector.tsx
    │           ├── IncidentHub.tsx
    │           └── SpeakerRegistry.tsx
    ├── speech_intelligence/         # STT & Social Engineering Detector
    ├── risk_engine/                 # Dynamic risk scoring & policies
    ├── incidents/                   # Security incident manager
    ├── prevention/                  # Prevention action engine
    └── verification/                # Secondary verification engine
`

---

## 🤖 AI/ML Pipeline

The end-to-end audio analysis pipeline processes each 2-second audio chunk through:

1. **Audio Preprocessor** — 16kHz linear resampling & SNR calculation
2. **Voice Activity Detector (VAD)** — RMS Energy + Zero-Crossing Rate thresholding
3. **Deepfake Voice Detector** — FFT phase variance & spectral flatness heuristics
4. **Speaker Identity Verifier** — 192-dim MFCC embedding + cosine similarity
5. **Acoustic & Prosody Analyzer** — Autocorrelation F0 (pitch), shimmer & spectral tilt
6. **Speech-to-Text** — faster-whisper INT8 / Acoustic STT fallback
7. **Social Engineering Detector** — 5-category regex NLP pattern matcher
8. **Risk Engine** — Multi-signal evidence aggregation (confidence scoring)
9. **Prevention Engine** — Policy state machine (alert → challenge → block)

> ⚡ **Total E2E Pipeline Latency: ~588 ms per 2-second audio chunk**

---

## 🔗 Blockchain Audit

Every security event is cryptographically logged in a SHA-256 hash chain and anchored on-chain:

- **lockchain/audit_chain.py** — Maintains a tamper-evident hash-chain ledger of all events
- **AuditTrail.sol** — Ethereum-compatible Solidity contract that anchors Merkle root batch hashes on-chain for immutable, third-party verifiable audit trails

---

## 🖥️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Core runtime |
| FastAPI | 0.109+ | REST API & WebSocket server |
| SQLAlchemy | 2.0+ | ORM & database management |
| PyTorch | 2.2+ | ML model inference |
| SpeechBrain | 0.5+ | Speaker verification |
| faster-whisper | 0.10+ | Speech-to-text transcription |
| librosa | 0.10+ | Audio feature extraction |
| Alembic | 1.13+ | Database migrations |
| PyJWT | 2.8+ | JWT authentication |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18.2 | UI framework |
| TypeScript | 5.2 | Type-safe development |
| Vite | 5.1 | Build tool & dev server |
| TailwindCSS | 3.4 | Utility-first styling |
| Recharts | 2.12 | Real-time data visualization |
| Lucide React | 0.330 | Icon library |

### Infrastructure
| Technology | Purpose |
|-----------|---------|
| SQLite | Local database for prototype |
| WebSockets | Real-time audio stream processing |
| Solidity 0.8.20 | Ethereum smart contract |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

---

### 🔧 Backend Setup

`ash
# Navigate to backend
cd voiceguard/backend

# Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
`

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🎨 Frontend Setup

`ash
# Navigate to frontend
cd voiceguard/frontend

# Install dependencies
npm install

# Start development server
npm run dev
`

Dashboard available at: [http://localhost:5173](http://localhost:5173)

---

## 📊 System Status

| Component | Type | Status |
|-----------|------|--------|
| Audio Preprocessor | REAL | ✅ ACTIVE |
| Voice Activity Detector | HEURISTIC | ✅ ACTIVE |
| Deepfake Voice Detector | HEURISTIC/AI | ✅ ACTIVE (PARTIAL_AI) |
| Speaker Identity Verifier | HEURISTIC/AI | ✅ ACTIVE (PARTIAL_AI) |
| Acoustic & Prosody Analyzer | HEURISTIC | ✅ ACTIVE |
| Speech-to-Text (Whisper) | REAL_AI | ✅ ACTIVE |
| Social Engineering Detector | HEURISTIC | ✅ ACTIVE |
| Dynamic Risk Engine | REAL_LOGIC | ✅ ACTIVE |
| Prevention Action Engine | REAL_LOGIC | ✅ ACTIVE |
| Secondary Verification Engine | REAL_LOGIC | ✅ ACTIVE |
| Security Incident Manager | REAL_LOGIC | ✅ ACTIVE |
| SHA-256 Hash-Chain Audit | REAL_CRYPTO | ✅ ACTIVE |
| Solidity AuditTrail Contract | REAL_CONTRACT | ✅ ACTIVE |
| React Security Dashboard | REAL_FRONTEND | ✅ ACTIVE |

> **Backend Tests**: 8/8 PASSED ✅ | **Frontend Build**: Clean Vite Build ✅

---

## 🧪 Running Tests

`ash
# Backend tests
cd voiceguard/backend
pytest tests/ -v
`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check & system status |
| POST | /api/v1/auth/login | JWT authentication |
| POST | /api/v1/voice/analyze | Analyze audio for deepfake/impersonation |
| GET | /api/v1/calls | List monitored calls |
| GET | /api/v1/incidents | List security incidents |
| GET | /api/v1/audit | View blockchain audit trail |
| GET | /api/v1/dashboard | Dashboard statistics |
| WS | /ws/calls/{session_id}/stream | Real-time audio stream WebSocket |

Full interactive docs: http://localhost:8000/docs

---

## 👥 Team

**Team VoiceGuard** — Smart India Hackathon 2026

---

## 📄 License

This project is developed for **Smart India Hackathon 2026** under the problem statement **SIH26104** by the **AICTE Cyber Security Cell**.

---

<p align="center">
  Built with ❤️ for a safer digital India 🇮🇳
</p>
