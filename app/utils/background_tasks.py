import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.application import Application, ProcessingStatus
from app.models.job import Job
from app.ai.text_extractor import extract_text_from_cv
from app.ai.name_extractor import extract_candidate_name
from app.ai.cv_scorer import calculate_match_score

logger = logging.getLogger(__name__)

async def process_cv_application(application_id: int, db: AsyncSession):
    """
    Background task to process a single CV application
    
    Steps:
    1. Extract text from CV file
    2. Extract candidate name
    3. Calculate match score against job description
    4. Update application record
    
    Args:
        application_id: ID of the application to process
        db: Database session
    """
    logger.info(f"🚀 Starting processing for Application ID: {application_id}")
    
    try:
        # Fetch application with job details
        result = await db.execute(
            select(Application).where(Application.id == application_id)
        )
        application = result.scalar_one_or_none()
        
        if not application:
            logger.error(f"❌ Application {application_id} not found")
            return
        
        # Update status to PROCESSING
        application.status = ProcessingStatus.PROCESSING
        await db.commit()
        
        # Fetch job description
        result = await db.execute(
            select(Job).where(Job.id == application.job_id)
        )
        job = result.scalar_one_or_none()
        
        if not job:
            raise Exception("Job not found")
        
        # Step 1: Extract text from CV
        logger.info(f"📄 Extracting text from: {application.original_filename}")
        extracted_text = extract_text_from_cv(application.cv_file_path)
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            raise Exception("Extracted text is too short or empty")
        
        # Step 2: Extract candidate name
        logger.info(f"👤 Extracting candidate name...")
        candidate_name, name_confidence = extract_candidate_name(extracted_text)
        
        # Step 3: Calculate match score
        logger.info(f"🎯 Calculating match score...")
        match_score = calculate_match_score(job.description, extracted_text)
        
        # Update application with results
        application.extracted_text = extracted_text
        application.candidate_name = candidate_name
        application.match_score = match_score
        application.status = ProcessingStatus.COMPLETED
        application.processed_at = datetime.utcnow()
        
        await db.commit()
        
        logger.info(
            f"✅ Processing completed for Application {application_id}\n"
            f"   Candidate: {candidate_name}\n"
            f"   Score: {match_score * 100:.2f}%"
        )
        
    except Exception as e:
        logger.error(f"❌ Processing failed for Application {application_id}: {e}")
        
        # Update status to FAILED
        try:
            result = await db.execute(
                select(Application).where(Application.id == application_id)
            )
            application = result.scalar_one_or_none()
            
            if application:
                application.status = ProcessingStatus.FAILED
                application.error_message = str(e)
                application.processed_at = datetime.utcnow()
                await db.commit()
        except Exception as db_error:
            logger.error(f"Failed to update error status: {db_error}")
