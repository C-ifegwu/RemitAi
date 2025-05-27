import os
import hashlib
import random

# This is a mock service. In a real non-custodial wallet, private keys/seeds
# would be derived from mnemonics and managed on the client-side.
# The backend would NOT store passphrases or private keys.

# Mock database for user backup status (e.g., if they've acknowledged backup)
# and potentially for storing an *encrypted* representation of a key if we were
# to simulate a more complex biometric recovery (out of scope for simple mock).
MOCK_USER_BACKUP_DB = {}

# Example wordlist for mnemonic generation (very simplified)
WORDLIST = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
    "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry",
    "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yuzu", "zucchini"
]

class SmartWalletBackupService:

    def __init__(self, voice_biometric_service_instance=None):
        """Initialize with an optional voice biometric service instance for integration."""
        self.voice_biometric_service = voice_biometric_service_instance
        # In a real app, this service would primarily guide the client-side operations
        # and potentially store metadata like backup_configured_date, but not secrets.

    def generate_mock_mnemonic(self, word_count: int = 12) -> list[str]:
        """Generates a mock mnemonic phrase.
        In a real wallet, this uses a standard like BIP-39.
        """
        if word_count not in [12, 24]:
            # BIP-39 typically uses 12 or 24 words.
            print("Warning: Standard mnemonic lengths are 12 or 24 words.")
        return random.sample(WORDLIST, k=min(word_count, len(WORDLIST)))

    def user_confirms_passphrase_saved(self, user_id: str) -> tuple[bool, str]:
        """Simulates the user confirming they have securely saved their passphrase.
        The backend only records that the user has completed this step.
        """
        MOCK_USER_BACKUP_DB[user_id] = {
            "passphrase_backup_confirmed": True,
            "biometric_linked": False,
            "mock_encrypted_seed_for_biometric_recovery": None # Example placeholder
        }
        print(f"[BACKUP_SERVICE] User {user_id} confirmed passphrase saved. Emphasize: User is solely responsible for the passphrase.")
        return True, "Passphrase backup process acknowledged. Store your passphrase securely!"

    def recover_wallet_with_passphrase_mock(self, user_id: str, provided_passphrase_words: list[str]) -> tuple[bool, str]:
        """Mocks wallet recovery using a passphrase.
        In a real scenario, this would involve client-side cryptographic operations
        to re-derive keys from the mnemonic. The backend would not see the passphrase.
        For this mock, we just check if the user *claims* to have a passphrase.
        """
        print(f"[BACKUP_SERVICE] Attempting mock recovery for user {user_id} with provided passphrase.")
        # Simulate a check. In a real app, the client derives keys and tries to access the wallet.
        # The backend might not even be involved directly in this step for a true non-custodial wallet.
        if not provided_passphrase_words or len(provided_passphrase_words) < 12:
            return False, "Invalid passphrase provided for recovery (mock check)."
        
        # Simulate successful derivation/unlock
        print(f"[BACKUP_SERVICE] Mock recovery successful for {user_id}. Client would now have access.")
        return True, "Wallet recovery with passphrase successful (mock)."

    def setup_biometric_assisted_recovery_mock(self, user_id: str, voice_print_id: str) -> tuple[bool, str]:
        """Simulates setting up biometric (voice) assisted recovery.
        This is highly conceptual for a non-custodial wallet.
        One approach could be that the user encrypts their seed/mnemonic with a key derived
        from their voice biometric (or the voice biometric unlocks a key that encrypts the seed).
        The encrypted seed could be stored by the user or (less ideally) on the backend.
        For this mock, we just link the voice_print_id.
        """
        if not self.voice_biometric_service:
            return False, "Voice biometric service not available for linking."
        
        # Assume voice_print_id is valid and registered with the voice biometric service
        # In a real scenario, the client would handle encryption of the seed using biometrics.
        # Backend only stores that this link is active.
        if user_id not in MOCK_USER_BACKUP_DB or not MOCK_USER_BACKUP_DB[user_id].get("passphrase_backup_confirmed"):
            return False, "Passphrase backup must be confirmed before setting up biometric recovery."

        # Mock: Simulate encrypting a (non-existent) seed with a key derived from voice_print_id
        # and storing this mock encrypted blob. The actual seed is NEVER on the backend.
        mock_seed = "THIS_IS_A_MOCK_SEED_FOR_USER_" + user_id
        mock_encrypted_blob = hashlib.sha256((mock_seed + voice_print_id).encode()).hexdigest()
        
        MOCK_USER_BACKUP_DB[user_id]["biometric_linked"] = True
        MOCK_USER_BACKUP_DB[user_id]["linked_voice_print_id"] = voice_print_id
        MOCK_USER_BACKUP_DB[user_id]["mock_encrypted_seed_for_biometric_recovery"] = mock_encrypted_blob

        print(f"[BACKUP_SERVICE] Biometric (voice print ID: {voice_print_id}) linked for user {user_id} for assisted recovery (mock).")
        return True, "Biometric assisted recovery setup successful (mock)."

    def recover_wallet_with_biometric_mock(self, user_id: str, voice_verification_token: str) -> tuple[bool, str]:
        """Simulates wallet recovery using biometric (voice) verification.
        The voice_verification_token implies successful voice auth.
        The client would then use this to decrypt the locally or backend-retrieved encrypted seed.
        """
        if not self.voice_biometric_service:
            return False, "Voice biometric service not available for verification."

        user_data = MOCK_USER_BACKUP_DB.get(user_id)
        if not user_data or not user_data.get("biometric_linked"):
            return False, "Biometric assisted recovery not set up for this user."

        # Mock: Assume voice_verification_token is a result of successful voice auth
        # In a real app, this token might be used to get a decryption key for the seed.
        # Here, we just check if the linked voice_print_id (conceptually part of the token) matches.
        # This is a very simplified mock.
        print(f"[BACKUP_SERVICE] Attempting biometric recovery for user {user_id} with token {voice_verification_token}.") 
        # Let's assume the token contains or allows retrieval of the original voice_print_id
        # For the mock, we don't have the voice_biometric_service to validate the token, so we assume it's valid.
        
        mock_encrypted_seed = user_data.get("mock_encrypted_seed_for_biometric_recovery")
        if not mock_encrypted_seed:
            return False, "No encrypted seed found for biometric recovery (mock error)."

        # Simulate decryption and recovery
        print(f"[BACKUP_SERVICE] Biometric verification successful (mock). Client would decrypt seed ({mock_encrypted_seed}) and recover wallet.")
        return True, "Wallet recovery with biometric assistance successful (mock)."

# Example Usage (for testing - requires a mock voice biometric service instance)
if __name__ == "__main__":
    # Mock VoiceBiometricService for testing
    class MockVoiceBiometricService:
        def verify_voice_print(self, user_id, voice_sample_path):
            print(f"[MOCK_VOICE_SVC] Verifying voice for {user_id} (mock)")
            return True, "mock_voice_verification_token_123"
        def register_voice_print(self, user_id, voice_sample_path):
            print(f"[MOCK_VOICE_SVC] Registering voice for {user_id} (mock)")
            return True, "mock_voice_print_id_abc"

    mock_voice_svc = MockVoiceBiometricService()
    backup_service = SmartWalletBackupService(voice_biometric_service_instance=mock_voice_svc)
    user_id_1 = "user_backup_test_001"

    print("--- Testing Passphrase Backup ---")
    mnemonic = backup_service.generate_mock_mnemonic()
    print(f"Generated Mnemonic (user must save this!): {' '.join(mnemonic)}")
    success, message = backup_service.user_confirms_passphrase_saved(user_id_1)
    print(f"Confirm Save: {success}, {message}")

    print("\n--- Testing Passphrase Recovery (Mock) ---")
    # User provides their saved mnemonic
    success, message = backup_service.recover_wallet_with_passphrase_mock(user_id_1, mnemonic)
    print(f"Recovery with Passphrase: {success}, {message}")
    success, message = backup_service.recover_wallet_with_passphrase_mock(user_id_1, ["wrong", "phrase"])
    print(f"Recovery with incorrect Passphrase: {success}, {message}")

    print("\n--- Testing Biometric Assisted Backup & Recovery (Mock) ---")
    # Assume user has a registered voice print
    mock_voice_print_id = "mock_voice_print_id_for_user1"
    success, message = backup_service.setup_biometric_assisted_recovery_mock(user_id_1, mock_voice_print_id)
    print(f"Setup Biometric Recovery: {success}, {message}")

    if success:
        # Simulate successful voice verification yielding a token
        mock_voice_token = "mock_voice_verification_token_xyz"
        rec_success, rec_message = backup_service.recover_wallet_with_biometric_mock(user_id_1, mock_voice_token)
        print(f"Recovery with Biometric: {rec_success}, {rec_message}")

    # Test case: User without passphrase confirmation trying biometric setup
    user_id_2 = "user_backup_test_002"
    success, message = backup_service.setup_biometric_assisted_recovery_mock(user_id_2, "any_voice_id")
    print(f"\nSetup Biometric Recovery (no passphrase confirm): {success}, {message}")

