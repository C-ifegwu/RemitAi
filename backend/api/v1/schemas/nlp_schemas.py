from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class NLPParseRequest(BaseModel):
    user_id: str = Field(..., example="user_nlp_test_001")
    text: str = Field(..., example="Send 100 KES to John Doe")
    language: Optional[str] = Field("en", example="en") # Default to English

class NLPParseResponse(BaseModel):
    user_id: str
    original_text: str
    language_detected: Optional[str] = None
    translated_text: Optional[str] = None
    intent: Optional[str] = None # e.g., "payment", "balance_inquiry"
    parsed_data: Optional[Dict[str, Any]] = None # e.g., {"amount": 100, "currency": "KES", ...}
    error_message: Optional[str] = None

