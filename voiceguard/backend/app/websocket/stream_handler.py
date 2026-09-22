import base64
import json
import logging
import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import CallSession, AudioSegment, AnalysisResult, VoiceProfile
from app.schemas.schemas import SignalScores, WSRiskUpdate
from ai.audio.preprocessor import AudioPreprocessor
from ai.audio.vad import VoiceActivityDetector
from ai.models.deepfake_detector import DeepfakeDetector
from ai.models.speaker_verifier import SpeakerVerifier
from ai.models.acoustic_analyzer import AcousticAnalyzer
from speech_intelligence.transcriber import SpeechTranscriber
from speech_intelligence.social_engineering import SocialEngineeringDetector
from risk_engine.engine import DynamicRiskEngine
from prevention.engine import PreventionEngine
from incidents.manager import IncidentManager
from blockchain.audit_chain import HashChainAuditLogger

logger = logging.getLogger("VoiceGuard.WebSocketStream")

router = APIRouter(tags=["Real-Time Audio Stream"])

preprocessor = AudioPreprocessor()
vad = VoiceActivityDetector()
deepfake_detector = DeepfakeDetector()
speaker_verifier = SpeakerVerifier()
acoustic_analyzer = AcousticAnalyzer()
transcriber = SpeechTranscriber()
social_engineering_detector = SocialEngineeringDetector()
risk_engine = DynamicRiskEngine()
prevention_engine = PreventionEngine()
incident_manager = IncidentManager()
audit_logger = HashChainAuditLogger()

@router.websocket("/ws/calls/{session_id}/stream")
async def websocket_call_stream(websocket: WebSocket, session_id: str):
    await websocket.accept()
    logger.info(f"WebSocket connection opened for call session {session_id}")

    db: Session = SessionLocal()
    chunk_index = 0
    accumulated_transcript = ""

    call_session = db.query(CallSession).filter(CallSession.id == session_id).first()
    expected_speaker_id = call_session.expected_speaker_id if call_session else None
    
    target_embedding_json = None
    if expected_speaker_id:
        profile = db.query(VoiceProfile).filter(VoiceProfile.speaker_id == expected_speaker_id).first()
        if profile:
            target_embedding_json = profile.embedding_json

    try:
        while True:
            raw_message = await websocket.receive_text()
            try:
                data = json.loads(raw_message)
            except Exception:
                continue

            event_type = data.get("event", "audio_chunk")
            if event_type == "ping":
                await websocket.send_json({"event": "pong"})
                continue
            elif event_type == "end_call":
                logger.info(f"Client requested end_call for session {session_id}")
                break

            audio_b64 = data.get("audio_base64")
            if not audio_b64:
                continue

            try:
                audio_bytes = base64.b64decode(audio_b64)
            except Exception as e:
                logger.warning(f"Invalid base64 audio payload: {e}")
                continue

            chunk_index += 1

            # 1. Audio Preprocessing
            audio_data, sr = preprocessor.load_audio_bytes(audio_bytes)

            # 2. VAD Check
            if not vad.is_speech(audio_data):
                # Silence frame, send current session status without escalating risk
                await websocket.send_json({
                    "event": "risk_update",
                    "session_id": session_id,
                    "chunk_index": chunk_index,
                    "transcript": accumulated_transcript,
                    "risk_score": call_session.current_risk_score if call_session else 0.0,
                    "risk_level": call_session.current_risk_level if call_session else "LOW",
                    "confidence": 0.90,
                    "signals": {
                        "deepfake_prob": 0.05,
                        "speaker_similarity": 0.95,
                        "acoustic_anomaly": 0.05,
                        "prosody_anomaly": 0.05,
                        "social_engineering_score": 0.0,
                        "transaction_risk": 0.0,
                        "context_risk": 0.0
                    },
                    "recommended_action": "CONTINUE_MONITORING",
                    "timestamp": datetime.datetime.utcnow().isoformat()
                })
                continue

            # 3. Deepfake Detection
            deepfake_prob, df_conf, _ = deepfake_detector.predict(audio_data)

            # 4. Speaker Verification
            speaker_similarity = 1.0
            if target_embedding_json:
                sim, is_match, _ = speaker_verifier.verify_speaker(audio_data, target_embedding_json)
                speaker_similarity = sim

            # 5. Acoustic Prosody
            acoustic_anomaly, prosody_anomaly, _ = acoustic_analyzer.analyze_acoustic_prosody(audio_data)

            # 6. Speech-to-Text & Social Engineering
            chunk_transcript, lang, _ = transcriber.transcribe(audio_data)
            if chunk_transcript:
                accumulated_transcript += " " + chunk_transcript

            se_score, intents, indicators, se_reasons = social_engineering_detector.analyze_transcript(accumulated_transcript)

            # 7. Assemble Signals
            signals = SignalScores(
                deepfake_prob=round(deepfake_prob, 3),
                speaker_similarity=round(speaker_similarity, 3),
                acoustic_anomaly=round(acoustic_anomaly, 3),
                prosody_anomaly=round(prosody_anomaly, 3),
                social_engineering_score=round(se_score, 1),
                transaction_risk=75.0 if "FINANCIAL_TRANSACTION" in intents else 0.0,
                context_risk=20.0
            )

            # 8. Dynamic Risk Engine
            risk_res = risk_engine.calculate_risk(
                signals=signals,
                detected_intents=intents,
                risk_indicators=indicators,
                previous_reasons=se_reasons
            )

            # 9. Prevention Workflow Execution
            prevention_res = prevention_engine.process_risk_action(db, session_id, risk_res)

            # 10. Incident Logging if needed
            if risk_res.risk_level in ["HIGH", "CRITICAL"]:
                incident_manager.create_incident_from_risk(db, session_id, risk_res, accumulated_transcript)

            # 11. Hash-Chain Audit Logging for critical events
            if risk_res.risk_level == "CRITICAL" or chunk_index % 10 == 0:
                audit_logger.log_event(
                    db=db,
                    event_type="STREAM_RISK_EVALUATED",
                    payload={
                        "session_id": session_id,
                        "chunk_index": chunk_index,
                        "risk_score": risk_res.risk_score,
                        "risk_level": risk_res.risk_level,
                        "deepfake_prob": deepfake_prob,
                        "speaker_similarity": speaker_similarity
                    },
                    session_id=session_id
                )

            # 12. Send Real-Time Update to WebSocket Client
            update_payload = WSRiskUpdate(
                session_id=session_id,
                chunk_index=chunk_index,
                transcript=accumulated_transcript.strip(),
                risk_score=risk_res.risk_score,
                risk_level=risk_res.risk_level,
                confidence=risk_res.confidence,
                signals=signals,
                recommended_action=risk_res.recommended_action,
                timestamp=datetime.datetime.utcnow().isoformat()
            )

            await websocket.send_text(update_payload.json())

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected for session {session_id}")
    finally:
        db.close()
