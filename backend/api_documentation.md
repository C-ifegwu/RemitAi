# RemitAI Backend API Documentation

## Overview

This document provides comprehensive documentation for the RemitAI backend API, which serves as the foundation for the RemitAI application. The API is built using FastAPI and provides endpoints for authentication, natural language processing, transactions, wallet management, and voice biometrics.

## API Structure

The API follows a modular structure with the following components:

- **Authentication**: User authentication, OTP generation and verification
- **NLP**: Natural language processing for intent parsing and multilingual support
- **Transactions**: On-ramp and off-ramp operations, transaction status, and fraud detection
- **Wallet**: Smart wallet backup and recovery operations
- **Voice Biometrics**: Voice ID registration and verification

## Base URL

All API endpoints are prefixed with `/api/v1/` followed by their respective category.

## Authentication Endpoints

### Request OTP

```
POST /api/v1/auth/request-otp
```

Request an OTP (One-Time Password) for two-factor authentication.

**Request Body:**
```json
{
  "user_id": "user_test_123",
  "phone_number": "+15551234567",
  "method": "sms"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP sent successfully via sms."
}
```

### Verify OTP

```
POST /api/v1/auth/verify-otp
```

Verify an OTP provided by the user.

**Request Body:**
```json
{
  "user_id": "user_test_123",
  "otp_code": "123456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP verified successfully.",
  "token": "mock_auth_token_for_user_test_123"
}
```

## NLP Endpoints

### Parse Intent

```
POST /api/v1/nlp/parse-intent
```

Parse natural language text to extract intent and structured data.

**Request Body:**
```json
{
  "user_id": "user_nlp_test_001",
  "text": "Send 100 KES to John Doe",
  "language": "en"
}
```

**Response:**
```json
{
  "user_id": "user_nlp_test_001",
  "original_text": "Send 100 KES to John Doe",
  "language_detected": "en",
  "translated_text": null,
  "intent": "payment",
  "parsed_data": {
    "original_text": "Send 100 KES to John Doe",
    "detected_language": "en",
    "parsed_text_language": "en",
    "amount": 100,
    "currency": "KES",
    "recipient_name": "John Doe"
  }
}
```

## Transaction Endpoints

### Initiate On-Ramp

```
POST /api/v1/transactions/onramp/initiate
```

Initiate an on-ramp transaction (buying USDC with local currency).

**Request Body:**
```json
{
  "user_id": "user_tx_test_001",
  "fiat_amount": 100.0,
  "fiat_currency": "KES",
  "provider": "remitai_mock"
}
```

**Response:**
```json
{
  "success": true,
  "transaction_id": "tx_1621234567_1234",
  "status": "pending",
  "details": {
    "transaction_id": "tx_1621234567_1234",
    "status": "pending",
    "provider": "RemitAI Mock Provider",
    "amount": 100.0,
    "currency": "KES",
    "fees": 0.05,
    "exchange_rate": 0.0077,
    "usdc_amount": 0.77,
    "recipient_address": "USER_SMART_WALLET_ADDRESS_FOR_user_tx_test_001",
    "payment_method": "Bank Transfer",
    "payment_instructions": {
      "account_name": "RemitAI Payment Processor",
      "account_number": "1234567890",
      "bank_name": "Mock Bank",
      "reference": "tx_1621234567_1234"
    },
    "estimated_completion_time": "1-5 minutes",
    "created_at": "2025-05-17 07:31:00",
    "expires_at": "2025-05-17 08:31:00"
  }
}
```

### Check On-Ramp Status

```
GET /api/v1/transactions/onramp/status/{transaction_id}
```

Check the status of an on-ramp transaction.

**Response:**
```json
{
  "transaction_id": "tx_1621234567_1234",
  "status": "completed",
  "details": {
    "transaction_id": "tx_1621234567_1234",
    "status": "completed",
    "message": "Transaction completed successfully",
    "last_updated": "2025-05-17 07:34:00"
  }
}
```

### Initiate Off-Ramp

```
POST /api/v1/transactions/offramp/initiate
```

Initiate an off-ramp transaction (selling USDC for local currency).

**Request Body:**
```json
{
  "user_id": "user_tx_test_002",
  "usdc_amount": 50.0,
  "target_currency": "NGN",
  "recipient_details": {
    "account_number": "0123456789",
    "bank_code": "058",
    "recipient_name": "John Doe"
  },
  "provider": "flutterwave_mock"
}
```

**Response:**
```json
{
  "success": true,
  "transaction_id": "offtx_1621234567_5678",
  "status": "pending_usdc_transfer",
  "details": {
    "transaction_id": "offtx_1621234567_5678",
    "status": "pending_usdc_transfer",
    "provider": "Flutterwave (Mock)",
    "usdc_amount_due": 50.0,
    "target_currency": "NGN",
    "estimated_fiat_payout": 75600.0,
    "fees_in_usdc": 0.9,
    "payout_method": "Bank Transfer",
    "payout_details_provided": {
      "account_number": "0123456789",
      "bank_code": "058",
      "recipient_name": "John Doe"
    },
    "deposit_address_for_usdc": "STELLAR_ADDRESS_FOR_FLUTTERWAVE_MOCK_DEPOSITS",
    "memo_required": "REMITAI_offtx_1621234567_5678",
    "estimated_completion_time": "15-60 minutes",
    "created_at": "2025-05-17 07:31:00",
    "expires_at": "2025-05-17 08:31:00"
  }
}
```

### Check Off-Ramp Status

```
GET /api/v1/transactions/offramp/status/{transaction_id}
```

Check the status of an off-ramp transaction.

**Response:**
```json
{
  "transaction_id": "offtx_1621234567_5678",
  "status": "usdc_received_processing_fiat",
  "details": {
    "transaction_id": "offtx_1621234567_5678",
    "status": "usdc_received_processing_fiat",
    "message": "USDC received. Processing fiat payout.",
    "last_updated": "2025-05-17 07:32:00"
  }
}
```

### Confirm Withdrawal on Contract

```
POST /api/v1/transactions/withdrawal/confirm-on-contract
```

Confirm a withdrawal on the smart contract.

**Request Body:**
```json
{
  "user_id": "user_tx_test_003",
  "transaction_id": "offramp_tx_123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Funds locked successfully"
}
```

### Payout Webhook

```
POST /api/v1/transactions/webhook/payout-status
```

Webhook endpoint for fiat payout providers to send status updates.

**Request Body:**
```json
{
  "transaction_id": "offramp_tx_123",
  "status": "completed",
  "provider_data": {
    "reference": "prov_ref_abc"
  }
}
```

**Response:**
```json
{
  "status": "acknowledged"
}
```

### Assess Transaction Risk

```
POST /api/v1/transactions/assess-risk
```

Assess the fraud risk of a potential transaction.

**Request Body:**
```json
{
  "user_id": "user_risk_test_001",
  "command_text": "Send 5000 KES to Bob",
  "amount": 5000.0,
  "recipient_id": "bob_user_id"
}
```

**Response:**
```json
{
  "user_id": "user_risk_test_001",
  "is_suspicious": false,
  "risk_score": 0,
  "reasons": [],
  "timestamp": 1621234567.89
}
```

## Wallet Endpoints

### Generate Recovery Phrase

```
POST /api/v1/wallet/backup/generate-phrase
```

Generate a recovery phrase (mnemonic) for wallet backup.

**Response:**
```json
{
  "success": true,
  "mnemonic_words": ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "mango", "nectarine"],
  "message": "Recovery phrase generated successfully. Store it securely!"
}
```

### Confirm Recovery Phrase Saved

```
POST /api/v1/wallet/backup/confirm-saved
```

Confirm that the user has saved their recovery phrase.

**Request Body:**
```json
{
  "user_id": "user_wallet_001"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Passphrase backup process acknowledged. Store your passphrase securely!"
}
```

### Link Biometric for Recovery

```
POST /api/v1/wallet/backup/link-biometric
```

Link voice biometric for assisted recovery.

**Request Body:**
```json
{
  "user_id": "user_wallet_001",
  "voice_print_id": "voice_print_abc123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Biometric assisted recovery setup successful (mock)."
}
```

### Recover with Passphrase

```
POST /api/v1/wallet/recover/passphrase
```

Recover wallet using passphrase.

**Request Body:**
```json
{
  "user_id": "user_wallet_001",
  "passphrase_words": ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "mango", "nectarine"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Wallet recovery with passphrase successful (mock)."
}
```

### Recover with Biometric

```
POST /api/v1/wallet/recover/biometric
```

Recover wallet using biometric (voice) verification.

**Request Body:**
```json
{
  "user_id": "user_wallet_001",
  "voice_verification_token": "voice_verification_token_xyz123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Wallet recovery with biometric assistance successful (mock)."
}
```

## Voice Biometrics Endpoints

### Register Voice

```
POST /api/v1/voice/register
```

Register a voice print for a user.

**Request Body:**
```json
{
  "user_id": "user_voice_001",
  "audio_sample_paths": ["/path/to/audio1.wav", "/path/to/audio2.wav"]
}
```

**Response:**
```json
{
  "success": true,
  "voice_id": "voice_print_abc123",
  "message": "Voice ID registered successfully.",
  "enrollment_details": {
    "voice_id": "voice_print_abc123",
    "user_identifier": "user_voice_001",
    "status": "enrolled",
    "enrollment_date": 1621234567.89,
    "num_samples_processed": 2
  }
}
```

### Verify Voice

```
POST /api/v1/voice/verify
```

Verify a user's voice against their registered voice print.

**Request Body:**
```json
{
  "user_id": "user_voice_001",
  "audio_sample_path": "/path/to/verify_audio.wav",
  "attempt_liveness_check": true
}
```

**Response:**
```json
{
  "success": true,
  "verified": true,
  "message": "Voice verified successfully.",
  "match_score": 0.92,
  "verification_token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}
```

## Error Handling

All endpoints follow a consistent error handling pattern. When an error occurs, the API returns an appropriate HTTP status code along with a JSON response containing an error message.

Example error response:

```json
{
  "detail": "Invalid OTP."
}
```

Common HTTP status codes:
- 400: Bad Request (client error)
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Running the API

To run the API locally:

```bash
cd /home/ubuntu/remitai/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation (Swagger UI)

When the API is running, interactive documentation is available at:

```
http://localhost:8000/docs
```

This provides a user-friendly interface to explore and test all API endpoints.
