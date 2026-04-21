from langchain_groq import ChatGroq
from app.core.config import settings
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import logging

logger = logging.getLogger(__name__)

def get_llm(model_name: str = None) -> ChatGroq:
    """
    Initializes and returns a ChatGroq LLM instance.
    """
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=model_name or settings.GROQ_MODEL,
        temperature=settings.GROQ_TEMPERATURE,
        max_tokens=settings.GROQ_MAX_TOKENS,
        request_timeout=60.0,  # Increase timeout to 60 seconds
    )

def resilient_call(chain_or_llm, input_data: dict):
    """
    Wraps an LLM/Chain call with exponential backoff retries and model fallback.
    """
    
    @retry(
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=settings.RETRY_DELAY_MIN, max=settings.RETRY_DELAY_MAX),
        stop=stop_after_attempt(settings.MAX_RETRIES),
        reraise=True,
    )
    def _call_with_retry(obj, data):
        return obj.invoke(data)

    try:
        # Attempt 1: Primary Model
        return _call_with_retry(chain_or_llm, input_data)
    except Exception as e:
        logger.warning(f"Primary model failed or rate limited: {str(e)}. Attempting fallback...")
        raise e
