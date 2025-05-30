from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..schemas.vault_schemas import VaultCreate, VaultStatusResponse, VaultWithdrawalRequest, VaultWithdrawalResponse
from ....services.vault_service import vault_service
from ..dependencies import get_current_user_id

router = APIRouter(prefix="/vault", tags=["vault"])

@router.post("/create", response_model=VaultStatusResponse, status_code=status.HTTP_201_CREATED)
async def create_vault(
    vault_data: VaultCreate,
    user_id: str = Depends(get_current_user_id)
):
    """
    Create a new vault to save local currency converted to USDC.
    """
    vault = vault_service.create_vault(user_id, vault_data)
    if not vault:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create vault. Unsupported currency or invalid data."
        )
    return vault_service.get_vault_status(user_id, vault.id)

@router.get("/list", response_model=List[VaultStatusResponse])
async def list_vaults(
    user_id: str = Depends(get_current_user_id)
):
    """
    List all vaults for the current user.
    """
    return vault_service.list_user_vaults(user_id)

@router.get("/{vault_id}", response_model=VaultStatusResponse)
async def get_vault_status(
    vault_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """
    Get the status of a specific vault.
    """
    status = vault_service.get_vault_status(user_id, vault_id)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vault not found"
        )
    return status

@router.post("/withdraw", response_model=VaultWithdrawalResponse)
async def withdraw_vault(
    withdrawal_request: VaultWithdrawalRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Withdraw funds from an unlocked vault.
    """
    result = vault_service.withdraw_vault(user_id, withdrawal_request.vault_id)
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    return VaultWithdrawalResponse(
        message=result["message"],
        vault_id=result["vault_id"],
        withdrawn_usdc_amount=result["withdrawn_usdc_amount"],
        mock_final_local_amount=result["mock_final_local_amount"],
        status=result["status"]
    )
