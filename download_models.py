"""
Pre-download all AI models for offline usage
Run once with internet connection
"""

import os
import sys
from pathlib import Path

def download_all_models():
    print("=" * 70)
    print("🚀 Smart Recruit AI - Model Downloader")
    print("=" * 70)
    
    # ==========================================
    # 1. Download Docling & OCR Models
    # ==========================================
    print("\n📦 Step 1/4: Downloading Docling & OCR models...")
    try:
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
        from docling.datamodel.base_models import InputFormat
        
        # Initialize converter (will download models)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
        
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
        print("✅ Docling & OCR models downloaded")
        
    except Exception as e:
        print(f"❌ Error downloading Docling models: {e}")
        return False
    
    # ==========================================
    # 2. Download Name Extraction Model
    # ==========================================
    print("\n📦 Step 2/4: Downloading Name Extraction model...")
    try:
        from transformers import AutoModelForQuestionAnswering, AutoTokenizer
        
        model_name = "timpal0l/mdeberta-v3-base-squad2"
        print(f"   Downloading: {model_name}")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        
        print("✅ Name Extraction model downloaded")
        
    except Exception as e:
        print(f"❌ Error downloading Name Extraction model: {e}")
        return False
    
    # ==========================================
    # 3. Download Sentence Transformer Model
    # ==========================================
    print("\n📦 Step 3/4: Downloading Sentence Transformer model...")
    try:
        from sentence_transformers import SentenceTransformer
        
        scoring_model = "paraphrase-multilingual-MiniLM-L12-v2"
        print(f"   Downloading: {scoring_model}")
        
        model = SentenceTransformer(scoring_model)
        
        print("✅ Sentence Transformer model downloaded")
        
    except Exception as e:
        print(f"❌ Error downloading Sentence Transformer: {e}")
        return False
    
    # ==========================================
    # 4. Install Additional Speed Optimizations
    # ==========================================
    print("\n📦 Step 4/4: Installing performance packages...")
    try:
        import subprocess
        
        packages = [
            "onnxruntime",
            "huggingface_hub[hf_xet]"
        ]
        
        for package in packages:
            print(f"   Installing: {package}")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "--quiet"],
                check=True
            )
        
        print("✅ Performance packages installed")
        
    except Exception as e:
        print(f"⚠️ Warning: {e}")
        print("   (Not critical, app will still work)")
    
    # ==========================================
    # Success Summary
    # ==========================================
    print("\n" + "=" * 70)
    print("🎉 ALL MODELS DOWNLOADED SUCCESSFULLY!")
    print("=" * 70)
    print("\n✅ Your app is now ready to work 100% OFFLINE")
    print("\n📂 Models saved to:")
    print(f"   - C:\\Users\\{os.getenv('USERNAME')}\\.cache\\huggingface")
    print(f"   - {Path.cwd()}\\venv\\Lib\\site-packages\\rapidocr\\models")
    print("\n🚀 Next steps:")
    print("   1. Run: python run.py")
    print("   2. Upload CVs - processing will be fast now!")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = download_all_models()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
