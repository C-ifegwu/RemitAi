from fastapi import APIRouter, HTTPException, status, Depends
from remitai.backend.api.v1.schemas.nlp_schemas import NLPParseRequest, NLPParseResponse
from remitai.backend.services.nlp_service import NLPIntentParser

router = APIRouter()

# Dependency for NLPIntentParser service
def get_nlp_service():
    return NLPIntentParser()

@router.post("/parse-intent", response_model=NLPParseResponse)
async def parse_intent_endpoint(
    request_data: NLPParseRequest,
    service: NLPIntentParser = Depends(get_nlp_service)
):
    """Endpoint to parse natural language text and extract intent."""
    try:
        # Assuming sender_country_code might be part of user profile or other context
        # For now, passing None or a mock value if not directly in request_data
        # The NLPParseRequest schema doesn't have sender_country_code, so it's not passed from client directly here.
        # This might need adjustment based on how sender_country_code is determined.
        parsed_result = service.parse_intent(text=request_data.text, sender_country_code=None) # Or fetch from user profile based on user_id

        return NLPParseResponse(
            user_id=request_data.user_id,
            original_text=parsed_result.get("original_text", request_data.text),
            language_detected=parsed_result.get("detected_language"),
            translated_text=parsed_result.get("parsed_text_language") if parsed_result.get("parsed_text_language") != parsed_result.get("detected_language") else None,
            intent=parsed_result.get("intent", "payment"), # Defaulting intent for now
            parsed_data=parsed_result
        )
    except Exception as e:
        # Log the exception e
        print(f"[NLP ENDPOINT ERROR] {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during NLP processing: {str(e)}"
        )

@router.get("/nlp/test") # Original test route
async def test_nlp():
    return {"message": "NLP endpoint test successful - new version"}

