from fastapi import APIRouter, HTTPException, status, Depends
from remitai.backend.api.v1.schemas.voice_schemas import (
    RegisterVoiceRequest,
    RegisterVoiceResponse,
    VerifyVoiceRequest,
    VerifyVoiceResponse
)
from remitai.backend.services.voice_biometrics_service import VoiceBiometricsService
import hashlib
import time

router = APIRouter()

# Dependency for service
def get_voice_biometrics_service():
    return VoiceBiometricsService(use_mock=True)

@router.post("/register", response_model=RegisterVoiceResponse)
async def register_voice_endpoint(
    request_data: RegisterVoiceRequest,
    service: VoiceBiometricsService = Depends(get_voice_biometrics_service)
):
    """Endpoint to register a voice print for a user."""
    result = service.register_voice_id(
        user_identifier=request_data.user_id,
        audio_sample_paths=request_data.audio_sample_paths
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to register voice ID.")
        )
    
    return RegisterVoiceResponse(
        success=True,
        voice_id=result.get("voice_id"),
        message=result.get("message", "Voice ID registered successfully."),
        enrollment_details=result.get("enrollment_details")
    )

@router.post("/verify", response_model=VerifyVoiceResponse)
async def verify_voice_endpoint(
    request_data: VerifyVoiceRequest,
    service: VoiceBiometricsService = Depends(get_voice_biometrics_service)
):
    """Endpoint to verify a user's voice against their registered voice print."""
    result = service.verify_voice(
        user_identifier=request_data.user_id,
        audio_sample_path=request_data.audio_sample_path,
        attempt_liveness_check=request_data.attempt_liveness_check
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Voice verification process failed.")
        )
    
    # Generate a verification token if verification was successful
    verification_token = None
    if result.get("verified"):
        # In a real system, this would be a JWT or similar secure token
        # For this mock, we'll create a simple hash-based token
        token_base = f"{request_data.user_id}_{time.time()}_verified"
        verification_token = hashlib.sha256(token_base.encode()).hexdigest()
    
    return VerifyVoiceResponse(
        success=result.get("success", False),
        verified=result.get("verified", False),
        message=result.get("message", "Voice verification completed."),
        match_score=result.get("match_score"),
        verification_token=verification_token if result.get("verified") else None
    )

@router.get("/voice/test") # Original test route
async def test_voice():
    return {"message": "Voice biometrics endpoint test successful - new version"}
