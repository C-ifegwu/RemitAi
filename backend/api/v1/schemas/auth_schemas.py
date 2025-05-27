from pydantic import BaseModel, Field
from typing import Literal, Optional

class RequestOTPRequest(BaseModel):
    user_id: str = Field(..., example="user_test_123")
    phone_number: str = Field(..., example="+15551234567")
    method: Literal["sms", "whatsapp"] = Field(..., example="sms")

class RequestOTPResponse(BaseModel):
    success: bool
    message: str

class VerifyOTPRequest(BaseModel):
    user_id: str = Field(..., example="user_test_123")
    otp_code: str = Field(..., min_length=6, max_length=6, example="123456")

class VerifyOTPResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None # Mock token

