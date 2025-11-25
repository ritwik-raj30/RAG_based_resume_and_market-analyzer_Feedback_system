"""
SerpAPI Integration for Job Market Data Collection (clean, import-safe)
- Loads env from .env (optional)
- Uses SERPAPI_KEY from environment
- Uses jobs_results length as fallback when total_results is missing/zero
- No test/main block so it's safe to import
"""

import os
import time
import requests
from typing import List, Dict
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
if not SERPAPI_KEY:
    # Don't hardcode keys here; raise so developers remember to set env
    raise RuntimeError("SERPAPI_KEY not set in environment")

SERPAPI_BASE_URL = "https://serpapi.com/search"


class JobScraper:
    def __init__(self, api_key: str = None, rate_limit_delay: float = 1.0):
        self.api_key = api_key or SERPAPI_KEY
        self.rate_limit_delay = float(rate_limit_delay)

    def scrape_skill_jobs(self, skill: str, location: str = "United States",
                          max_results: int = 10) -> Dict:
        """
        Scrape job postings for a specific skill

        Returns a dict:
        {
            "skill": skill,
            "total_jobs": int,
            "job_descriptions": [ {title, company, description, full_text} ],
            "related_skills": [...],
            "search_query": query
        }
        """
        print(f"🔍 Scraping jobs for: {skill} (location: {location}, max: {max_results})")

        query = f"{skill} developer"

        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": self.api_key,
            "num": max_results
        }

        try:
            resp = requests.get(SERPAPI_BASE_URL, params=params, timeout=12)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            print(f"❌ Error scraping {skill}: {e}")
            return {
                "skill": skill,
                "total_jobs": 0,
                "job_descriptions": [],
                "related_skills": [],
                "search_query": query,
                "error": str(e)
            }

        # Best-effort extraction
        total_results = data.get("search_information", {}).get("total_results", 0)
        jobs = data.get("jobs_results", []) or []

        # Fallback: if total_results is zero or missing, use number of returned jobs
        if not total_results or total_results == 0:
            total_results = len(jobs)

        job_descriptions = []
        related_skills = set()

        for job in jobs:
            title = (job.get("title") or "").strip()
            company = (job.get("company_name") or job.get("company") or "").strip()
            description = (job.get("description") or job.get("snippet") or "").strip()
            full_text = f"{title}. {description}" if title or description else ""

            job_descriptions.append({
                "title": title,
                "company": company,
                "description": description,
                "full_text": full_text
            })

            # Extract simple keywords (lowercased)
            extracted = self._extract_skills_from_text(description)
            related_skills.update(extracted)

        print(f"✅ Found {total_results:,} jobs for {skill} (returned: {len(job_descriptions)})")
        return {
            "skill": skill,
            "total_jobs": int(total_results),
            "job_descriptions": job_descriptions,
            "related_skills": sorted(list(related_skills)),
            "search_query": query
        }

    def scrape_multiple_skills(self, skills: List[str], location: str = "United States",
                               max_results: int = 10) -> List[Dict]:
        results = []
        for i, skill in enumerate(skills):
            results.append(self.scrape_skill_jobs(skill, location=location, max_results=max_results))
            if i < len(skills) - 1:
                print(f"⏳ Waiting {self.rate_limit_delay}s before next request...")
                time.sleep(self.rate_limit_delay)
        return results

    def _extract_skills_from_text(self, text: str) -> List[str]:
        if not text:
            return []
        text_lower = text.lower()
        skill_keywords = {
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
            "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
            "git", "jenkins", "ci/cd", "agile", "scrum",
            "machine learning", "deep learning", "llm", "rag", "langchain",
            "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy"
        }
        found = [kw for kw in skill_keywords if kw in text_lower]
        return found
