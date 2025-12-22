from fastapi import APIRouter, Form, HTTPException
from database import resume_collection
from calculation import analyze_resume_against_jd
from ml_executor import execute_ml_work
from bson import ObjectId
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter()

async def analyze_single_resume(resume_data, jd_text):
    """Analyze a single resume - runs in thread pool (non-blocking)"""
    try:
        resume_url = resume_data["resumeUrl"]
        email = resume_data["email"]
        drive_url = resume_data.get("driveUrl", "")
        resume_id = resume_data["_id"]

        # Run ML analysis in thread pool (non-blocking)
        analysis = await execute_ml_work(
            analyze_resume_against_jd,
            resume_url=resume_url,
            jd_text=jd_text
        )

        return {
            "resumeId": str(resume_id),
            "email": email,
            "resumeUrl": resume_url,
            "driveUrl": drive_url,
            "matchedSkills": analysis["matchedSkills"],
            "scores": {
                "skillScore": analysis["skillScore"],
                "tfidfScore": analysis["tfidfScore"],
                "bertScore": analysis["bertScore"],
                "hybridScore": analysis["hybridScore"]
            }
        }
    except Exception as e:
        logger.error(f"⚠️ Error analyzing resume {resume_data.get('_id')}: {e}")
        return None

@router.post("/top-matches")
async def get_top_matching_resumes(jd_text: str = Form(...)):
    try:
        resumes = list(resume_collection.find({}, {
            "resumeUrl": 1,
            "email": 1,
            "driveUrl": 1,   # <-- Include this
            "_id": 1
        }))
        
        if not resumes:
            raise HTTPException(status_code=404, detail="No resumes available in database.")

        logger.info(f"🔍 Analyzing {len(resumes)} resumes against JD...")

        # Process all resumes in parallel using asyncio.gather
        # This allows FastAPI to handle other requests while ML work runs in threads
        tasks = [analyze_single_resume(resume, jd_text) for resume in resumes]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out None results (failed analyses) and exceptions
        valid_results = []
        for result in results:
            if result and not isinstance(result, Exception):
                valid_results.append(result)

        # Group by email and keep best resume per email
        email_to_best_resume = {}
        for resume_data in valid_results:
            email = resume_data["email"]
            if email not in email_to_best_resume or \
               resume_data["scores"]["hybridScore"] > email_to_best_resume[email]["scores"]["hybridScore"]:
                email_to_best_resume[email] = resume_data

        # Sort and return top 10
        top_resumes = sorted(
            email_to_best_resume.values(),
            key=lambda x: x["scores"]["hybridScore"],
            reverse=True
        )[:10]

        logger.info(f"✅ Found {len(top_resumes)} top matching resumes")

        return {
            "message": "Top matching resumes retrieved",
            "jd": jd_text,
            "count": len(top_resumes),
            "topResumes": top_resumes
        }

    except Exception as e:
        logger.error(f"❌ Error matching resumes: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error matching resumes: {str(e)}")
