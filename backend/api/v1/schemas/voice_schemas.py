from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal

class RegisterVoiceRequest(BaseModel):
    user_id: str = Field(..., example="user_voice_001")
    audio_sample_paths: List[str] = Field(..., min_items=1, example=["/path/to/audio1.wav", "/path/to/audio2.wav"])

class RegisterVoiceResponse(BaseModel):
    success: bool
    voice_id: Optional[str] = None
    message: str
    enrollment_details: Optional[Dict[str, Any]] = None

class VerifyVoiceRequest(BaseModel):
    user_id: str = Field(..., example="user_voice_001")
    audio_sample_path: str = Field(..., example="/path/to/verify_audio.wav")
    attempt_liveness_check: bool = Field(True, example=True)

class VerifyVoiceResponse(BaseModel):
    success: bool
    verified: bool
    message: str
    match_score: Optional[float] = None
    verification_token: Optional[str] = None  # Token that can be used for subsequent operations
