## Security Layer Requirements Analysis

This document outlines the requirements for the Security Layer of the RemitAI project, covering Two-Factor Authentication (2FA), Smart Wallet Backup, and Fraud Detection.

### 1. Two-Factor Authentication (2FA)

**Objective:** Enhance user account security by requiring a second form of verification in addition to the primary authentication method (e.g., password or biometric).

**Requirements:**
- **Method:** Implement 2FA using One-Time Passwords (OTPs).
- **Delivery Channels:** Support OTP delivery via:
    - SMS: Integrate with a mock SMS gateway service for sending OTPs to user's registered phone numbers.
    - WhatsApp OTP: Explore feasibility and implement a mock integration for sending OTPs via WhatsApp. This might involve a mock API endpoint simulating a WhatsApp Business API provider.
- **OTP Generation:** Generate secure, time-sensitive (e.g., 5-10 minute validity) or single-use OTPs.
- **OTP Verification:** Implement backend logic to verify OTPs entered by the user.
- **User Flow:**
    - User initiates a sensitive action (e.g., login, high-value transaction, changing security settings).
    - System prompts for 2FA.
    - User chooses preferred OTP delivery channel (if multiple are configured and enabled).
    - System sends OTP to the chosen channel.
    - User enters the received OTP into the application.
    - System verifies the OTP.
    - Access is granted or denied based on OTP validity.
- **Configuration:** Allow users to enable/disable 2FA and manage their registered phone number for OTP delivery (requires re-authentication).
- **Resend/Fallback:** Provide options to resend OTP if not received, and potentially offer alternative verification methods if OTP delivery fails consistently (though this might be out of scope for mock implementation).
- **Security Considerations:** Protect against OTP brute-force attacks (e.g., rate limiting, account lockout after multiple failed attempts).

### 2. Smart Wallet Backup & Recovery

**Objective:** Provide users with a secure method to back up their smart wallet and recover access in case of device loss or other issues.

**Requirements:**
- **Backup Method 1: Passphrase**
    - **Generation:** Allow users to generate or set a strong, unique passphrase (e.g., a mnemonic phrase of 12-24 words, or a user-defined strong password).
    - **Storage:** The passphrase itself should **not** be stored by the RemitAI backend. The user is responsible for securely storing their passphrase.
    - **Guidance:** Provide clear instructions and warnings to the user about the importance of the passphrase and how to store it safely (e.g., offline, in multiple locations).
    - **Recovery:** Implement a mechanism where the user can re-enter their passphrase to recover access to their wallet. This would typically involve re-deriving wallet keys from the passphrase.
- **Backup Method 2: Optional Biometric Backup (Conceptual for Mock)**
    - **Concept:** Explore how biometrics (e.g., voice print already implemented, or device-native biometrics like fingerprint/face ID) could be *part* of a backup or recovery process. This is more complex for non-custodial wallets.
    - **Mock Implementation:** For a mock, this could involve simulating the use of a previously registered voice print as an *additional factor* or as a way to authorize access to an encrypted seed/key that is stored locally on the user's device (if such a design is chosen). The core idea is to link it to existing biometric features.
    - **Consideration:** True biometric backup for non-custodial wallets often involves social recovery or sharding secrets, which is advanced. For this project, a simpler mock focusing on user experience of *using* biometrics in a recovery flow is sufficient.
- **User Flow (Passphrase):**
    - **Backup:** User navigates to wallet backup settings. System guides them through generating/setting a passphrase. User confirms they have saved it securely.
    - **Recovery:** User indicates they need to recover their wallet. System prompts for the passphrase. User enters passphrase. System attempts to restore wallet access.
- **Security Considerations:** Emphasize that loss of the passphrase means loss of funds for a non-custodial wallet. No backend recovery possible if the user loses their passphrase.

### 3. Fraud Detection

**Objective:** Implement basic fraud detection mechanisms to identify and flag potentially suspicious activities.

**Requirements:**
- **Duplicate Voice Commands:**
    - **Logic:** Detect if the exact same voice command (or highly similar, post-transcription) is issued multiple times in rapid succession from the same user or targeting the same recipient/amount.
    - **Thresholds:** Define reasonable thresholds for what constitutes "rapid succession" and "highly similar."
    - **Action:** Flag suspicious activity. This could involve:
        - Temporarily rate-limiting the user.
        - Requiring additional verification (e.g., re-authentication, 2FA if not already triggered).
        - Notifying the user of potential duplicate transactions.
        - For a mock, log the detection.
- **Spam Commands:**
    - **Logic:** Identify patterns indicative of spam, such as:
        - High frequency of low-value transactions.
        - Transactions to a large number of new, unverified recipients in a short period.
        - Use of known spam-associated keywords or patterns in text/voice inputs (though this is more advanced NLP).
    - **Action:** Similar to duplicate voice commands: rate-limiting, additional verification, user notification, logging.
- **Integration:** Fraud detection logic should be integrated into the transaction processing flow.
- **Configurability (Future):** Ideally, fraud detection rules and thresholds would be configurable, but for mock implementation, hardcoded rules are acceptable.

This analysis will serve as the foundation for designing and implementing the Security Layer features.
