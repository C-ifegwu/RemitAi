from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal

class OnRampInitiateRequest(BaseModel):
    user_id: str = Field(..., example="user_tx_test_001")
    fiat_amount: float = Field(..., gt=0, example=100.0)
    fiat_currency: str = Field(..., example="KES")
    provider: Optional[str] = Field(None, example="mock_provider_A")

class OnRampInitiateResponse(BaseModel):
    success: bool
    transaction_id: Optional[str] = None
    status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class TransactionStatusResponse(BaseModel):
    transaction_id: str
    status: str
    details: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class OffRampInitiateRequest(BaseModel):
    user_id: str = Field(..., example="user_tx_test_002")
    usdc_amount: float = Field(..., gt=0, example=50.0)
    target_currency: str = Field(..., example="NGN")
    recipient_details: Dict[str, Any] = Field(..., example={"account_number": "0123456789", "bank_code": "058"})
    provider: Optional[str] = Field(None, example="mock_provider_B")

class OffRampInitiateResponse(BaseModel):
    success: bool
    transaction_id: Optional[str] = None
    status: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class ConfirmWithdrawalRequest(BaseModel):
    user_id: str = Field(..., example="user_tx_test_003")
    transaction_id: str = Field(..., example="offramp_tx_123")

class ConfirmWithdrawalResponse(BaseModel):
    success: bool
    message: str

class PayoutWebhookRequest(BaseModel):
    transaction_id: str = Field(..., example="offramp_tx_123")
    status: Literal["completed", "failed", "pending", "processed"] # Added more mock statuses
    provider_data: Optional[Dict[str, Any]] = Field(None, example={"reference": "prov_ref_abc"})

class PayoutWebhookResponse(BaseModel):
    status: str # e.g., "received", "acknowledged"

class AssessRiskRequest(BaseModel):
    user_id: str = Field(..., example="user_risk_test_001")
    command_text: str = Field(..., example="Send 5000 KES to Bob")
    amount: float = Field(..., ge=0, example=5000.0)
    recipient_id: str = Field(..., example="bob_user_id")

class AssessRiskResponse(BaseModel):
    user_id: str
    is_suspicious: bool
    risk_score: int
    reasons: list[str]
    timestamp: float

