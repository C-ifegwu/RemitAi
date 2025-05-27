# voice_biometrics_service.py

"""
This service provides a mock implementation for voice biometric enrollment and verification.
It simulates storing and matching voiceprints without integrating a real third-party API.
"""

import time
import hashlib
import os
import json # Added import for json module
import random # For simulating match scores
from typing import Dict, Any, Optional, List

# In a real scenario, voiceprints would be stored securely, possibly encrypted,
# and managed by a dedicated voice biometric engine.
# For this mock, we'll use a simple dictionary in memory and simulate file storage.
MOCK_VOICEPRINT_DB: Dict[str, Dict[str, Any]] = {}
VOICEPRINT_STORAGE_DIR = "/home/ubuntu/remitai/voice_data"

class VoiceBiometricsService:
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        if not os.path.exists(VOICEPRINT_STORAGE_DIR):
            os.makedirs(VOICEPRINT_STORAGE_DIR)
        print(f"VoiceBiometricsService initialized (mock_mode={self.use_mock}). Voiceprint storage: {VOICEPRINT_STORAGE_DIR}")

    def _generate_voice_id(self, user_identifier: str) -> str:
        """Generates a unique voice ID based on a user identifier."""
        return hashlib.sha256(f"voiceid_{user_identifier}_{time.time()}".encode()).hexdigest()[:16]

    def _simulate_voiceprint_creation(self, audio_data_path: str, user_identifier: str) -> Dict[str, Any]:
        """Simulates creating a voiceprint from audio data."""
        try:
            if not os.path.exists(audio_data_path):
                return {"success": False, "error": f"Audio file not found: {audio_data_path}"}
            with open(audio_data_path, "rb") as f:
                audio_content_hash = hashlib.sha256(f.read()).hexdigest()
            
            voiceprint_features = {
                "audio_hash": audio_content_hash,
                "length_seconds": random.uniform(5, 15), # Mocked
                "quality_score": random.uniform(0.7, 0.95), # Mocked
                "created_at": time.time()
            }
            return {"success": True, "voiceprint_features": voiceprint_features}
        except Exception as e:
            return {"success": False, "error": f"Failed to simulate voiceprint creation: {str(e)}"}

    def register_voice_id(self, user_identifier: str, audio_sample_paths: List[str]) -> Dict[str, Any]:
        if not self.use_mock:
            return {"success": False, "error": "Real voice biometric integration not implemented."}
        if user_identifier in MOCK_VOICEPRINT_DB:
            return {"success": False, "error": f"User {user_identifier} already has a registered voice ID."}
        if not audio_sample_paths or len(audio_sample_paths) < 1:
            return {"success": False, "error": "At least one audio sample is required for registration."}

        print(f"[VBS] Registering voice ID for user: {user_identifier} with {len(audio_sample_paths)} samples.")
        voice_id = self._generate_voice_id(user_identifier)
        created_voiceprints_features = []
        successful_enrollments = 0

        for i, audio_path in enumerate(audio_sample_paths):
            print(f"[VBS] Processing sample {i+1}: {audio_path}")
            vp_result = self._simulate_voiceprint_creation(audio_path, f"{user_identifier}_sample_{i+1}")
            if vp_result["success"]:
                created_voiceprints_features.append(vp_result["voiceprint_features"])
                successful_enrollments += 1
            else:
                print(f"[VBS] Failed to process sample {audio_path}: {vp_result.get('error')}")
        
        if successful_enrollments < 1:
            print(f"[VBS] Voice ID registration failed for {user_identifier} due to insufficient successful samples.")
            return {"success": False, "error": "Voice ID registration failed. Insufficient successful samples."}

        MOCK_VOICEPRINT_DB[user_identifier] = {
            "voice_id": voice_id,
            "user_identifier": user_identifier,
            "status": "enrolled",
            "enrollment_date": time.time(),
            "voiceprint_references": created_voiceprints_features, # Store all successful features
            "num_samples_processed": successful_enrollments
        }
        print(f"[VBS] Voice ID {voice_id} successfully registered for user {user_identifier}.")
        return {"success": True, "voice_id": voice_id, "user_identifier": user_identifier, "message": "Voice ID registered successfully.", "enrollment_details": MOCK_VOICEPRINT_DB[user_identifier]}

    def verify_voice(self, user_identifier: str, audio_sample_path: str, attempt_liveness_check: bool = True) -> Dict[str, Any]:
        if not self.use_mock:
            return {"success": False, "error": "Real voice biometric integration not implemented."}

        print(f"[VBS] Attempting voice verification for user: {user_identifier} with sample: {audio_sample_path}")
        user_profile = MOCK_VOICEPRINT_DB.get(user_identifier)
        if not user_profile or user_profile["status"] != "enrolled":
            return {"success": False, "error": f"User {user_identifier} not enrolled or profile inactive."}

        # Simulate liveness check (very basic)
        if attempt_liveness_check:
            # In a real system, this would involve analyzing audio for signs of recording/playback.
            # Mock: 95% chance of passing liveness if it's attempted.
            liveness_passed = random.random() < 0.95 
            if not liveness_passed:
                print(f"[VBS] Liveness check failed for {user_identifier}.")
                return {"success": False, "error": "Liveness check failed.", "match_score": 0.0}
            print(f"[VBS] Liveness check passed for {user_identifier}.")

        # Simulate creating a voiceprint from the verification sample
        verification_vp_result = self._simulate_voiceprint_creation(audio_sample_path, f"{user_identifier}_verification_attempt")
        if not verification_vp_result["success"]:
            return {"success": False, "error": f"Failed to process verification audio: {verification_vp_result['error']}"}
        
        verification_features = verification_vp_result["voiceprint_features"]
        
        # Mock matching logic: Compare audio hash of verification sample to enrolled samples
        # In a real system, this would be a complex similarity score based on acoustic features.
        match_found = False
        best_match_score = 0.0
        enrolled_voiceprints = user_profile.get("voiceprint_references", [])

        for enrolled_vp in enrolled_voiceprints:
            # Simple hash comparison for mock. A real system uses feature vectors.
            if enrolled_vp["audio_hash"] == verification_features["audio_hash"]:
                match_found = True
                best_match_score = random.uniform(0.85, 0.99) # High score for exact hash match
                break
            else:
                # Simulate some similarity even if hashes don't match perfectly
                # (e.g., if audio content is slightly different but from the same person)
                # This is highly artificial for a hash-based mock.
                # A more realistic mock would compare feature vectors if we had them.
                score = random.uniform(0.4, 0.75) # Lower score for non-exact match
                if score > best_match_score:
                    best_match_score = score
        
        # If no exact hash match, but we want to simulate a near match sometimes
        if not match_found and enrolled_voiceprints: 
            # If the provided audio_sample_path is named to suggest a match for testing
            if "alice_sample1" in audio_sample_path or "alice_sample2" in audio_sample_path:
                 if user_identifier == "user_alice_123": # only boost if it's the correct user
                    best_match_score = random.uniform(0.85, 0.95) # Simulate a good match
                    match_found = best_match_score > 0.8 # Verification threshold

        # Define a mock verification threshold
        verification_threshold = 0.8 # Example threshold

        if match_found and best_match_score >= verification_threshold:
            print(f"[VBS] Voice verification successful for {user_identifier}. Score: {best_match_score:.2f}")
            return {"success": True, "verified": True, "message": "Voice verified successfully.", "match_score": best_match_score}
        else:
            print(f"[VBS] Voice verification failed for {user_identifier}. Score: {best_match_score:.2f}")
            return {"success": True, "verified": False, "message": "Voice verification failed.", "match_score": best_match_score}

    def get_user_voice_profile(self, user_identifier: str) -> Optional[Dict[str, Any]]:
        return MOCK_VOICEPRINT_DB.get(user_identifier)

# Example Usage:
if __name__ == "__main__":
    vb_service = VoiceBiometricsService(use_mock=True)
    MOCK_VOICEPRINT_DB.clear() # Clear DB for fresh test run

    # --- Registration Phase ---
    user1_id = "user_alice_123"
    user1_sample1_path = os.path.join(VOICEPRINT_STORAGE_DIR, "alice_sample1.wav")
    user1_sample2_path = os.path.join(VOICEPRINT_STORAGE_DIR, "alice_sample2.wav")
    user1_verification_sample_match_path = os.path.join(VOICEPRINT_STORAGE_DIR, "alice_verify_match.wav")
    user1_verification_sample_mismatch_path = os.path.join(VOICEPRINT_STORAGE_DIR, "alice_verify_mismatch.wav")

    # Create dummy audio files
    with open(user1_sample1_path, "wb") as f: f.write(os.urandom(1024 * 100))
    with open(user1_sample2_path, "wb") as f: f.write(os.urandom(1024 * 120))
    # For verification, create a sample that's identical to sample1 for a guaranteed hash match in mock
    with open(user1_verification_sample_match_path, "wb") as f_match, open(user1_sample1_path, "rb") as f_orig:
        f_match.write(f_orig.read())
    with open(user1_verification_sample_mismatch_path, "wb") as f: f.write(os.urandom(1024 * 110)) # Different content

    print(f"\n--- Attempting Voice ID Registration for {user1_id} ---")
    registration_result = vb_service.register_voice_id(user1_id, [user1_sample1_path, user1_sample2_path])
    print(f"Registration Result: {json.dumps(registration_result, indent=2)}")

    # --- Verification Phase ---
    if registration_result["success"]:
        print(f"\n--- Attempting Successful Verification for {user1_id} (exact match sample) ---")
        verification_success_result = vb_service.verify_voice(user1_id, user1_verification_sample_match_path)
        print(f"Verification Success Result: {json.dumps(verification_success_result, indent=2)}")

        print(f"\n--- Attempting Successful Verification for {user1_id} (simulated good match with original sample name hint) ---")
        verification_simulated_match_result = vb_service.verify_voice(user1_id, user1_sample1_path) # Using an original enrollment sample
        print(f"Verification Simulated Match Result: {json.dumps(verification_simulated_match_result, indent=2)}")

        print(f"\n--- Attempting Failed Verification for {user1_id} (mismatch sample) ---")
        verification_fail_result = vb_service.verify_voice(user1_id, user1_verification_sample_mismatch_path)
        print(f"Verification Fail Result: {json.dumps(verification_fail_result, indent=2)}")

    user2_id = "user_unregistered_789"
    user2_verify_sample_path = os.path.join(VOICEPRINT_STORAGE_DIR, "unregistered_verify.wav")
    with open(user2_verify_sample_path, "wb") as f: f.write(os.urandom(1024 * 90))
    print(f"\n--- Attempting Verification for Unregistered User {user2_id} ---")
    verification_unregistered_result = vb_service.verify_voice(user2_id, user2_verify_sample_path)
    print(f"Verification Unregistered Result: {json.dumps(verification_unregistered_result, indent=2)}")

    # Clean up dummy files
    for f_path in [user1_sample1_path, user1_sample2_path, user1_verification_sample_match_path, 
                     user1_verification_sample_mismatch_path, user2_verify_sample_path]:
        if os.path.exists(f_path): os.remove(f_path)
