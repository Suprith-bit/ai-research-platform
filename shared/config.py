import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    # LLM Settings - Back to Gemini as requested
    USE_OPENAI = False  # Set to False to use Gemini
    MODEL_NAME = "gpt-4o-mini" if USE_OPENAI else "gemini-2.5-flash"
    MAX_TOKENS = 1500
    TEMPERATURE = 0.3

    # Search Settings - Optimized for speed
    MAX_SEARCH_RESULTS = 6
    MAX_SOURCES_PER_QUERY = 3

    # Agent Settings - Reduced for faster processing
    MAX_SUB_QUESTIONS = 3
    MIN_SUB_QUESTIONS = 2

    @classmethod
    def validate(cls):
        if cls.USE_OPENAI and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment")
        elif not cls.USE_OPENAI and not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment")
        if not cls.SERPER_API_KEY:
            raise ValueError("SERPER_API_KEY not found in environment")