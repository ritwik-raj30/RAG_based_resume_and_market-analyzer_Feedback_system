"""
llm_reporter.py
Generates a market analysis report from retrieved chunks.

Behavior:
 - If environment GROQ_API_KEY or OPENAI_API_KEY is present and 'use_llm' is True,
   this will construct a prompt and attempt to call an LLM (placeholder).
 - Otherwise it will synthesize a concise report from the hits (simple heuristic).
 
NOTE: This file does NOT embed any secret keys. Provide them via env variables.
"""

import os
import textwrap
from typing import Dict, Any, List

# optional HTTP client for calling an LLM API if configured
import requests

from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Configure which model / service to use via env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # options: "groq", "openai", "none"

def _build_prompt(context: Dict[str, Any]) -> str:
    """
    Build a concise LLM prompt from the context (hits).
    """
    q = context.get("query", "")
    hits = context.get("hits", [])
    summary_docs = []
    for i, h in enumerate(hits):
        title = h.get("source_job_title") or h.get("skill") or "Unknown title"
        comp = h.get("source_company") or ""
        score = h.get("score", 0)
        text_snippet = (h.get("chunk_text") or "")[:700]
        summary_docs.append(f"{i+1}. [{title} @ {comp}] (score: {score:.3f})\n{text_snippet}")

    docs_block = "\n\n".join(summary_docs)
    prompt = f"""
You are a job market analyst. Given the query: "{q}", and the following job snippets, produce:
1) A short demand summary (HIGH / MEDIUM / LOW + bullet justification)
2) Top 5 related skills appearing in these snippets
3) One suggested missing high-value skill to learn (and why)
4) Salary guidance if present in snippets (optional)

Documents:
{docs_block}

Answer succinctly in JSON with fields: demand_level, demand_reason, top_skills, missing_skill, salary_insights, recommendations.
"""
    return textwrap.dedent(prompt).strip()


def _call_llm_stub(prompt: str) -> Dict[str, Any]:
    """
    Placeholder LLM call. Replace this with a real Groq/OpenAI API call.
    For now, return a naive synthesized JSON from heuristics.
    """
    # Fallback simple heuristic synthesis (not a real LLM)
    # Count mentions of obvious keywords in the prompt
    txt = prompt.lower()
    top_skills = []
    for k in ["python", "react", "aws", "docker", "kubernetes", "pytorch", "tensorflow", "node.js", "postgresql"]:
        if k in txt:
            top_skills.append(k)
    top_skills = top_skills[:5]

    demand_level = "MEDIUM"
    if "python" in txt or "machine learning" in txt:
        demand_level = "HIGH"

    return {
        "demand_level": demand_level,
        "demand_reason": f"Simple heuristic: matched keywords {top_skills}",
        "top_skills": top_skills,
        "missing_skill": "docker" if "docker" not in top_skills else "kubernetes",
        "salary_insights": None,
        "recommendations": ["Learn Docker + Kubernetes", "Practice building REST APIs", "Build portfolio projects"]
    }


def _call_groq(prompt: str) -> Dict[str, Any]:
    """
    Calls Groq's chat completion API using llama3-70b.
    Returns the assistant-generated text as a dict.
    """

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set in environment")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a job market analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 800
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=20)
    
    # ADD THIS: Print the error response
    if not resp.ok:
        print(f"Error Status: {resp.status_code}")
        print(f"Error Response: {resp.text}")
    
    resp.raise_for_status()
    data = resp.json()

    assistant_reply = data["choices"][0]["message"]["content"]

    return {
        "provider": "groq",
        "text": assistant_reply,
        "raw": data
    }



def generate_report(context: Dict[str, Any], use_llm: bool = True) -> Dict[str, Any]:
    """
    Generates a report for the given context.
    If use_llm is True and LLM provider env is configured, try to call it.
    Otherwise return a heuristic report.
    """
    prompt = _build_prompt(context)

    if use_llm and LLM_PROVIDER.lower() == "groq" and GROQ_API_KEY:
        try:
            out = _call_groq(prompt)
            return {"provider": "groq", "result": out}
        except Exception as e:
            # fallback to stub
            return {"provider": "groq", "error": str(e), "result": _call_llm_stub(prompt)}

    if use_llm and LLM_PROVIDER.lower() == "openai" and OPENAI_API_KEY:
        # You can implement OpenAI call here (left as exercise)
        try:
            # placeholder - user to implement
            return {"provider": "openai", "result": "openai-call-not-implemented"}
        except Exception as e:
            return {"provider": "openai", "error": str(e), "result": _call_llm_stub(prompt)}

    # Default heuristic response (no LLM)
    return {"provider": "heuristic", "result": _call_llm_stub(prompt)}
