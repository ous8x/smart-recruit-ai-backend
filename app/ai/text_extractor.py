import os
import unicodedata
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_docling_converter():
    """Initialize Docling Converter (Cached)"""
    logger.info("⚙️ Initializing Docling converter...")
    
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    logger.info("✅ Docling converter ready")
    return converter

def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    if not text:
        return ""
    return unicodedata.normalize('NFKC', text)

def extract_text_from_cv(file_path: str) -> str:
    """
    Extract text from PDF/DOCX file using Docling
    
    Args:
        file_path: Path to the CV file
        
    Returns:
        Cleaned text content
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    logger.info(f"📄 Extracting text from: {os.path.basename(file_path)}")
    
    try:
        converter = get_docling_converter()
        result = converter.convert(file_path)
        raw_text = result.document.export_to_markdown()
        cleaned_text = clean_text(raw_text)
        
        logger.info(f"✅ Text extracted successfully ({len(cleaned_text)} chars)")
        return cleaned_text
        
    except Exception as e:
        logger.error(f"❌ Failed to extract text: {e}")
        raise
