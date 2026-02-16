"""
Smart Recruit AI - Model Downloader
===================================

This script pre-downloads ALL AI models required by the application.
Run this file ONCE with internet access (Task Component / local docker).

✔ Cloud safe
✔ Linux safe
✔ Offline ready
✔ Production ready
"""

import os
from pathlib import Path

# ============================================================
# Global Cache Directory (IMPORTANT)
# ============================================================

BASE_DIR = Path("/app")
CACHE_DIR = BASE_DIR / ".cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

os.environ["HF_HOME"] = str(CACHE_DIR)
os.environ["TRANSFORMERS_CACHE"] = str(CACHE_DIR)
os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(CACHE_DIR)
os.environ["TORCH_HOME"] = str(CACHE_DIR)

# ============================================================
# Main Downloader
# ============================================================

def download_all_models():
    print("=" * 70)
    print("🚀 Smart Recruit AI - Downloading AI Models")
    print("=" * 70)

    # --------------------------------------------------------
    # 1️⃣ Docling + OCR Models
    # --------------------------------------------------------
    print("\n[1/3] Downloading Docling & OCR models...")
    try:
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
        from docling.datamodel.base_models import InputFormat

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

        DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )

        print("✅ Docling & OCR models ready")

    except Exception as e:
        print("❌ Failed to download Docling models")
        raise e

    # --------------------------------------------------------
    # 2️⃣ Name Extraction (QA Transformer)
    # --------------------------------------------------------
    print("\n[2/3] Downloading Name Extraction model...")
    try:
        from transformers import AutoTokenizer, AutoModelForQuestionAnswering

        model_name = "timpal0l/mdeberta-v3-base-squad2"

        AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=CACHE_DIR
        )
        AutoModelForQuestionAnswering.from_pretrained(
            model_name,
            cache_dir=CACHE_DIR
        )

        print("✅ Name Extraction model ready")

    except Exception as e:
        print("❌ Failed to download Name Extraction model")
        raise e

    # --------------------------------------------------------
    # 3️⃣ CV Scoring (Sentence Transformer)
    # --------------------------------------------------------
    print("\n[3/3] Downloading CV Scoring model...")
    try:
        from sentence_transformers import SentenceTransformer

        SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2",
            cache_folder=str(CACHE_DIR)
        )

        print("✅ CV Scoring model ready")

    except Exception as e:
        print("❌ Failed to download Sentence Transformer model")
        raise e

    # --------------------------------------------------------
    # DONE
    # --------------------------------------------------------
    print("\n" + "=" * 70)
    print("🎉 ALL MODELS DOWNLOADED SUCCESSFULLY")
    print("=" * 70)
    print(f"📂 Cache directory: {CACHE_DIR}")
    print("🚀 Application is now 100% OFFLINE READY")
    print("=" * 70)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    download_all_models()
