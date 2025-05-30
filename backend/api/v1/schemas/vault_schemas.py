from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class VaultBase(BaseModel):
    local_currency: str = Field(..., example="NGN", description="The user's local currency code (e.g., NGN, KES)")
    local_amount: float = Field(..., gt=0, description="Amount of local currency to deposit")
    lock_duration_days: int = Field(..., gt=0, description="Duration in days to lock the funds")

class VaultCreate(VaultBase):
    pass

class Vault(VaultBase):
    id: str = Field(..., description="Unique identifier for the vault")
    user_id: str # Assuming user identification is handled elsewhere (e.g., via auth token)
    usdc_amount: float = Field(..., description="Equivalent USDC amount locked")
    start_date: datetime = Field(..., description="Timestamp when the vault was created and funds locked")
    end_date: datetime = Field(..., description="Timestamp when the funds unlock")
    status: str = Field(..., example="LOCKED", description="Current status (e.g., LOCKED, UNLOCKED, WITHDRAWN)")
    mock_yield_earned: float = Field(0.0, description="Mock yield earned in USDC")
    mock_withdrawal_local_amount: Optional[float] = Field(None, description="Mock local amount upon withdrawal at current rate")

    class Config:
        orm_mode = True # For potential future ORM integration

class VaultStatusResponse(BaseModel):
    id: str
    local_currency: str
    original_local_amount: float
    usdc_amount: float
    start_date: datetime
    end_date: datetime
    status: str
    mock_yield_earned: float
    is_withdrawable: bool
    mock_current_withdrawal_value_local: Optional[float] = None # Calculated at time of request

class VaultWithdrawalRequest(BaseModel):
    vault_id: str

class VaultWithdrawalResponse(BaseModel):
    message: str
    vault_id: str
    withdrawn_usdc_amount: float
    mock_final_local_amount: float
    status: str

