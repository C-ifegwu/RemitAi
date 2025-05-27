from fastapi import APIRouter, HTTPException, status, Depends, Path, Body
from typing import Optional
from remitai.backend.api.v1.schemas.transaction_schemas import (
    OnRampInitiateRequest,
    OnRampInitiateResponse,
    TransactionStatusResponse,
    OffRampInitiateRequest,
    OffRampInitiateResponse,
    ConfirmWithdrawalRequest,
    ConfirmWithdrawalResponse,
    PayoutWebhookRequest,
    PayoutWebhookResponse,
    AssessRiskRequest,
    AssessRiskResponse
)
from remitai.backend.services.onramp_service import OnRampService
from remitai.backend.services.offramp_service import OffRampService
from remitai.backend.services.withdrawal_confirmation_service import WithdrawalConfirmationService
from remitai.backend.services.fraud_detection_service import FraudDetectionService

router = APIRouter()

# Mock contract ID for WithdrawalConfirmationService
MOCK_SMART_WALLET_CONTRACT_ID = "CAD0000000000000000000000000000000000000000000000000000000000000"

# Dependencies for services
def get_onramp_service():
    return OnRampService(use_mock=True)

def get_offramp_service():
    return OffRampService(use_mock=True)

def get_withdrawal_confirmation_service():
    # In a real app, contract_id would come from config
    return WithdrawalConfirmationService(smart_wallet_contract_id=MOCK_SMART_WALLET_CONTRACT_ID)

def get_fraud_detection_service():
    return FraudDetectionService()

@router.post("/onramp/initiate", response_model=OnRampInitiateResponse)
async def initiate_onramp_endpoint(
    request_data: OnRampInitiateRequest,
    service: OnRampService = Depends(get_onramp_service)
):
    """Endpoint to initiate an on-ramp (buy USDC) transaction."""
    # Mock recipient address for USDC, in a real app this would be the user's smart wallet
    mock_recipient_usdc_address = f"USER_SMART_WALLET_ADDRESS_FOR_{request_data.user_id}"
    # Mock payment method, could be part of request or selected by user
    mock_payment_method = "Bank Transfer" 

    result = service.initiate_onramp_transaction(
        provider_id=request_data.provider if request_data.provider else service.preferred_provider,
        amount=request_data.fiat_amount,
        currency=request_data.fiat_currency,
        payment_method=mock_payment_method, # This should ideally come from user selection or request
        recipient_address=mock_recipient_usdc_address,
        user_details={"user_id": request_data.user_id} # Mock user details
    )
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    
    return OnRampInitiateResponse(
        success=True,
        transaction_id=result.get("transaction_id"),
        status=result.get("status"),
        details=result
    )

@router.get("/onramp/status/{transaction_id}", response_model=TransactionStatusResponse)
async def get_onramp_status_endpoint(
    transaction_id: str = Path(..., title="The ID of the on-ramp transaction to get status for"),
    service: OnRampService = Depends(get_onramp_service)
):
    """Endpoint to check the status of an on-ramp transaction."""
    result = service.check_transaction_status(transaction_id)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
    return TransactionStatusResponse(
        transaction_id=result.get("transaction_id", transaction_id),
        status=result.get("status", "unknown"),
        details=result
    )

@router.post("/offramp/initiate", response_model=OffRampInitiateResponse)
async def initiate_offramp_endpoint(
    request_data: OffRampInitiateRequest,
    service: OffRampService = Depends(get_offramp_service)
):
    """Endpoint to initiate an off-ramp (sell USDC for fiat) transaction."""
    # Mock sender wallet address (user's smart wallet)
    mock_sender_usdc_address = f"USER_SMART_WALLET_ADDRESS_FOR_{request_data.user_id}"
    # Mock payout method, should ideally come from user selection or request
    mock_payout_method = request_data.recipient_details.get("payout_method", "Bank Transfer")

    result = service.initiate_offramp_transaction(
        provider_id=request_data.provider if request_data.provider else service.preferred_provider,
        usdc_amount=request_data.usdc_amount,
        target_currency=request_data.target_currency,
        payout_method=mock_payout_method,
        payout_details=request_data.recipient_details,
        sender_wallet_address=mock_sender_usdc_address
    )
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
    return OffRampInitiateResponse(
        success=True,
        transaction_id=result.get("transaction_id"),
        status=result.get("status"),
        details=result
    )

@router.get("/offramp/status/{transaction_id}", response_model=TransactionStatusResponse)
async def get_offramp_status_endpoint(
    transaction_id: str = Path(..., title="The ID of the off-ramp transaction to get status for"),
    service: OffRampService = Depends(get_offramp_service)
):
    """Endpoint to check the status of an off-ramp transaction."""
    result = service.check_transaction_status(transaction_id)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["error"])
    return TransactionStatusResponse(
        transaction_id=result.get("transaction_id", transaction_id),
        status=result.get("status", "unknown"),
        details=result
    )

@router.post("/withdrawal/confirm-on-contract", response_model=ConfirmWithdrawalResponse)
async def confirm_withdrawal_on_contract_endpoint(
    request_data: ConfirmWithdrawalRequest, # This should contain offramp_tx_id, user_wallet, usdc_amount
    service: WithdrawalConfirmationService = Depends(get_withdrawal_confirmation_service)
):
    """Endpoint to (mock) trigger USDC lock on smart contract for withdrawal."""
    # In a real flow, usdc_amount and user_wallet_address would be fetched based on transaction_id
    # For this mock, let's assume they are part of the request or a preceding step has set them.
    # This endpoint is simplified; a real one would fetch details from the offramp_service first.
    mock_usdc_amount = 50.0 # Placeholder, should be from offramp tx details
    mock_user_wallet = f"USER_WALLET_FOR_{request_data.user_id}" # Placeholder

    result = service.initiate_usdc_withdrawal_on_contract(
        offramp_transaction_id=request_data.transaction_id,
        user_wallet_address=mock_user_wallet, # This should be the user's actual Soroban wallet address
        usdc_amount=mock_usdc_amount # This should be the actual USDC amount for the transaction
    )
    if not result.get("success"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error", "Failed to lock funds on contract"))
    return ConfirmWithdrawalResponse(success=True, message=result.get("message", "Contract interaction successful."))

@router.post("/webhook/payout-status", response_model=PayoutWebhookResponse)
async def payout_status_webhook_endpoint(
    webhook_data: PayoutWebhookRequest, # Data from the payout provider
    service: WithdrawalConfirmationService = Depends(get_withdrawal_confirmation_service)
):
    """(Mock) Webhook endpoint for fiat payout providers to send status updates."""
    result = service.process_fiat_payout_webhook(webhook_data.model_dump())
    if not result.get("success"):
        # Log critical errors for manual intervention
        if "Manual intervention required" in result.get("error", ""):
            print(f"CRITICAL WEBHOOK ERROR: {result.get('error')} for tx_id: {webhook_data.transaction_id}")
            # In a real app, send alerts here
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error", "Webhook processing failed"))
    return PayoutWebhookResponse(status="acknowledged")

@router.post("/assess-risk", response_model=AssessRiskResponse)
async def assess_transaction_risk_endpoint(
    request_data: AssessRiskRequest,
    service: FraudDetectionService = Depends(get_fraud_detection_service)
):
    """Endpoint to assess the fraud risk of a potential transaction."""
    result = service.assess_transaction_risk(
        user_id=request_data.user_id,
        command_text=request_data.command_text,
        amount=request_data.amount,
        recipient_id=request_data.recipient_id
    )
    return AssessRiskResponse(**result)


@router.get("/transactions/test") # Original test route
async def test_transactions():
    return {"message": "Transactions endpoint test successful - new version"}

