from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GeneratePhraseResponse(BaseModel):
    success: bool
    mnemonic_words: List[str]
    message: Optional[str] = None

class ConfirmSavedRequest(BaseModel):
    user_id: str = Field(..., example="user_wallet_001")

class ConfirmSavedResponse(BaseModel):
    success: bool
    message: str

class LinkBiometricRequest(BaseModel):
    user_id: str = Field(..., example="user_wallet_001")
    voice_print_id: str = Field(..., example="voice_print_abc123")

class LinkBiometricResponse(BaseModel):
    success: bool
    message: str

class RecoverPassphraseRequest(BaseModel):
    user_id: str = Field(..., example="user_wallet_001")
    passphrase_words: List[str] = Field(..., min_items=12, example=["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "mango", "nectarine"])

class RecoverPassphraseResponse(BaseModel):
    success: bool
    message: str

class RecoverBiometricRequest(BaseModel):
    user_id: str = Field(..., example="user_wallet_001")
    voice_verification_token: str = Field(..., example="voice_verification_token_xyz123")

class RecoverBiometricResponse(BaseModel):
    success: bool
    message: str
