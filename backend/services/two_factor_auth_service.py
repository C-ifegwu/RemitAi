import random
import string
import time

# Mock database to store OTPs and their expiry times, and user 2FA settings
# In a real application, use a secure database.
MOCK_OTP_DB = {}
# MOCK_USER_2FA_SETTINGS = {
# "user_id_1": {"phone_number": "+1234567890", "whatsapp_enabled": True, "2fa_enabled": True}
# }

OTP_LENGTH = 6
OTP_VALIDITY_DURATION_SECONDS = 300  # 5 minutes

class TwoFactorAuthService:
    def __init__(self):
        self.otp_db = MOCK_OTP_DB

    def _generate_otp(self) -> str:
        """Generates a random OTP."""
        return "".join(random.choices(string.digits, k=OTP_LENGTH))

    def _send_otp_sms(self, phone_number: str, otp: str) -> bool:
        """Mocks sending OTP via SMS."""
        print(f"[MOCK SMS] Sending OTP {otp} to {phone_number}")
        # In a real implementation, integrate with an SMS gateway API
        return True

    def _send_otp_whatsapp(self, phone_number: str, otp: str) -> bool:
        """Mocks sending OTP via WhatsApp."""
        print(f"[MOCK WhatsApp] Sending OTP {otp} to {phone_number} via WhatsApp")
        # In a real implementation, integrate with WhatsApp Business API
        return True

    def request_otp(self, user_id: str, delivery_method: str = "sms", phone_number: str = None) -> tuple[bool, str]:
        """Generates and sends an OTP to the user.

        Args:
            user_id: The unique identifier for the user.
            delivery_method: "sms" or "whatsapp".
            phone_number: The phone number to send the OTP to. Required if not already stored for the user.

        Returns:
            A tuple (success: bool, message: str).
        """
        # In a real app, fetch user's registered phone and 2FA preferences
        # For this mock, we might require phone_number to be passed or have a mock user setting
        if not phone_number:
            # Placeholder: fetch from a hypothetical user settings DB
            # user_settings = MOCK_USER_2FA_SETTINGS.get(user_id)
            # if not user_settings or not user_settings.get("phone_number"):
            #     return False, "Phone number not found for user."
            # phone_number = user_settings["phone_number"]
            return False, "Phone number is required for OTP delivery in this mock."

        otp = self._generate_otp()
        expiry_time = time.time() + OTP_VALIDITY_DURATION_SECONDS

        self.otp_db[user_id] = {
            "otp": otp,
            "expiry_time": expiry_time,
            "verified": False,
            "attempts": 0
        }

        sent = False
        if delivery_method == "sms":
            sent = self._send_otp_sms(phone_number, otp)
        elif delivery_method == "whatsapp":
            sent = self._send_otp_whatsapp(phone_number, otp)
        else:
            return False, "Invalid OTP delivery method."

        if sent:
            return True, f"OTP sent successfully via {delivery_method}."
        else:
            # Clean up OTP if sending failed to prevent misuse
            del self.otp_db[user_id]
            return False, f"Failed to send OTP via {delivery_method}."

    def verify_otp(self, user_id: str, otp_code: str) -> tuple[bool, str]:
        """Verifies the OTP provided by the user.

        Args:
            user_id: The unique identifier for the user.
            otp_code: The OTP code entered by the user.

        Returns:
            A tuple (success: bool, message: str).
        """
        user_otp_data = self.otp_db.get(user_id)

        if not user_otp_data:
            return False, "No OTP request found for this user or OTP expired. Please request a new one."

        if user_otp_data["verified"]:
             return False, "OTP already verified. Please request a new one for a new operation."

        if time.time() > user_otp_data["expiry_time"]:
            del self.otp_db[user_id] # Clean up expired OTP
            return False, "OTP has expired. Please request a new one."

        # Basic brute-force protection (mock)
        if user_otp_data["attempts"] >= 5:
            # In a real app, might lock account temporarily or require captcha
            del self.otp_db[user_id] # Clean up OTP after too many attempts
            return False, "Too many failed OTP attempts. Please request a new one."

        if user_otp_data["otp"] == otp_code:
            user_otp_data["verified"] = True # Mark as verified for single use
            # self.otp_db[user_id]["verified"] = True # Persist if needed for audit, but usually delete after use
            # For single-use OTPs, it's often better to delete them after successful verification.
            # However, for this mock, marking as verified demonstrates state change.
            # To make it strictly single-use, uncomment the del line below.
            # del self.otp_db[user_id]
            return True, "OTP verified successfully."
        else:
            self.otp_db[user_id]["attempts"] += 1
            return False, "Invalid OTP."

# Example Usage (for testing)
if __name__ == "__main__":
    service = TwoFactorAuthService()
    user1_id = "user_test_123"
    user1_phone = "+15551234567"

    print("--- Testing SMS OTP ---")
    success, message = service.request_otp(user1_id, delivery_method="sms", phone_number=user1_phone)
    print(f"Request OTP: {success}, {message}")

    if success:
        # Simulate user receiving and entering OTP
        # In a real scenario, the OTP would be unknown here.
        # For testing, we can peek into the mock DB.
        generated_otp = service.otp_db[user1_id]["otp"]
        print(f"Generated OTP (for testing): {generated_otp}")

        # Test correct OTP
        verify_success, verify_message = service.verify_otp(user1_id, generated_otp)
        print(f"Verify OTP (correct): {verify_success}, {verify_message}")

        # Test incorrect OTP
        verify_success, verify_message = service.verify_otp(user1_id, "000000")
        print(f"Verify OTP (incorrect): {verify_success}, {verify_message}")

        # Test already verified OTP (if not deleted after first verification)
        # This depends on the implementation detail of whether OTP is deleted or just marked.
        # If we mark it as verified and don't delete:
        if service.otp_db.get(user1_id) and service.otp_db[user1_id]["verified"]:
             verify_success, verify_message = service.verify_otp(user1_id, generated_otp)
             print(f"Verify OTP (already verified): {verify_success}, {verify_message}")

    print("\n--- Testing WhatsApp OTP ---")
    user2_id = "user_test_456"
    user2_phone = "+15557654321"
    success, message = service.request_otp(user2_id, delivery_method="whatsapp", phone_number=user2_phone)
    print(f"Request OTP: {success}, {message}")
    if success:
        generated_otp_whatsapp = service.otp_db[user2_id]["otp"]
        verify_success, verify_message = service.verify_otp(user2_id, generated_otp_whatsapp)
        print(f"Verify OTP (WhatsApp, correct): {verify_success}, {verify_message}")

    print("\n--- Testing OTP Expiry (simulated) ---")
    user3_id = "user_test_789"
    user3_phone = "+15550001111"
    success, message = service.request_otp(user3_id, phone_number=user3_phone)
    print(f"Request OTP: {success}, {message}")
    if success:
        generated_otp_expiry = service.otp_db[user3_id]["otp"]
        print(f"Generated OTP (for expiry test): {generated_otp_expiry}")
        # Simulate time passing beyond expiry
        service.otp_db[user3_id]["expiry_time"] = time.time() - 1 # Set expiry to past
        verify_success, verify_message = service.verify_otp(user3_id, generated_otp_expiry)
        print(f"Verify OTP (expired): {verify_success}, {verify_message}")

    print("\n--- Testing Max Attempts ---")
    user4_id = "user_test_101"
    user4_phone = "+15552223333"
    success, message = service.request_otp(user4_id, phone_number=user4_phone)
    print(f"Request OTP: {success}, {message}")
    if success:
        for i in range(6):
            verify_success, verify_message = service.verify_otp(user4_id, f"12345{i}")
            print(f"Verify OTP (attempt {i+1}): {verify_success}, {verify_message}")
            if not verify_success and "Too many failed" in verify_message:
                break

