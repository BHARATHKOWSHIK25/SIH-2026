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

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" />
  <img src="https://img.shields.io/badge/Backend%20Tests-8%2F8%20Passing-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Build-Passing-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/PRs-Welcome-blueviolet?style=flat-square" />
</p>

---

## 📌 Problem Statement

Voice impersonation and deepfake audio attacks are an emerging threat in cybersecurity, targeting financial institutions, government agencies, and critical infrastructure. Adversaries clone voices using AI tools to bypass speaker authentication systems, authorize fraudulent transactions, and manipulate personnel over live phone calls.

**VoiceGuard AI** is a real-time, multi-layered defense system that detects, prevents, and audits voice impersonation attacks the moment they occur, before any damage is done.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🎙️ **Real-Time Deepfake Detection** | FFT phase variance and spectral flatness analysis on live audio streams |
| 🧬 **Speaker Identity Verification** | 192-dim MFCC embedding with cosine similarity scoring |
| 🧠 **Social Engineering Detection** | 5-category NLP regex pattern matcher for manipulation tactics |
| ⚡ **Dynamic Risk Engine** | Multi-signal evidence aggregation with a policy-driven workflow state machine |
| 🔐 **Blockchain Audit Trail** | SHA-256 hash-chain ledger anchored to Ethereum via `AuditTrail.sol` |
| 📊 **Live Security Dashboard** | React 18 + WebSocket real-time monitoring UI |
| 🔔 **Automated Prevention Actions** | Out-of-band OTP challenge, call flagging, and incident escalation |
| 🗣️ **Speech-to-Text** | faster-whisper INT8 transcription for forensic logging |

---

## 🏗️ Architecture Overview

```
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
```

---

## 📁 Project Structure

```
SIH-2026/
└── voiceguard/
    ├── ai/                          # AI & ML models
    │   ├── audio/                   # Audio preprocessor & VAD
    │   ├── models/                  # Deepfake detector, speaker verifier, acoustic analyzer
    │   └── fusion/                  # Authenticity fusion engine
    ├── backend/                     # FastAPI backend
    │   ├── app/
    │   │   ├── api/v1/              # REST endpoints (auth, calls, voice, speaker, incidents, audit)
    │   │   ├── models/               # SQLAlchemy ORM models
    │   │   ├── schemas/              # Pydantic schemas
    │   │   └── websocket/            # Real-time WebSocket stream handler
    │   └── requirements.txt
    ├── blockchain/                  # Blockchain audit layer
    │   ├── audit_chain.py           # SHA-256 hash-chain ledger
    │   └── contracts/AuditTrail.sol # Solidity smart contract
    ├── frontend/                    # React dashboard
    │   └── src/
    │       └── components/
    │           ├── DashboardOverview.tsx
    │           ├── LiveCallMonitor.tsx
    │           ├── VoiceAnalyzer.tsx
    │           ├── AuditInspector.tsx
    │           ├── IncidentHub.tsx
    │           └── SpeakerRegistry.tsx
    ├── speech_intelligence/         # STT & social engineering detector
    ├── risk_engine/                 # Dynamic risk scoring & policies
    ├── incidents/                   # Security incident manager
    ├── prevention/                  # Prevention action engine
    └── verification/                # Secondary verification engine
```

---

## 🤖 AI/ML Pipeline

The end-to-end audio analysis pipeline processes each 2-second audio chunk through the following stages:

1. **Audio Preprocessor** — 16 kHz linear resampling and SNR calculation
2. **Voice Activity Detector (VAD)** — RMS energy and zero-crossing-rate thresholding
3. **Deepfake Voice Detector** — FFT phase variance and spectral flatness heuristics
4. **Speaker Identity Verifier** — 192-dim MFCC embedding with cosine similarity
5. **Acoustic & Prosody Analyzer** — Autocorrelation F0 (pitch), shimmer, and spectral tilt
6. **Speech-to-Text** — faster-whisper INT8, with an acoustic STT fallback
7. **Social Engineering Detector** — 5-category regex NLP pattern matcher
8. **Risk Engine** — Multi-signal evidence aggregation and confidence scoring
9. **Prevention Engine** — Policy state machine (alert → challenge → block)

> ⚡ **Total end-to-end pipeline latency: ~588 ms per 2-second audio chunk**

---

## 🔗 Blockchain Audit

Every security event is cryptographically logged in a SHA-256 hash chain and anchored on-chain:

- **`blockchain/audit_chain.py`** — Maintains a tamper-evident hash-chain ledger of all events
- **`AuditTrail.sol`** — Ethereum-compatible Solidity contract that anchors Merkle-root batch hashes on-chain for immutable, third-party-verifiable audit trails

---

## 🖥️ Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
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
|---|---|---|
| React | 18.2 | UI framework |
| TypeScript | 5.2 | Type-safe development |
| Vite | 5.1 | Build tool & dev server |
| TailwindCSS | 3.4 | Utility-first styling |
| Recharts | 2.12 | Real-time data visualization |
| Lucide React | 0.330 | Icon library |

### Infrastructure
| Technology | Purpose |
|---|---|
| SQLite | Local database for the prototype |
| WebSockets | Real-time audio stream processing |
| Solidity 0.8.20 | Ethereum smart contract |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### 🔧 Backend Setup

```bash
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
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 🎨 Frontend Setup

```bash
# Navigate to frontend
cd voiceguard/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Dashboard available at: [http://localhost:5173](http://localhost:5173)

---

## 📊 System Status

| Component | Type | Status |
|---|---|---|
| Audio Preprocessor | REAL | ✅ Active |
| Voice Activity Detector | HEURISTIC | ✅ Active |
| Deepfake Voice Detector | HEURISTIC/AI | ✅ Active (Partial AI) |
| Speaker Identity Verifier | HEURISTIC/AI | ✅ Active (Partial AI) |
| Acoustic & Prosody Analyzer | HEURISTIC | ✅ Active |
| Speech-to-Text (Whisper) | REAL_AI | ✅ Active |
| Social Engineering Detector | HEURISTIC | ✅ Active |
| Dynamic Risk Engine | REAL_LOGIC | ✅ Active |
| Prevention Action Engine | REAL_LOGIC | ✅ Active |
| Secondary Verification Engine | REAL_LOGIC | ✅ Active |
| Security Incident Manager | REAL_LOGIC | ✅ Active |
| SHA-256 Hash-Chain Audit | REAL_CRYPTO | ✅ Active |
| Solidity AuditTrail Contract | REAL_CONTRACT | ✅ Active |
| React Security Dashboard | REAL_FRONTEND | ✅ Active |

> **Backend tests:** 8/8 passed ✅ &nbsp;|&nbsp; **Frontend build:** Clean Vite build ✅

---

## 🧪 Running Tests

```bash
# Backend tests
cd voiceguard/backend
pytest tests/ -v
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check & system status |
| POST | `/api/v1/auth/login` | JWT authentication |
| POST | `/api/v1/voice/analyze` | Analyze audio for deepfake/impersonation |
| GET | `/api/v1/calls` | List monitored calls |
| GET | `/api/v1/incidents` | List security incidents |
| GET | `/api/v1/audit` | View blockchain audit trail |
| GET | `/api/v1/dashboard` | Dashboard statistics |
| WS | `/ws/calls/{session_id}/stream` | Real-time audio stream WebSocket |

Full interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🗺️ Roadmap

- [ ] Replace heuristic deepfake/speaker modules with fully trained deep-learning models
- [ ] Add multi-language support for social engineering detection
- [ ] Deploy smart contract to a public testnet
- [ ] Add role-based access control (RBAC) for the dashboard

---

## 🤝 Contributing

Contributions are welcome. Please open an issue to discuss what you'd like to change before submitting a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a pull request

---

## 👥 Team

**Team VoiceGuard** — Smart India Hackathon 2026

---

## 📄 License

This project is developed for **Smart India Hackathon 2026** under problem statement **SIH26104**, issued by the **AICTE Cyber Security Cell**.

---
