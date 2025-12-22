# from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
# from typing import Optional
# from bson import ObjectId
# from datetime import datetime
# from database import resume_collection
# from utils import upload_pdf_to_cloudinary
# from calculation import analyze_resume_against_jd
# from ai_feedback import generate_feedback
# from auth_utils import get_current_user

# router = APIRouter()

# @router.post("/upload-resume-analyze")
# async def upload_and_analyze_resume(
#     file: Optional[UploadFile] = File(None),
#     jd_text: str = Form(...),
#     drive_url: Optional[str] = Form(None),
#     user=Depends(get_current_user),
# ):
#     print("📩 Received request from user:", user["email"])
#     print("📎 File uploaded:", bool(file))
#     print("🔗 Drive URL received:", drive_url)

#     if not file and not drive_url:
#         raise HTTPException(status_code=400, detail="Please upload a resume or provide a Google Drive link.")

#     try:
#         # Determine which URL to analyze (Cloudinary or Google Drive)
#         resume_url = ""
#         if file:
#             if file.content_type != "application/pdf":
#                 raise HTTPException(status_code=400, detail="Only PDF files are supported.")
#             print("📤 Uploading to Cloudinary...")
#             resume_url = upload_pdf_to_cloudinary(file.file)
#             print("✅ Uploaded to:", resume_url)
#         else:
#             resume_url = drive_url.strip()
#             print("✅ Using provided Google Drive link:", resume_url)

#         # ✅ Store both Cloudinary and Drive URLs regardless
#         resume_doc = {
#             "email": user["email"],
#             "resumeUrl": resume_url,  # This is used for analysis
#             "driveUrl": drive_url.strip() if drive_url else "NULL",  # Always store driveUrl if present
#             "aiFeedback": "",
#             "scores": {
#                 "skillScore": None,
#                 "tfidfScore": None,
#                 "bertScore": None,
#                 "hybridScore": None,
#             },
#             "uploadedAt": datetime.utcnow(),
#         }

#         result = resume_collection.insert_one(resume_doc)
#         resume_id = str(result.inserted_id)

#         # Perform analysis
#         analysis = analyze_resume_against_jd(resume_url=resume_url, jd_text=jd_text)
#         resume_text = analysis.get("resumeText", "")

#         feedback = generate_feedback(
#             resume_text=resume_text,
#             analysis_results=analysis
#         )

#         analysis["aiFeedback"] = feedback

#         # Update document with scores and feedback
#         resume_collection.update_one(
#             {"_id": ObjectId(resume_id)},
#             {
#                 "$set": {
#                     "scores.skillScore": analysis["skillScore"],
#                     "scores.tfidfScore": analysis["tfidfScore"],
#                     "scores.bertScore": analysis["bertScore"],
#                     "scores.hybridScore": analysis["hybridScore"],
#                     "aiFeedback": feedback,
#                 }
#             },
#         )

#         return {
#             "message": "Resume uploaded and analyzed successfully",
#             "resumeId": resume_id,
#             "resumeUrl": resume_url,
#             "driveUrl": drive_url.strip() if drive_url else "",
#             **analysis
#         }

#     except Exception as e:
#         print("❌ Error during resume analysis:", str(e))
#         raise HTTPException(status_code=500, detail=str(e))




# @router.post("/guest-analyze")
# def analyze_guest_resume():
#     try:
#         resume_url = "https://res.cloudinary.com/dloh7csm6/raw/upload/v1752328644/bbaexcathzjznjeixvo5.pdf"

#         # 3. Hardcoded JD
#         jd_text = """
#         We are looking for a versatile full-stack developer with strong experience in the MERN stack (MongoDB, Express.js, React, Node.js) 
#         along with solid programming skills in Python, Java, and C++. The ideal candidate should be proficient in building RESTful APIs, 
#         working with SQL and NoSQL databases, and designing scalable backend systems. Experience in machine learning, data science, and 
#         related Python libraries such as pandas, scikit-learn, and TensorFlow is highly desirable. Familiarity with data structures, 
#         algorithms, and cloud platforms (e.g., AWS) is a plus. Strong problem-solving skills and the ability to work in cross-functional teams are essential.
#         """

#         # 4. Analyze using Cloudinary URL
#         analysis = analyze_resume_against_jd(resume_url=resume_url, jd_text=jd_text)
#         resume_text = analysis.get("resumeText", "")  # Ensure for feedback

#         # 5. Generate AI feedback
#         feedback = generate_feedback(
#             resume_text=resume_text,
#             analysis_results=analysis
#         )
#         analysis["aiFeedback"] = feedback

#         return {
#             "message": "Guest resume analyzed successfully",
#             "resumeUrl": resume_url,
#             **analysis
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error analyzing guest resume: {str(e)}")
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
from bson import ObjectId
from datetime import datetime
from database import resume_collection
from utils import upload_pdf_to_cloudinary
from calculation import analyze_resume_against_jd
from ai_feedback import generate_feedback
from auth_utils import get_current_user
from ml_executor import execute_ml_work
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload-resume-analyze")
async def upload_and_analyze_resume(
    file: Optional[UploadFile] = File(None),
    jd_text: str = Form(...),
    drive_url: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),  # 🆕 NEW: Company name
    company_url: Optional[str] = Form(None),   # 🆕 NEW: Company website URL
    user=Depends(get_current_user),
):
    logger.info(f"📩 Received request from user: {user['email']}")
    logger.info(f"📎 File uploaded: {bool(file)}")
    logger.info(f"🔗 Drive URL received: {drive_url}")
    logger.info(f"🏢 Company Name: {company_name}")
    logger.info(f"🌐 Company URL: {company_url}")

    if not file and not drive_url:
        raise HTTPException(status_code=400, detail="Please upload a resume or provide a Google Drive link.")

    try:
        # Determine which URL to analyze (Cloudinary or Google Drive)
        resume_url = ""
        if file:
            if file.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail="Only PDF files are supported.")
            logger.info("📤 Uploading to Cloudinary...")
            resume_url = upload_pdf_to_cloudinary(file.file)
            logger.info(f"✅ Uploaded to: {resume_url}")
        else:
            resume_url = drive_url.strip()
            logger.info(f"✅ Using provided Google Drive link: {resume_url}")

        # Store resume document
        resume_doc = {
            "email": user["email"],
            "resumeUrl": resume_url,
            "driveUrl": drive_url.strip() if drive_url else "NULL",
            "companyName": company_name.strip() if company_name else "N/A",  # 🆕 Store company name
            "companyUrl": company_url.strip() if company_url else "N/A",      # 🆕 Store company URL
            "aiFeedback": "",
            "scores": {
                "skillScore": None,
                "tfidfScore": None,
                "bertScore": None,
                "hybridScore": None,
            },
            "uploadedAt": datetime.utcnow(),
        }

        result = resume_collection.insert_one(resume_doc)
        resume_id = str(result.inserted_id)

        # 🚀 Perform RAG-enhanced analysis in ThreadPool (NON-BLOCKING)
        logger.info("🚀 Starting ML analysis in background thread...")
        analysis = await execute_ml_work(
            analyze_resume_against_jd,
            resume_url=resume_url,
            jd_text=jd_text,
            company_name=company_name,
            company_url=company_url
        )
        logger.info("✅ ML analysis completed")
        
        # Add JD text to analysis for feedback generation
        analysis["jdText"] = jd_text
        
        resume_text = analysis.get("resumeText", "")

        # 🤖 Generate AI feedback in ThreadPool (NON-BLOCKING)
        logger.info("🤖 Generating AI feedback in background thread...")
        feedback = await execute_ml_work(
            generate_feedback,
            resume_text=resume_text,
            analysis_results=analysis
        )
        logger.info("✅ AI feedback generated")

        analysis["aiFeedback"] = feedback

        # Update document with scores and feedback
        resume_collection.update_one(
            {"_id": ObjectId(resume_id)},
            {
                "$set": {
                    "scores.skillScore": analysis["skillScore"],
                    "scores.tfidfScore": analysis["tfidfScore"],
                    "scores.bertScore": analysis["bertScore"],
                    "scores.hybridScore": analysis["hybridScore"],
                    "aiFeedback": feedback,
                    "ragData": analysis.get("ragData", {}),  # 🆕 Store RAG data
                }
            },
        )

        return {
            "message": "Resume uploaded and analyzed successfully",
            "resumeId": resume_id,
            "resumeUrl": resume_url,
            "driveUrl": drive_url.strip() if drive_url else "",
            "companyName": company_name if company_name else "N/A",  # 🆕 Return company name
            "companyUrl": company_url if company_url else "N/A",      # 🆕 Return company URL
            **analysis
        }

    except Exception as e:
        logger.error(f"❌ Error during resume analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/guest-analyze")
async def analyze_guest_resume():
    try:
        resume_url = "https://res.cloudinary.com/dloh7csm6/raw/upload/v1752328644/bbaexcathzjznjeixvo5.pdf"

        # Hardcoded JD
        jd_text = """
        We are looking for a versatile full-stack developer with strong experience in the MERN stack (MongoDB, Express.js, React, Node.js) 
        along with solid programming skills in Python, Java, and C++. The ideal candidate should be proficient in building RESTful APIs, 
        working with SQL and NoSQL databases, and designing scalable backend systems. Experience in machine learning, data science, and 
        related Python libraries such as pandas, scikit-learn, and TensorFlow is highly desirable. Familiarity with data structures, 
        algorithms, and cloud platforms (e.g., AWS) is a plus. Strong problem-solving skills and the ability to work in cross-functional teams are essential.
        """

        # 🚀 Analyze with RAG (no company info for guest) in ThreadPool
        logger.info("🚀 Starting guest resume analysis in background thread...")
        analysis = await execute_ml_work(
            analyze_resume_against_jd,
            resume_url=resume_url,
            jd_text=jd_text,
            company_name=None,
            company_url=None
        )
        logger.info("✅ Guest resume analysis completed")
        
        analysis["jdText"] = jd_text
        resume_text = analysis.get("resumeText", "")

        # Generate feedback in ThreadPool
        logger.info("🤖 Generating guest feedback in background thread...")
        feedback = await execute_ml_work(
            generate_feedback,
            resume_text=resume_text,
            analysis_results=analysis
        )
        logger.info("✅ Guest feedback generated")
        
        analysis["aiFeedback"] = feedback

        return {
            "message": "Guest resume analyzed successfully",
            "resumeUrl": resume_url,
            **analysis
        }

    except Exception as e:
        logger.error(f"❌ Error analyzing guest resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error analyzing guest resume: {str(e)}")