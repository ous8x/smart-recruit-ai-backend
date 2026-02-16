from transformers import pipeline
from sentence_transformers import SentenceTransformer
from functools import lru_cache
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

@lru_cache(maxsize=1)
def get_name_extraction_model():
    """Load Name Extraction Model (Cached)"""
    logger.info(f"Loading Name Extraction Model: {settings.NAME_EXTRACTION_MODEL}")
    try:
        qa_pipeline = pipeline(
            'question-answering',
            model=settings.NAME_EXTRACTION_MODEL,
            tokenizer=settings.NAME_EXTRACTION_MODEL
        )
        logger.info("✅ Name Extraction Model loaded successfully")
        return qa_pipeline
    except Exception as e:
        logger.error(f"❌ Failed to load Name Extraction Model: {e}")
        raise

@lru_cache(maxsize=1)
def get_scoring_model():
    """Load Sentence Transformer Model for Scoring (Cached)"""
    logger.info(f"Loading Scoring Model: {settings.SCORING_MODEL}")
    try:
        model = SentenceTransformer(settings.SCORING_MODEL)
        logger.info("✅ Scoring Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"❌ Failed to load Scoring Model: {e}")
        raise
