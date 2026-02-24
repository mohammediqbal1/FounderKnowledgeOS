from core.config import GEMINI_URL
from core.http_client import call_gemini_with_retry

CATEGORIES = [
    "ELECTRICAL_CONTRACT",
    "SEMICONDUCTOR",
    "AI_SYSTEM",
    "FINANCIAL",
    "GENERAL",
]


def classify_document(text: str) -> str:
    """
    Classify a document into one of the predefined domain categories
    using Google Gemini API with retry logic.
    
    Args:
        text: The full document text (first 1500 chars will be used).
    
    Returns:
        A single category string from CATEGORIES.
    """
    prompt = f"""Classify the following document into exactly one of these categories:
{CATEGORIES}

Document:
{text[:1500]}

Return only the category name. Nothing else."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 50,
        },
    }

    try:
        data = call_gemini_with_retry(GEMINI_URL, payload)
        
        result = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "GENERAL")
            .strip()
        )

        # Validate the result is a known category
        for category in CATEGORIES:
            if category in result.upper():
                return category

        return "GENERAL"

    except Exception as e:
        print(f"[Classification] Error: {e}. Defaulting to GENERAL.")
        return "GENERAL"
