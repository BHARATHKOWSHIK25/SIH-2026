import uuid
import datetime
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import VoiceProfile, CallSession, AudioSegment, AnalysisResult
from app.schemas.schemas import AudioAnalysisResponse, SignalScores, DynamicRiskResponse
from ai.audio.preprocessor import AudioPreprocessor
from ai.models.deepfake_detector import DeepfakeDetector
from ai.models.speaker_verifier import SpeakerVerifier
from ai.models.acoustic_analyzer import AcousticAnalyzer
from ai.fusion.authenticity_fusion import AuthenticityFusionEngine
from speech_intelligence.transcriber import SpeechTranscriber
from speech_intelligence.social_engineering import SocialEngineeringDetector
from risk_engine.engine import DynamicRiskEngine
from prevention.engine import PreventionEngine
from incidents.manager import IncidentManager
from blockchain.audit_chain import HashChainAuditLogger

router = APIRouter(prefix="/voice", tags=["Voice Analysis"])

preprocessor = AudioPreprocessor()
deepfake_detector = DeepfakeDetector()
speaker_verifier = SpeakerVerifier()
acoustic_analyzer = AcousticAnalyzer()
authenticity_fusion = AuthenticityFusionEngine()
transcriber = SpeechTranscriber()
social_engineering_detector = SocialEngineeringDetector()
risk_engine = DynamicRiskEngine()
prevention_engine = PreventionEngine()
incident_manager = IncidentManager()
audit_logger = HashChainAuditLogger()

@router.post("/analyze", response_model=AudioAnalysisResponse)
async def analyze_audio_file(
    file: UploadFile = File(...),
    expected_speaker_id: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty audio file provided.")

    # 1. Preprocess audio
    audio_data, sr = preprocessor.load_audio_bytes(contents)

    # 2. Deepfake detection
    deepfake_prob, df_conf, df_class = deepfake_detector.predict(audio_data)

    # 3. Speaker verification if profile target given
    speaker_similarity = 1.0
    if expected_speaker_id:
        profile = db.query(VoiceProfile).filter(VoiceProfile.speaker_id == expected_speaker_id).first()
        if profile and profile.embedding_json:
            sim, is_match, _ = speaker_verifier.verify_speaker(audio_data, profile.embedding_json)
            speaker_similarity = sim

    # 4. Acoustic & Prosody analysis
    acoustic_anomaly, prosody_anomaly, metrics = acoustic_analyzer.analyze_acoustic_prosody(audio_data)

    # 5. Transcription & Social Engineering
    transcript, lang, _ = transcriber.transcribe(audio_data)
    se_score, intents, indicators, se_reasons = social_engineering_detector.analyze_transcript(transcript)

    # 6. Signals assembly
    signals = SignalScores(
        deepfake_prob=round(deepfake_prob, 3),
        speaker_similarity=round(speaker_similarity, 3),
        acoustic_anomaly=round(acoustic_anomaly, 3),
        prosody_anomaly=round(prosody_anomaly, 3),
        social_engineering_score=round(se_score, 1),
        transaction_risk=75.0 if "FINANCIAL_TRANSACTION" in intents else 0.0,
        context_risk=20.0
    )

    # 7. Dynamic Risk calculation
    risk_res = risk_engine.calculate_risk(
        signals=signals,
        detected_intents=intents,
        risk_indicators=indicators,
        previous_reasons=se_reasons
    )

    # 8. Create session if not provided
    if not session_id:
        session_id = f"CALL-{uuid.uuid4().hex[:8].upper()}"
        call = CallSession(
            id=session_id,
            caller_id="UPLOAD_USER",
            callee_id="SYSTEM",
            expected_speaker_id=expected_speaker_id,
            status="ACTIVE",
            current_risk_score=risk_res.risk_score,
            current_risk_level=risk_res.risk_level,
            peak_risk_score=risk_res.risk_score
        )
        db.add(call)
        db.commit()

    # 9. Audit event log
    audit_logger.log_event(
        db=db,
        event_type="VOICE_ANALYSIS_PERFORMED",
        payload={
            "session_id": session_id,
            "filename": file.filename,
            "risk_score": risk_res.risk_score,
            "risk_level": risk_res.risk_level,
            "deepfake_prob": deepfake_prob,
            "transcript": transcript
        },
        session_id=session_id
    )

    # 10. Incident creation if High/Critical
    if risk_res.risk_level in ["HIGH", "CRITICAL"]:
        incident_manager.create_incident_from_risk(db, session_id, risk_res, transcript)

    return AudioAnalysisResponse(
        segment_id=1,
        chunk_index=0,
        transcript=transcript if transcript else "Audio analyzed successfully.",
        language=lang,
        risk=risk_res
    )
