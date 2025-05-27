from fastapi import APIRouter, HTTPException, status, Depends
from remitai.backend.api.v1.schemas.wallet_schemas import (
    GeneratePhraseResponse,
    ConfirmSavedRequest,
    ConfirmSavedResponse,
    LinkBiometricRequest,
    LinkBiometricResponse,
    RecoverPassphraseRequest,
    RecoverPassphraseResponse,
    RecoverBiometricRequest,
    RecoverBiometricResponse
)
from remitai.backend.services.smart_wallet_backup_service import SmartWalletBackupService
from remitai.backend.services.voice_biometrics_service import VoiceBiometricService

router = APIRouter()

# Dependencies for services
def get_wallet_backup_service():
    # In a real app, we would inject the voice biometric service here
    voice_service = VoiceBiometricService()
    return SmartWalletBackupService(voice_biometric_service_instance=voice_service)

@router.post("/backup/generate-phrase", response_model=GeneratePhraseResponse)
async def generate_phrase_endpoint(
    service: SmartWalletBackupService = Depends(get_wallet_backup_service)
):
    """Endpoint to generate a recovery phrase (mnemonic) for wallet backup."""
    try:
        # In a real non-custodial wallet, this would typically be done client-side
        # For this mock, we generate it server-side
        mnemonic_words = service.generate_mock_mnemonic()
        return GeneratePhraseResponse(
            success=True,
            mnemonic_words=mnemonic_words,
            message="Recovery phrase generated successfully. Store it securely!"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recovery phrase: {str(e)}"
        )

@router.post("/backup/confirm-saved", response_model=ConfirmSavedResponse)
async def confirm_saved_endpoint(
    request_data: ConfirmSavedRequest,
    service: SmartWalletBackupService = Depends(get_wallet_backup_service)
):
    """Endpoint to confirm that the user has saved their recovery phrase."""
    success, message = service.user_confirms_passphrase_saved(request_data.user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return ConfirmSavedResponse(success=success, message=message)

@router.post("/backup/link-biometric", response_model=LinkBiometricResponse)
async def link_biometric_endpoint(
    request_data: LinkBiometricRequest,
    service: SmartWalletBackupService = Depends(get_wallet_backup_service)
):
    """Endpoint to link voice biometric for assisted recovery."""
    success, message = service.setup_biometric_assisted_recovery_mock(
        user_id=request_data.user_id,
        voice_print_id=request_data.voice_print_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return LinkBiometricResponse(success=success, message=message)

@router.post("/recover/passphrase", response_model=RecoverPassphraseResponse)
async def recover_with_passphrase_endpoint(
    request_data: RecoverPassphraseRequest,
    service: SmartWalletBackupService = Depends(get_wallet_backup_service)
):
    """Endpoint to recover wallet using passphrase."""
    success, message = service.recover_wallet_with_passphrase_mock(
        user_id=request_data.user_id,
        provided_passphrase_words=request_data.passphrase_words
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return RecoverPassphraseResponse(success=success, message=message)

@router.post("/recover/biometric", response_model=RecoverBiometricResponse)
async def recover_with_biometric_endpoint(
    request_data: RecoverBiometricRequest,
    service: SmartWalletBackupService = Depends(get_wallet_backup_service)
):
    """Endpoint to recover wallet using biometric (voice) verification."""
    success, message = service.recover_wallet_with_biometric_mock(
        user_id=request_data.user_id,
        voice_verification_token=request_data.voice_verification_token
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return RecoverBiometricResponse(success=success, message=message)

@router.get("/wallet/test") # Original test route
async def test_wallet():
    return {"message": "Wallet endpoint test successful - new version"}
