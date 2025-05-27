from fastapi import APIRouter, HTTPException, status, Depends
from remitai.backend.api.v1.schemas.auth_schemas import (
    RequestOTPRequest,
    RequestOTPResponse,
    VerifyOTPRequest,
    VerifyOTPResponse
)
from remitai.backend.services.two_factor_auth_service import TwoFactorAuthService

router = APIRouter()

# Dependency for TwoFactorAuthService
# This ensures a single instance or a new instance per request as configured
# For simplicity, creating a new instance each time here.
# In a larger app, you might use FastAPI's dependency injection system more elaborately.
def get_2fa_service():
    return TwoFactorAuthService()

@router.post("/request-otp", response_model=RequestOTPResponse)
async def request_otp_endpoint(
    request_data: RequestOTPRequest,
    service: TwoFactorAuthService = Depends(get_2fa_service)
):
    """Endpoint to request an OTP for 2FA."""
    success, message = service.request_otp(
        user_id=request_data.user_id,
        delivery_method=request_data.method,
        phone_number=request_data.phone_number
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return RequestOTPResponse(success=True, message=message)

@router.post("/verify-otp", response_model=VerifyOTPResponse)
async def verify_otp_endpoint(
    request_data: VerifyOTPRequest,
    service: TwoFactorAuthService = Depends(get_2fa_service)
):
    """Endpoint to verify an OTP for 2FA."""
    success, message = service.verify_otp(
        user_id=request_data.user_id,
        otp_code=request_data.otp_code
    )
    if not success:
        # Distinguish between invalid OTP and other errors if necessary
        if "Invalid OTP" in message or "expired" in message or "Too many failed" in message or "No OTP request found" in message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during OTP verification."
            )
    
    # Mock token generation on successful verification
    mock_token = f"mock_auth_token_for_{request_data.user_id}"
    return VerifyOTPResponse(success=True, message=message, token=mock_token)


@router.get("/auth/test") # Original test route, can be kept or removed
async def test_auth():
    return {"message": "Auth endpoint test successful - new version"}

# TODO: Implement actual registration and login endpoints with password hashing, JWT, etc.
# For now, these are placeholders if needed by frontend mock flows.
@router.post("/register")
async def register_user():
    # Mock implementation
    # In a real app: validate input, hash password, store user in DB
    return {"message": "User registration endpoint (mock)", "user_id": "mock_user_123"}

@router.post("/login")
async def login_user():
    # Mock implementation
    # In a real app: validate credentials, issue JWT token
    return {"message": "User login endpoint (mock)", "token": "mock_jwt_token_xyz"}

