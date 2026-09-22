import pytest
import numpy as np
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from ai.audio.preprocessor import AudioPreprocessor
from ai.audio.vad import VoiceActivityDetector
from ai.models.deepfake_detector import DeepfakeDetector
from ai.models.speaker_verifier import SpeakerVerifier
from ai.models.acoustic_analyzer import AcousticAnalyzer
from speech_intelligence.social_engineering import SocialEngineeringDetector
from risk_engine.engine import DynamicRiskEngine
from app.schemas.schemas import SignalScores
from blockchain.audit_chain import HashChainAuditLogger

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_root_status():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["problem_statement"] == "SIH26104"

def test_audio_preprocessor():
    preprocessor = AudioPreprocessor(target_sample_rate=16000)
    # Generate 1 sec 440Hz sine wave
    t = np.linspace(0, 1.0, 16000)
    audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)
    
    snr = preprocessor.calculate_snr(audio)
    assert snr >= 0.0

    chunks = preprocessor.chunk_audio(audio, chunk_dur_sec=0.5, overlap_sec=0.1)
    assert len(chunks) > 1

def test_vad():
    vad = VoiceActivityDetector()
    t = np.linspace(0, 0.1, 1600)
    speech_signal = np.sin(2 * np.pi * 300 * t).astype(np.float32)
    silence = np.zeros(1600, dtype=np.float32)

    assert vad.is_speech(speech_signal) is True
    assert vad.is_speech(silence) is False

def test_deepfake_detector():
    detector = DeepfakeDetector()
    t = np.linspace(0, 1.0, 16000)
    audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)

    prob, conf, classification = detector.predict(audio)
    assert 0.0 <= prob <= 1.0
    assert 0.0 <= conf <= 1.0
    assert classification in ["REAL", "SUSPICIOUS", "SYNTHETIC"]

def test_speaker_verifier():
    verifier = SpeakerVerifier()
    t = np.linspace(0, 1.0, 16000)
    audio_a = np.sin(2 * np.pi * 300 * t).astype(np.float32)
    audio_b = np.sin(2 * np.pi * 300 * t).astype(np.float32)

    emb_a = verifier.extract_embedding(audio_a)
    emb_b = verifier.extract_embedding(audio_b)

    assert len(emb_a) == 192
    assert len(emb_b) == 192

    sim = verifier.compute_similarity(emb_a, emb_b)
    assert sim >= 0.90 # Same signal should be highly similar

def test_social_engineering():
    se_detector = SocialEngineeringDetector()
    transcript = "This is the CEO calling from head office. Transfer rupees 500000 immediately via NEFT and do not tell anyone."
    
    score, intents, indicators, reasons = se_detector.analyze_transcript(transcript)
    assert score >= 70.0
    assert "AUTHORITY" in intents
    assert "URGENCY" in intents
    assert "FINANCIAL_TRANSACTION" in intents
    assert "SECRECY" in intents

def test_dynamic_risk_engine_evidence_rule():
    engine_inst = DynamicRiskEngine()

    # Single high signal (deepfake=0.9, but all others low/zero)
    single_signal = SignalScores(
        deepfake_prob=0.90,
        speaker_similarity=0.95,
        acoustic_anomaly=0.10,
        prosody_anomaly=0.10,
        social_engineering_score=0.0,
        transaction_risk=0.0,
        context_risk=0.0
    )

    res_single = engine_inst.calculate_risk(single_signal)
    # Score is 27.0 (LOW) and capped below CRITICAL (84.0) because only 1 strong signal exists
    assert res_single.risk_score <= 84.0
    assert res_single.risk_level == "LOW"

    # Multi high signals (deepfake=0.90 AND speaker mismatch=0.20 AND social eng=80)
    multi_signals = SignalScores(
        deepfake_prob=0.90,
        speaker_similarity=0.20, # High mismatch
        acoustic_anomaly=0.70,
        prosody_anomaly=0.70,
        social_engineering_score=80.0,
        transaction_risk=80.0,
        context_risk=50.0
    )

    res_multi = engine_inst.calculate_risk(multi_signals)
    # Should reach CRITICAL (>= 85.0) because multiple strong signals exist
    assert res_multi.risk_score >= 85.0
    assert res_multi.risk_level == "CRITICAL"

def test_hash_chain_audit():
    db = SessionLocal()
    audit_logger = HashChainAuditLogger()

    event1 = audit_logger.log_event(db, "TEST_EVENT_1", {"key": "val1"})
    event2 = audit_logger.log_event(db, "TEST_EVENT_2", {"key": "val2"})

    assert event2.previous_hash == event1.event_hash

    verify_res = audit_logger.verify_chain_integrity(db)
    assert verify_res.is_valid is True
    db.close()
