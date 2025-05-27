# RemitAI Backend Structure and API Requirements

## 1. Introduction

This document outlines the requirements for the backend structure and API endpoints for the RemitAI project. The goal is to create a well-organized, maintainable, and scalable backend that effectively supports all frontend functionalities and integrates the various backend services developed so far.

## 2. Overall Backend Architecture Goals

*   **Modularity:** Each component (NLP, On-Ramp, Security, etc.) should be a distinct service or module.
*   **Maintainability:** The codebase should be easy to understand, modify, and debug. Clear separation of concerns is key.
*   **Scalability (Conceptual):** While this is a mock implementation, the structure should conceptually allow for future scaling (e.g., by containerizing services).
*   **Security:** API endpoints must be designed with security best practices in mind, even in a mock environment (e.g., input validation, clear error messages that don't leak sensitive info).
*   **Testability:** The structure should facilitate unit and integration testing for backend components.

## 3. Proposed Directory Structure (within `/home/ubuntu/remitai/backend`)

```
/remitai/backend/
├── main.py                 # Main application entry point (e.g., FastAPI or Flask app)
├── config.py               # Application configuration settings
├── requirements.txt        # Python dependencies for the backend
├── /api/
│   ├── __init__.py
│   ├── v1/                   # API versioning (good practice)
│   │   ├── __init__.py
│   │   ├── endpoints/        # Directory for endpoint route definitions
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Authentication related endpoints (login, register, 2FA)
│   │   │   ├── nlp.py          # NLP processing endpoints
│   │   │   ├── transactions.py # Transaction related endpoints (onramp, offramp, status)
│   │   │   ├── wallet.py       # Wallet management (backup, recovery links)
│   │   │   └── voice.py        # Voice biometrics endpoints
│   │   └── schemas/          # Pydantic models for request/response validation
│   │       ├── __init__.py
│   │       ├── auth_schemas.py
│   │       ├── nlp_schemas.py
│   │       ├── transaction_schemas.py
│   │       └── wallet_schemas.py
├── /core/
│   └── __init__.py           # Core logic, security utilities not part of specific services
├── /services/                # Existing backend services, to be integrated via controllers/routers
│   ├── __init__.py
│   ├── nlp_service.py
│   ├── onramp_service.py
│   ├── offramp_service.py
│   ├── withdrawal_confirmation_service.py
│   ├── voice_biometrics_service.py
│   ├── two_factor_auth_service.py
│   ├── smart_wallet_backup_service.py
│   └── fraud_detection_service.py
├── /utils/
│   ├── __init__.py
│   └── exchange_rates.py     # Utility functions like currency conversion
└── /tests/                   # Unit and integration tests for the backend
    ├── __init__.py
    └── ... (test files for each module/service)
```

**Rationale:**
*   **`main.py`**: Central application runner (e.g., using FastAPI or Flask).
*   **`api/v1/endpoints/`**: Organizes API routes by feature, making them easier to find and manage.
*   **`api/v1/schemas/`**: Uses Pydantic (or similar) for data validation and serialization, improving robustness and providing clear API contracts.
*   **`services/`**: Houses the business logic for different features, keeping it separate from API routing and request/response handling.
*   **`utils/`**: Contains shared utility functions.
*   **`core/`**: For any core application logic, security helpers, etc., that don't fit neatly into a specific service or util.

## 4. Core API Endpoint Categories & Definitions (Conceptual)

All endpoints will be prefixed with `/api/v1/`.

### 4.1. Authentication (`/auth`)
*   **POST `/auth/register`**: User registration (mock).
*   **POST `/auth/login`**: User login (mock).
*   **POST `/auth/request-otp`**: Request 2FA OTP.
    *   Request: `{ "user_id": "string", "phone_number": "string", "method": "sms" | "whatsapp" }`
    *   Response: `{ "success": "boolean", "message": "string" }`
*   **POST `/auth/verify-otp`**: Verify 2FA OTP.
    *   Request: `{ "user_id": "string", "otp_code": "string" }`
    *   Response: `{ "success": "boolean", "message": "string", "token": "string" (if successful) }`

### 4.2. NLP & Chat (`/nlp`)
*   **POST `/nlp/parse-intent`**: Process natural language query to extract intent.
    *   Request: `{ "user_id": "string", "text": "string", "language": "string" (e.g., "en", "yo") }`
    *   Response: `{ "intent": "object", "original_text": "string", "translated_text": "string" (if applicable), "parsed_data": { "amount": "float", "currency": "string", ... } }` (based on `nlp_service.py` output)

### 4.3. Transactions (`/transactions`)
*   **POST `/transactions/initiate-onramp`**: Initiate a mock USDC purchase.
    *   Request: `{ "user_id": "string", "fiat_amount": "float", "fiat_currency": "string", "provider": "string" }`
    *   Response: `{ "success": "boolean", "transaction_id": "string", "status": "string", "details": "object" }`
*   **GET `/transactions/onramp-status/{transaction_id}`**: Check on-ramp transaction status.
    *   Response: `{ "transaction_id": "string", "status": "string", "details": "object" }`
*   **POST `/transactions/initiate-offramp`**: Initiate a mock USDC to fiat withdrawal.
    *   Request: `{ "user_id": "string", "usdc_amount": "float", "target_currency": "string", "recipient_details": "object", "provider": "string" }`
    *   Response: `{ "success": "boolean", "transaction_id": "string", "status": "string", "details": "object" }`
*   **GET `/transactions/offramp-status/{transaction_id}`**: Check off-ramp transaction status.
    *   Response: `{ "transaction_id": "string", "status": "string", "details": "object" }`
*   **POST `/transactions/confirm-withdrawal`**: (Mock) Smart contract interaction for withdrawal.
    *   Request: `{ "user_id": "string", "transaction_id": "string" }`
    *   Response: `{ "success": "boolean", "message": "string" }`
*   **POST `/transactions/webhook/payout-status`**: (Mock) Webhook from fiat payout provider.
    *   Request: `{ "transaction_id": "string", "status": "completed" | "failed", "provider_data": "object" }`
    *   Response: `{ "status": "received" }`
*   **POST `/transactions/assess-risk`**: Assess fraud risk for a potential transaction.
    *   Request: `{ "user_id": "string", "command_text": "string", "amount": "float", "recipient_id": "string" }`
    *   Response: (Based on `fraud_detection_service.py` output)

### 4.4. Wallet Management (`/wallet`)
*   **POST `/wallet/backup/generate-phrase`**: (Mock) Guide user to generate recovery phrase (client-side focus).
    *   Response: `{ "success": "boolean", "mnemonic_words": ["word1", ...] }` (Or just guidance if fully client-side)
*   **POST `/wallet/backup/confirm-saved`**: User confirms they saved the phrase.
    *   Request: `{ "user_id": "string" }`
    *   Response: `{ "success": "boolean", "message": "string" }`
*   **POST `/wallet/backup/link-biometric`**: Link voice biometric for assisted recovery.
    *   Request: `{ "user_id": "string", "voice_print_id": "string" }`
    *   Response: `{ "success": "boolean", "message": "string" }`
*   **POST `/wallet/recover/passphrase`**: (Mock) Initiate recovery with passphrase (client-side focus).
    *   Request: `{ "user_id": "string", "passphrase_words": ["word1", ...] }`
    *   Response: `{ "success": "boolean", "message": "string" }`
*   **POST `/wallet/recover/biometric`**: (Mock) Initiate recovery with biometric.
    *   Request: `{ "user_id": "string", "voice_verification_token": "string" }`
    *   Response: `{ "success": "boolean", "message": "string" }`

### 4.5. Voice Biometrics (`/voice`)
*   **POST `/voice/register`**: Register a voice print.
    *   Request: `{ "user_id": "string", "voice_sample_path_or_data": "string" }` (Path for mock, data for real)
    *   Response: `{ "success": "boolean", "voice_print_id": "string", "message": "string" }`
*   **POST `/voice/verify`**: Verify a voice print.
    *   Request: `{ "user_id": "string", "voice_sample_path_or_data": "string" }`
    *   Response: `{ "success": "boolean", "verified": "boolean", "token": "string" (if verified), "message": "string" }`

### 4.6. Utilities (`/utils` - or integrated into other endpoints)
*   **GET `/utils/exchange-rate`**: Get exchange rate.
    *   Query Params: `from_currency=USD&to_currency=KES&amount=100`
    *   Response: `{ "from_currency": "string", "to_currency": "string", "rate": "float", "converted_amount": "float" }`

## 5. General API Design Principles

*   **Framework:** FastAPI is recommended due to its modern features, automatic data validation (with Pydantic), and OpenAPI documentation generation.
*   **Statelessness:** APIs should be stateless where possible.
*   **JSON for Request/Response:** Use JSON for all request and response bodies.
*   **HTTP Status Codes:** Use appropriate HTTP status codes (e.g., 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error).
*   **Error Handling:** Provide clear, consistent error messages in JSON format: `{ "detail": "Error message" }` or `{ "errors": [{"field": "field_name", "message": "error_description"}] }`.
*   **Input Validation:** All incoming data must be validated (e.g., using Pydantic schemas in FastAPI).
*   **Asynchronous Operations:** Utilize `async/await` for I/O-bound operations to improve performance, especially with FastAPI.

## 6. Data Models (Conceptual - Pydantic Schemas)

For each endpoint, Pydantic schemas will define the expected request and response structures. Examples:

```python
# Example: nlp_schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

class NLPParseRequest(BaseModel):
    user_id: str
    text: str
    language: Optional[str] = "en"

class NLPParseResponse(BaseModel):
    intent: Optional[Dict[str, Any]]
    original_text: str
    translated_text: Optional[str]
    parsed_data: Optional[Dict[str, Any]]
```

## 7. Next Steps

1.  Finalize the choice of web framework (FastAPI recommended).
2.  Implement the directory structure.
3.  Define Pydantic schemas for all API requests and responses.
4.  Implement API routers/controllers for each category of endpoints.
5.  Integrate existing backend services with these controllers.
6.  Implement comprehensive error handling and input validation.
7.  Write unit and integration tests.

This document provides a foundational plan for the backend structure and API development. It will be refined as implementation progresses.
