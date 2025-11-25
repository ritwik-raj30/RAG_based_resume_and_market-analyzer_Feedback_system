# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel, Field
# from typing import List, Dict, Any
# import json
# import re
# from .market_analyzer import run_full_pipeline, query_and_report

# router = APIRouter()


# class MarketAnalysisRequest(BaseModel):
#     query: str = Field(..., description="Market analysis query")
#     location: str = Field(default="United States", description="Location for job market analysis")
#     top_k: int = Field(default=5, ge=1, le=20, description="Number of top results to return")
#     use_llm: bool = Field(default=True, description="Whether to use LLM for report generation")


# def parse_llm_json_response(report_data: Dict) -> Dict:
#     """
#     Parse the nested LLM response and extract clean JSON
    
#     Input structure:
#     {
#         'provider': 'groq',
#         'result': {
#             'text': 'json\n{...}\n',
#             ...
#         }
#     }
    
#     Output: Clean parsed JSON dict
#     """
#     try:
#         # Navigate to the text field
#         if isinstance(report_data, dict):
#             # Check if it's already parsed
#             if 'demand_level' in report_data:
#                 return report_data
            
#             # Try to get text from nested structure
#             text = report_data.get('result', {}).get('text', '')
            
#             if not text and 'text' in report_data:
#                 text = report_data['text']
            
#             if not text:
#                 print("⚠️ No text found in report data")
#                 return report_data
            
#             # Remove markdown code fence if present
#             text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
#             text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
#             text = text.strip()
            
#             # Remove "json" prefix if present
#             if text.startswith('json'):
#                 text = text[4:].strip()
            
#             # Parse JSON
#             parsed = json.loads(text)
#             print("✅ Successfully parsed LLM JSON response")
#             return parsed
            
#     except json.JSONDecodeError as e:
#         print(f"❌ JSON parsing failed: {e}")
#         print(f"Raw text: {text[:200]}")
#         return {
#             "error": "Failed to parse LLM response",
#             "raw_text": str(report_data)
#         }
#     except Exception as e:
#         print(f"❌ Unexpected error: {e}")
#         return report_data


# @router.post("/quick-analyze")
# async def quick_market_analysis(request: MarketAnalysisRequest):
#     """
#     Simplified endpoint: Runs full CLI-style pipeline with user inputs.
#     Scrapes, builds index, and returns AI-powered report in one call.
#     """
#     try:
#         # Extract skills from query intelligently
#         query_lower = request.query.lower()
#         skill_keywords = [
#             "python", "javascript", "java", "react", "angular", "vue",
#             "node", "django", "flask", "aws", "azure", "docker",
#             "kubernetes", "sql", "mongodb", "machine learning", "ai",
#             "data science", "devops", "backend", "frontend", "full stack"
#         ]

#         # Detect skills from query
#         skills = [skill for skill in skill_keywords if skill in query_lower]
#         if not skills:
#             skills = ["Python", "JavaScript", "React", "Data Science", "DevOps"]
#         else:
#             skills = [skill.title() for skill in skills[:5]]

#         print(f"🚀 Running full pipeline for skills: {skills} at location: {request.location}")

#         # Step 1: Run full pipeline (scrape + index)
#         artifact_info = run_full_pipeline(
#             skills=skills,
#             location=request.location,
#             max_results=10,
#             save_to_disk=True
#         )

#         # Step 2: Run query + LLM report
#         result = query_and_report(
#             query=request.query,
#             top_k=request.top_k,
#             use_llm=request.use_llm,
#             index_path=artifact_info["index_path"],
#             metadata_path=artifact_info["metadata_path"]
#         )

#         # Step 3: Parse the LLM response properly
#         raw_report = result.get("report", {})
#         parsed_report = parse_llm_json_response(raw_report)
        
#         print(f"📊 Parsed report structure: {list(parsed_report.keys())}")

#         # Step 4: Format response for frontend
#         return {
#             "success": True,
#             "query": request.query,
#             "location": request.location,
#             "skills_analyzed": skills,
#             "total_results": len(result.get("hits", [])),
#             "hits": result.get("hits", []),
            
#             # Main report data (clean JSON)
#             "report": {
#                 "demand_level": parsed_report.get("demand_level", "UNKNOWN"),
#                 "demand_reason": parsed_report.get("demand_reason", []),
#                 "top_skills": parsed_report.get("top_skills", []),
#                 "missing_skill": parsed_report.get("missing_skill", ""),
#                 "salary_insights": parsed_report.get("salary_insights", {}),
#                 "recommendations": parsed_report.get("recommendations", "")
#             },
            
#             # Index metadata
#             "index_info": {
#                 "total_chunks": artifact_info.get("total_chunks", 0),
#                 "skills_analyzed": skills
#             },
            
#             # Raw report (for debugging)
#             "_raw_report": raw_report if request.top_k <= 5 else None
#         }

#     except Exception as e:
#         import traceback
#         error_detail = traceback.format_exc()
#         print(f"❌ Error in market analysis: {error_detail}")
        
#         raise HTTPException(
#             status_code=500, 
#             detail={
#                 "error": "Quick analysis failed",
#                 "message": str(e),
#                 "traceback": error_detail
#             }
#         )


# @router.get("/health")
# async def health_check():
#     """Simple health check endpoint"""
#     return {
#         "status": "healthy",
#         "service": "market_analysis",
#         "version": "1.0.0"
#     }
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import re
from .market_analyzer import run_full_pipeline, query_and_report

router = APIRouter()


class MarketAnalysisRequest(BaseModel):
    query: str = Field(..., description="Market analysis query")
    location: str = Field(default="United States", description="Location for job market analysis")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of top results to return")
    use_llm: bool = Field(default=True, description="Whether to use LLM for report generation")


def parse_llm_json_response(report_data: Dict) -> Dict:
    """
    Parse the nested LLM response and extract clean JSON
    """
    try:
        # Navigate to the text field
        if isinstance(report_data, dict):
            # Check if it's already parsed
            if 'demand_level' in report_data:
                return report_data
            
            # Try to get text from nested structure
            text = report_data.get('result', {}).get('text', '')
            
            if not text and 'text' in report_data:
                text = report_data['text']
            
            if not text:
                print("⚠️ No text found in report data")
                return report_data
            
            # Remove markdown code fence if present
            text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
            text = re.sub(r'^```\s*$', '', text, flags=re.MULTILINE)
            text = text.strip()
            
            # Remove "json" prefix if present
            if text.startswith('json'):
                text = text[4:].strip()
            
            # Parse JSON
            parsed = json.loads(text)
            print("✅ Successfully parsed LLM JSON response")
            return parsed
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        print(f"Raw text: {text[:200] if 'text' in locals() else 'N/A'}")
        return {
            "error": "Failed to parse LLM response",
            "raw_text": str(report_data)
        }
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return report_data


def normalize_salary_insights(salary_data: Any) -> Dict[str, str]:
    """
    Normalize salary insights to always return a proper dict structure.
    Handles cases where salary_data might be a string or improperly formatted.
    """
    if not salary_data:
        return {}
    
    # If it's already a dict with proper structure, return it
    if isinstance(salary_data, dict):
        # Filter out generic/unhelpful messages
        filtered = {}
        for key, value in salary_data.items():
            val_str = str(value).lower()
            # Skip generic messages
            if any(phrase in val_str for phrase in [
                'not explicitly mentioned',
                'not mentioned',
                'competitive benefits',
                'no specific',
                'varies'
            ]) and len(salary_data) == 1:
                continue
            filtered[key] = value
        return filtered
    
    # If it's a string, try to extract salary info
    if isinstance(salary_data, str):
        salary_str = salary_data.lower()
        # Skip if it's a generic message
        if any(phrase in salary_str for phrase in [
            'not explicitly mentioned',
            'not mentioned',
            'competitive benefits',
            'varies'
        ]):
            return {}
        
        # Try to extract salary range if present
        # Look for patterns like "$40.00 - $45.00" or "$80,000 - $120,000"
        import re
        salary_pattern = r'\$[\d,]+(?:\.\d{2})?\s*-\s*\$[\d,]+(?:\.\d{2})?'
        matches = re.findall(salary_pattern, salary_data)
        if matches:
            return {"range": matches[0]}
        
        # If there's actual content but no pattern, return as-is
        if len(salary_data.strip()) > 10:
            return {"info": salary_data}
    
    return {}


@router.post("/quick-analyze")
async def quick_market_analysis(request: MarketAnalysisRequest):
    """
    Simplified endpoint: Runs full CLI-style pipeline with user inputs.
    Scrapes, builds index, and returns AI-powered report in one call.
    """
    try:
        # Extract skills from query intelligently
        query_lower = request.query.lower()
        skill_keywords = [
            "python", "javascript", "java", "react", "angular", "vue",
            "node", "django", "flask", "aws", "azure", "docker",
            "kubernetes", "sql", "mongodb", "machine learning", "ai",
            "data science", "devops", "backend", "frontend", "full stack"
        ]

        # Detect skills from query
        skills = [skill for skill in skill_keywords if skill in query_lower]
        if not skills:
            skills = ["Python", "JavaScript", "React", "Data Science", "DevOps"]
        else:
            skills = [skill.title() for skill in skills[:5]]

        print(f"🚀 Running full pipeline for skills: {skills} at location: {request.location}")

        # Step 1: Run full pipeline (scrape + index)
        artifact_info = run_full_pipeline(
            skills=skills,
            location=request.location,
            max_results=20,  # Increased from 10 to match CLI
            save_to_disk=True
        )

        # Step 2: Run query + LLM report
        result = query_and_report(
            query=request.query,
            top_k=request.top_k,
            use_llm=request.use_llm,
            index_path=artifact_info["index_path"],
            metadata_path=artifact_info["metadata_path"]
        )

        # Step 3: Parse the LLM response properly
        raw_report = result.get("report", {})
        parsed_report = parse_llm_json_response(raw_report)
        
        print(f"📊 Parsed report structure: {list(parsed_report.keys())}")
        
        # Step 4: Normalize salary insights
        salary_insights = normalize_salary_insights(parsed_report.get("salary_insights", {}))
        print(f"💰 Normalized salary insights: {salary_insights}")

        # Step 5: Format response for frontend
        return {
            "success": True,
            "query": request.query,
            "location": request.location,
            "skills_analyzed": skills,
            "total_results": len(result.get("hits", [])),
            "hits": result.get("hits", []),
            
            # Main report data (clean JSON)
            "report": {
                "demand_level": parsed_report.get("demand_level", "UNKNOWN"),
                "demand_reason": parsed_report.get("demand_reason", []),
                "top_skills": parsed_report.get("top_skills", []),
                "missing_skill": parsed_report.get("missing_skill", ""),
                "salary_insights": salary_insights,  # Use normalized version
                "recommendations": parsed_report.get("recommendations", "")
            },
            
            # Index metadata
            "index_info": {
                "total_chunks": artifact_info.get("total_chunks", 0),
                "skills_analyzed": skills
            },
            
            # Raw report (for debugging)
            "_raw_report": raw_report if request.top_k <= 5 else None
        }

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"❌ Error in market analysis: {error_detail}")
        
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "Quick analysis failed",
                "message": str(e),
                "traceback": error_detail
            }
        )


@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": "market_analysis",
        "version": "1.0.0"
    }