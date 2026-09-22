import json
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import VoiceProfile
from app.schemas.schemas import VoiceProfileResponse, SpeakerVerifyResponse
from ai.audio.preprocessor import AudioPreprocessor
from ai.models.speaker_verifier import SpeakerVerifier
from blockchain.audit_chain import HashChainAuditLogger

router = APIRouter(prefix="/speaker", tags=["Speaker Verification"])

preprocessor = AudioPreprocessor()
speaker_verifier = SpeakerVerifier()
audit_logger = HashChainAuditLogger()

@router.post("/register", response_model=VoiceProfileResponse)
async def register_speaker_profile(
    speaker_id: str = Form(...),
    speaker_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    existing = db.query(VoiceProfile).filter(VoiceProfile.speaker_id == speaker_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Speaker ID '{speaker_id}' is already registered.")

    audio_bytes = await file.read()
    audio_data, sr = preprocessor.load_audio_bytes(audio_bytes)
    
    embedding = speaker_verifier.extract_embedding(audio_data)
    emb_json = speaker_verifier.embedding_to_json(embedding)

    profile = VoiceProfile(
        speaker_id=speaker_id,
        speaker_name=speaker_name,
        embedding_json=emb_json,
        audio_sample_path=file.filename,
        is_active=True
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    audit_logger.log_event(
        db=db,
        event_type="SPEAKER_PROFILE_REGISTERED",
        payload={
            "speaker_id": speaker_id,
            "speaker_name": speaker_name,
            "sample_filename": file.filename
        }
    )

    return profile

@router.get("/profiles", response_model=List[VoiceProfileResponse])
def list_speaker_profiles(db: Session = Depends(get_db)):
    return db.query(VoiceProfile).filter(VoiceProfile.is_active == True).all()

@router.post("/verify", response_model=SpeakerVerifyResponse)
async def verify_speaker_identity(
    speaker_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    profile = db.query(VoiceProfile).filter(VoiceProfile.speaker_id == speaker_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Speaker profile '{speaker_id}' not found.")

    audio_bytes = await file.read()
    audio_data, sr = preprocessor.load_audio_bytes(audio_bytes)

    sim, is_match, conf = speaker_verifier.verify_speaker(audio_data, profile.embedding_json)

    return SpeakerVerifyResponse(
        speaker_id=speaker_id,
        similarity_score=round(sim, 3),
        is_match=is_match,
        confidence=round(conf, 2)
    )
