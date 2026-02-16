import re
from app.ai.model_loader import get_name_extraction_model
import logging

logger = logging.getLogger(__name__)

def clean_extracted_name(raw_name: str) -> str:
    """
    Clean the extracted name from model output
    Removes markdown headers, extra spaces, etc.
    """
    if not raw_name:
        return "Unknown"
    
    # Remove markdown headers (##, ###)
    cleaned = re.sub(r'^#+\s*', '', raw_name)
    
    # Remove extra whitespace
    cleaned = ' '.join(cleaned.split())
    
    # Remove common prefixes
    cleaned = re.sub(r'^(Nom|Name|Email)\s*', '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip() or "Unknown"

def extract_candidate_name(cv_text: str) -> tuple[str, float]:
    """
    Extract candidate name from CV text using AI
    
    Args:
        cv_text: Full CV text content
        
    Returns:
        Tuple of (candidate_name, confidence_score)
    """
    if not cv_text or len(cv_text.strip()) < 50:
        logger.warning("CV text too short for name extraction")
        return "Unknown", 0.0
    
    logger.info("🤖 Extracting candidate name using AI...")
    
    try:
        qa_pipeline = get_name_extraction_model()
        
        # Use first 3000 chars for better accuracy
        context = cv_text[:3000]
        
        result = qa_pipeline({
            'question': "What is the name of the candidate?",
            'context': context
        })
        
        raw_name = result['answer']
        confidence = round(result['score'], 2)
        
        cleaned_name = clean_extracted_name(raw_name)
        
        logger.info(f"✅ Name extracted: '{cleaned_name}' (confidence: {confidence})")
        
        return cleaned_name, confidence
        
    except Exception as e:
        logger.error(f"❌ Name extraction failed: {e}")
        return "Unknown", 0.0
