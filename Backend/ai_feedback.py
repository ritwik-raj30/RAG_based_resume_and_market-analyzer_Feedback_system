# def generate_feedback(resume_text, analysis_results):
#     """
#     Plaintext AI-style feedback for resume vs JD comparison.
#     No markdown/bold symbols. Uses all caps for section headers.
#     """

#     skill_score = analysis_results.get("skillScore", 0)
#     hybrid_score = analysis_results.get("hybridScore", 0)
#     missing_skills = analysis_results.get("missingSkills", [])
#     resume_length = len(resume_text.split())

#     resume_fields = analysis_results.get("resumeFields", {})
#     jd_fields = analysis_results.get("jdFields", {})

#     feedback = []

#     # --- Skills & Similarity Feedback ---
#     feedback.append(
#         f"Based on the resume analysis, the skill relevance score is {skill_score}% and the overall compatibility (hybrid) score is {hybrid_score}%. This reflects how well your resume aligns with the job description."
#     )

#     if missing_skills:
#         feedback.append(
#             f"The following relevant skills were missing in your resume: {', '.join(missing_skills[:5])}. Consider adding them where applicable."
#         )

#     # --- Resume Content Length Feedback ---
#     if resume_length < 200:
#         feedback.append("Your resume is quite concise. You might want to elaborate more on your experience, skills, or projects.")
#     else:
#         feedback.append("Resume length appears sufficient and provides good context.")

#     # --- Section Check ---
#     if "experience" not in resume_text.lower() or "education" not in resume_text.lower():
#         feedback.append("Ensure both 'Experience' and 'Education' sections are clearly present in your resume.")

#     # --- Strict Field Validations ---
#     field_errors = []

#     # Degree
#     if jd_fields.get("degree"):
#         resume_degree = resume_fields.get("degree")
#         if not resume_degree:
#             field_errors.append(f"Degree required: {jd_fields['degree']} — but no degree was detected in your resume.")
#         elif jd_fields["degree"].lower() not in resume_degree.lower():
#             field_errors.append(f"Degree mismatch: JD expects {jd_fields['degree']}, but your resume has {resume_degree}.")

#     # Branch
#     if jd_fields.get("branch"):
#         resume_branch = resume_fields.get("branch")
#         if not resume_branch:
#             field_errors.append(f"Branch required: {jd_fields['branch']} — but no branch or stream found in resume.")
#         elif jd_fields["branch"].lower() not in resume_branch.lower():
#             field_errors.append(f"Branch mismatch: JD needs {jd_fields['branch']}, but your resume shows {resume_branch}.")

#     # CGPA
#     if jd_fields.get("cgpa"):
#         resume_cgpa = resume_fields.get("cgpa")
#         if resume_cgpa is None:
#             field_errors.append(f"CGPA required: {jd_fields['cgpa']} — but your resume does not mention any CGPA.")
#         elif resume_cgpa < jd_fields["cgpa"]:
#             field_errors.append(f"CGPA below cutoff: Required is {jd_fields['cgpa']}, but yours is {resume_cgpa}.")

#     # Experience
#     if jd_fields.get("experience"):
#         resume_exp = resume_fields.get("experience")
#         if resume_exp is None:
#             field_errors.append(f"Experience required: {jd_fields['experience']} years — but experience info is missing.")
#         elif resume_exp < jd_fields["experience"]:
#             field_errors.append(f"Experience below requirement: JD expects {jd_fields['experience']} years, but only {resume_exp} years were found.")

#     # Add all strict field error messages if there is any
#     if field_errors:
#         feedback.append("STRICT VIOLATIONS:")
#         feedback.extend(field_errors)
#         feedback.append("Based on these mismatches, your resume may not pass initial eligibility filters.")

#     # --- Final Evaluation Summary ---
#     if hybrid_score < 50:
#         feedback.append("Overall, the resume shows a low match to the role. Improve skills alignment and address eligibility gaps.")
#     elif hybrid_score < 80:
#         feedback.append("The resume shows moderate alignment. Add more relevant experience and address skill or field mismatches.")
#     else:
#         feedback.append("Your resume shows a strong match to the role. Make sure it's tailored for each job application.")

#     return {
#         "feedback": feedback,
#         "overallScore": hybrid_score,
#         "recommendations": 1
#     }
from groq import Groq
import os
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------
# Configure Groq API
# -------------------------
client = Groq(api_key=GROQ_API_KEY)

# -------------------------
# Strict Field Validation (ALWAYS RUN)
# -------------------------
def validate_strict_requirements(resume_text, analysis_results):
    """
    Check hard requirements: CGPA, Degree, Branch, Experience
    This runs REGARDLESS of LLM/rule-based feedback
    """
    resume_fields = analysis_results.get("resumeFields", {})
    jd_fields = analysis_results.get("jdFields", {})
    
    violations = []
    warnings = []
    
    # 1. Degree Check
    if jd_fields.get("degree"):
        resume_degree = resume_fields.get("degree")
        jd_degree = jd_fields["degree"]
        
        if not resume_degree:
            violations.append({
                "type": "CRITICAL",
                "field": "Degree",
                "message": f"❌ MISSING: JD requires '{jd_degree}' degree, but no degree found in resume."
            })
        elif jd_degree.lower() not in resume_degree.lower():
            violations.append({
                "type": "MISMATCH",
                "field": "Degree",
                "message": f"⚠️ MISMATCH: JD expects '{jd_degree}', but resume shows '{resume_degree}'."
            })
    
    # 2. Branch Check
    if jd_fields.get("branch"):
        resume_branch = resume_fields.get("branch")
        jd_branch = jd_fields["branch"]
        
        if not resume_branch:
            violations.append({
                "type": "CRITICAL",
                "field": "Branch/Stream",
                "message": f"❌ MISSING: JD requires '{jd_branch}' branch, but no branch/stream found in resume."
            })
        elif jd_branch.lower() not in resume_branch.lower():
            violations.append({
                "type": "MISMATCH",
                "field": "Branch/Stream",
                "message": f"⚠️ MISMATCH: JD expects '{jd_branch}', but resume shows '{resume_branch}'."
            })
    
    # 3. CGPA Check
    if jd_fields.get("cgpa"):
        resume_cgpa = resume_fields.get("cgpa")
        jd_cgpa = jd_fields["cgpa"]
        
        if resume_cgpa is None:
            violations.append({
                "type": "CRITICAL",
                "field": "CGPA/GPA",
                "message": f"❌ MISSING: JD requires CGPA {jd_cgpa}+, but no CGPA mentioned in resume."
            })
        elif resume_cgpa < jd_cgpa:
            violations.append({
                "type": "CRITICAL",
                "field": "CGPA/GPA",
                "message": f"❌ BELOW CUTOFF: JD requires {jd_cgpa}, but resume shows {resume_cgpa}. This may disqualify you."
            })
        else:
            warnings.append({
                "type": "PASS",
                "field": "CGPA/GPA",
                "message": f"✅ CGPA requirement met: {resume_cgpa} >= {jd_cgpa}"
            })
    
    # 4. Experience Check
    if jd_fields.get("experience"):
        resume_exp = resume_fields.get("experience")
        jd_exp = jd_fields["experience"]
        
        if resume_exp is None:
            violations.append({
                "type": "CRITICAL",
                "field": "Experience",
                "message": f"❌ MISSING: JD requires {jd_exp}+ years of experience, but no experience info found."
            })
        elif resume_exp < jd_exp:
            violations.append({
                "type": "CRITICAL",
                "field": "Experience",
                "message": f"❌ INSUFFICIENT: JD requires {jd_exp} years, but resume shows only {resume_exp} years."
            })
        else:
            warnings.append({
                "type": "PASS",
                "field": "Experience",
                "message": f"✅ Experience requirement met: {resume_exp} >= {jd_exp} years"
            })
    
    return {
        "violations": violations,
        "warnings": warnings,
        "has_critical_issues": len([v for v in violations if v["type"] == "CRITICAL"]) > 0
    }

# -------------------------
# Generate Feedback with Groq LLM
# -------------------------
def generate_feedback_with_llm(jd_text, resume_chunks, company_info, matched_skills, 
                               tfidf_score, bert_score, hybrid_score, company_name,
                               strict_validation):
    """
    Generate RAG-enhanced feedback using Groq LLM
    Now includes strict validation context
    """
    # Prepare context from RAG chunks
    resume_context = "\n\n".join(resume_chunks) if resume_chunks else "No specific chunks available"
    
    # Add strict validation context to prompt
    violations_text = ""
    if strict_validation["violations"]:
        violations_text = "\n### ⚠️ CRITICAL ISSUES DETECTED:\n" + "\n".join(
            [f"- {v['message']}" for v in strict_validation["violations"]]
        )
    
    # Build enhanced prompt
    prompt = f"""You are an expert AI recruiter with deep knowledge of industry trends. Analyze this resume against the job description.

## Job Description:
{jd_text}

## Company Information:
{company_name if company_name != "N/A" else "Company details not provided"}
{company_info[:500] if company_info else "No company website data available"}

## Relevant Resume Sections (RAG-Retrieved):
{resume_context}

## Matching Metrics:
- Matched Skills: {matched_skills}
- TF-IDF Score: {tfidf_score:.2f}%
- BERT Semantic Score: {bert_score:.2f}%
- Overall Hybrid Score: {hybrid_score:.2f}%

{violations_text}

Provide detailed, actionable feedback in exactly 5 points:
1. **Missing Critical Skills**: What key skills are missing from the JD?
2. **Project Enhancement**: How to better phrase projects and achievements?
3. **Action Verbs & Metrics**: Specific suggestions for quantifiable results
4. **Company Alignment**: How well does the resume align with company culture/values?
5. **Overall Assessment**: Final verdict with improvement steps (mention any critical issues above)

Keep each point concise (2-3 sentences). Be direct and actionable."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI recruiter providing resume feedback with deep industry insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=700
        )
        
        llm_feedback = chat_completion.choices[0].message.content
        print("✅ LLM feedback generated successfully")
        return llm_feedback
    
    except Exception as e:
        print(f"❌ Groq API failed: {e}")
        return None

# -------------------------
# Rule-Based Feedback (Fallback)
# -------------------------
def generate_rule_based_feedback(resume_text, analysis_results, strict_validation):
    """
    Fallback rule-based feedback when LLM fails
    Now includes strict validation results
    """
    skill_score = analysis_results.get("skillScore", 0)
    hybrid_score = analysis_results.get("hybridScore", 0)
    missing_skills = analysis_results.get("missingSkills", [])
    resume_length = len(resume_text.split())

    feedback = []

    # Skills & Similarity
    feedback.append(
        f"Based on the resume analysis, the skill relevance score is {skill_score}% and the overall compatibility (hybrid) score is {hybrid_score}%. This reflects how well your resume aligns with the job description."
    )

    if missing_skills:
        feedback.append(
            f"The following relevant skills were missing in your resume: {', '.join(missing_skills[:5])}. Consider adding them where applicable."
        )

    # Resume Length
    if resume_length < 200:
        feedback.append("Your resume is quite concise. You might want to elaborate more on your experience, skills, or projects.")
    else:
        feedback.append("Resume length appears sufficient and provides good context.")

    # Section Check
    if "experience" not in resume_text.lower() or "education" not in resume_text.lower():
        feedback.append("Ensure both 'Experience' and 'Education' sections are clearly present in your resume.")

    # Final Summary based on score
    if hybrid_score < 50:
        feedback.append("Overall, the resume shows a low match to the role. Improve skills alignment and address eligibility gaps.")
    elif hybrid_score < 80:
        feedback.append("The resume shows moderate alignment. Add more relevant experience and address skill or field mismatches.")
    else:
        feedback.append("Your resume shows a strong match to the role. Make sure it's tailored for each job application.")

    return {
        "feedback": feedback,
        "overallScore": hybrid_score,
        "feedbackType": "Rule-Based"
    }

# -------------------------
# Main Feedback Generator (HYBRID APPROACH)
# -------------------------
def generate_feedback(resume_text, analysis_results):
    """
    Main feedback function - HYBRID approach:
    1. ALWAYS run strict field validation
    2. Try LLM feedback (with validation context)
    3. Fall back to rule-based if LLM fails
    4. ALWAYS append strict violations at the end
    """
    
    # STEP 1: ALWAYS validate strict requirements first
    strict_validation = validate_strict_requirements(resume_text, analysis_results)
    
    # STEP 2: Get RAG data
    rag_data = analysis_results.get("ragData", {})
    top_chunks = rag_data.get("topChunks", [])
    company_info = rag_data.get("companyInfo", "")
    rag_enabled = rag_data.get("ragEnabled", False)
    
    jd_text = analysis_results.get("jdText", "")
    company_name = analysis_results.get("companyName", "N/A")
    
    matched_skills = ", ".join(analysis_results.get("matchedSkills", []))
    tfidf_score = analysis_results.get("tfidfScore", 0)
    bert_score = analysis_results.get("bertScore", 0)
    hybrid_score = analysis_results.get("hybridScore", 0)
    
    # STEP 3: Try LLM feedback if RAG is enabled
    feedback_points = []
    feedback_type = "Rule-Based"
    
    if rag_enabled and top_chunks:
        llm_feedback = generate_feedback_with_llm(
            jd_text=jd_text,
            resume_chunks=top_chunks,
            company_info=company_info,
            matched_skills=matched_skills if matched_skills else "None",
            tfidf_score=tfidf_score,
            bert_score=bert_score,
            hybrid_score=hybrid_score,
            company_name=company_name,
            strict_validation=strict_validation
        )
        
        if llm_feedback:
            # Parse LLM feedback into list
            feedback_points = [line.strip() for line in llm_feedback.split('\n') if line.strip()]
            feedback_type = "LLM-Powered (RAG Enhanced)"
    
    # STEP 4: Fall back to rule-based if LLM failed
    if not feedback_points:
        print("⚠️ Using rule-based feedback")
        rule_based = generate_rule_based_feedback(resume_text, analysis_results, strict_validation)
        feedback_points = rule_based["feedback"]
        feedback_type = rule_based["feedbackType"]
    
    # STEP 5: ALWAYS append strict violations (regardless of LLM/rule-based)
    if strict_validation["violations"]:
        feedback_points.append("")  # Empty line for separation
        feedback_points.append("🚨 === STRICT ELIGIBILITY CHECK === 🚨")
        feedback_points.append("")
        
        for violation in strict_validation["violations"]:
            feedback_points.append(f"{violation['message']}")
        
        feedback_points.append("")
        if strict_validation["has_critical_issues"]:
            feedback_points.append(
                "⚠️ WARNING: Your resume has critical mismatches that may result in automatic rejection by ATS systems or recruiters. "
                "Address these issues immediately before applying."
            )
        else:
            feedback_points.append(
                "⚠️ Note: While these are not critical, addressing them will improve your chances."
            )
    
    # STEP 6: Add any passing checks as positive feedback
    if strict_validation["warnings"]:
        feedback_points.append("")
        feedback_points.append("✅ === REQUIREMENTS MET === ✅")
        for warning in strict_validation["warnings"]:
            feedback_points.append(warning["message"])
    
    return {
        "feedback": feedback_points,
        "overallScore": hybrid_score,
        "ragEnhanced": rag_enabled,
        "feedbackType": feedback_type,
        "strictValidation": strict_validation,
        "hasCriticalIssues": strict_validation["has_critical_issues"]
    }