import re
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

# Mock data for countries and currencies for simplicity
AFRICAN_COUNTRIES = {
    "nigeria": "NG",
    "kenya": "KE",
    "ghana": "GH",
    # Add more countries as needed
}

CURRENCIES = {
    "naira": "NGN",
    "shilling": "KES", # Kenyan Shilling
    "cedi": "GHS",   # Ghanaian Cedi
    "ngn": "NGN",
    "kes": "KES",
    "ghs": "GHS",
    "dollars": "USD", # Added for more general cases
    "usd": "USD",
    # Add more currency names and codes
}

# Supported languages for translation to English before parsing
# Yoruba (yo), Igbo (ig), Hausa (ha), French (fr), Arabic (ar), Swahili (sw)
SUPPORTED_LANGUAGES_FOR_TRANSLATION = ["yo", "ig", "ha", "fr", "ar", "sw"]

class NLPIntentParser:
    def __init__(self):
        pass

    def _translate_to_english(self, text: str, source_language: str) -> str:
        """Translates text from source_language to English."""
        try:
            translated_text = GoogleTranslator(source=source_language, target="en").translate(text)
            print(f"[NLP] Translated from {source_language} to en: \"{text}\" -> \"{translated_text}\"")
            return translated_text
        except Exception as e:
            print(f"[NLP] Error translating from {source_language}: {e}")
            return text # Return original text if translation fails

    def parse_intent(self, text: str, sender_country_code: str = None):
        original_text = text
        detected_lang = "en" # Default to English
        try:
            detected_lang = detect(text)
            print(f"[NLP] Detected language: {detected_lang} for input: \"{text}\"")
        except LangDetectException:
            print(f"[NLP] Could not detect language for: \"{text}\". Assuming English.")

        if detected_lang != "en" and detected_lang in SUPPORTED_LANGUAGES_FOR_TRANSLATION:
            text = self._translate_to_english(text, detected_lang)
        elif detected_lang != "en" and detected_lang not in SUPPORTED_LANGUAGES_FOR_TRANSLATION:
            print(f"[NLP] Language {detected_lang} not in supported list for direct translation to English for parsing. Proceeding with original text, parsing might be less accurate.")
            # For unsupported languages, we might still try to parse if it contains numbers/keywords
            # or return an error/request for English input.

        text_lower = text.lower() # Parse the (potentially translated) English text
        
        amount = None
        currency = None
        recipient_name = None
        recipient_country = None
        sender_country = AFRICAN_COUNTRIES.get(sender_country_code.lower()) if sender_country_code else None

        amount_currency_match = re.search(r"(\d{1,3}(?:,\d{3})*|\d+)\s*([a-zA-Z]+)", text_lower)
        currency_amount_match = re.search(r"([a-zA-Z]{3})\s*(\d{1,3}(?:,\d{3})*|\d+)", text_lower)

        if amount_currency_match:
            try:
                amount_str = amount_currency_match.group(1).replace(",", "")
                amount = int(amount_str)
                currency_word = amount_currency_match.group(2)
                currency = CURRENCIES.get(currency_word)
            except ValueError:
                pass
        elif currency_amount_match:
            try:
                amount_str = currency_amount_match.group(2).replace(",", "")
                amount = int(amount_str)
                currency_code_match = currency_amount_match.group(1)
                currency = CURRENCIES.get(currency_code_match)
            except ValueError:
                pass

        recipient_match_in = re.search(r"to\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)\s+in\s+([a-zA-Z]+)", text_lower)
        if recipient_match_in:
            potential_name = recipient_match_in.group(1).strip()
            potential_country = recipient_match_in.group(2).strip()
            if AFRICAN_COUNTRIES.get(potential_country):
                recipient_name = potential_name.title()
                recipient_country = AFRICAN_COUNTRIES.get(potential_country)
        
        if not recipient_name:
            recipient_match_parentheses = re.search(r"to\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)\s+\(([a-zA-Z]+)\)", text_lower)
            if recipient_match_parentheses:
                potential_name = recipient_match_parentheses.group(1).strip()
                potential_country_in_paren = recipient_match_parentheses.group(2).strip()
                if AFRICAN_COUNTRIES.get(potential_country_in_paren):
                    recipient_name = potential_name.title()
                    recipient_country = AFRICAN_COUNTRIES.get(potential_country_in_paren)

        if not recipient_name and amount is not None:
            recipient_only_match = re.search(r"to\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)*)", text_lower)
            if recipient_only_match:
                possible_name_candidate = recipient_only_match.group(1).strip()
                if not AFRICAN_COUNTRIES.get(possible_name_candidate):
                     recipient_name = possible_name_candidate.title()

        if not sender_country and currency:
            for country_name, country_code_val in AFRICAN_COUNTRIES.items():
                if currency == "NGN" and country_code_val == "NG": sender_country = "NG"; break
                if currency == "KES" and country_code_val == "KE": sender_country = "KE"; break
                if currency == "GHS" and country_code_val == "GH": sender_country = "GH"; break
        
        parsed_data = {"original_text": original_text, "detected_language": detected_lang, "parsed_text_language": "en" if text != original_text else detected_lang}
        if amount is not None: parsed_data["amount"] = amount
        if currency: parsed_data["currency"] = currency
        if sender_country: parsed_data["sender_country_code"] = sender_country
        if recipient_name: parsed_data["recipient_name"] = recipient_name
        if recipient_country: parsed_data["recipient_country_code"] = recipient_country

        return parsed_data

if __name__ == "__main__":
    parser = NLPIntentParser()
    
    test_phrases = [
        "Send 30,000 Naira to Amina in Kenya", # English
        "Je veux envoyer 500 dollars à Jean au Ghana", # French: I want to send 500 dollars to Jean in Ghana
        "Nataka kutuma shilingi elfu kumi kwa Maria nchini Nigeria", # Swahili: I want to send ten thousand shillings to Maria in Nigeria
        "إرسال 20000 دينار إلى فاطمة في كينيا", # Arabic: Send 20000 Dinar to Fatima in Kenya (Note: Dinar not in CURRENCIES, will be None)
        "Fi 30000 Naira ranṣẹ si Amina ni Kenya", # Yoruba: Send 30000 Naira to Amina in Kenya
        "Ziga Naira dubu talatin zuwa Amina a Kenya", # Hausa: Send thirty thousand Naira to Amina in Kenya
        "Zipu Naira puku iri atọ nye Amina na Kenya", # Igbo: Send thirty thousand Naira to Amina in Kenya
        "Pay 250 cedi to Kofi in Ghana"
    ]
    
    print("--- Multilingual Intent Parsing (Example) ---")
    for phrase in test_phrases:
        sender_country_context = None # Simplified context
        intent = parser.parse_intent(phrase, sender_country_code=sender_country_context)
        print(f"Input ({intent.get('detected_language', 'unknown')}): {intent.get('original_text')}")
        if intent.get('parsed_text_language') != intent.get('detected_language'):
             print(f"Translated to English for parsing: {intent.get('parsed_text_language')}")
        print(f"Parsed: {intent}\n")
