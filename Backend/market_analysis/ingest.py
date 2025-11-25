# ingest.py
"""
Ingestion pipeline:
1) Scrape job postings for given skills using JobScraper
2) Deduplicate scraped jobs
3) Process scraped results with JobDataProcessor
4) Save processed output to disk for later indexing
"""

import os
import time
import hashlib
import pickle
from typing import List, Dict, Set
from pathlib import Path
from dotenv import load_dotenv


load_dotenv() 

# Import your cleaned modules
from .serp_scraper import JobScraper
from .data_processor import JobDataProcessor

# Config
DATA_DIR = Path(os.getenv("MARKET_DATA_DIR", "./market_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_LOCATION = os.getenv("MARKET_LOCATION", "United States")
DEFAULT_MAX_RESULTS = int(os.getenv("MARKET_MAX_RESULTS", "10"))
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
if not SERPAPI_KEY:
    raise RuntimeError("SERPAPI_KEY not set in environment. Set it before running ingest.")

# Instantiate components
scraper = JobScraper(api_key=SERPAPI_KEY)
processor = JobDataProcessor(chunk_size=int(os.getenv("CHUNK_SIZE", 500)))


# Helper - compute stable hash for a job
def job_hash(title: str, company: str, snippet: str) -> str:
    s = f"{(title or '').strip()}||{(company or '').strip()}||{(snippet or '').strip()}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def dedupe_scraped_results(scraped_results: List[Dict]) -> List[Dict]:
    """
    Deduplicate across skills and within each skill's jobs.
    Returns a new list of scraped_results with job_descriptions deduped.
    """
    seen: Set[str] = set()
    deduped_results = []

    for res in scraped_results:
        skill = res.get("skill")
        job_descriptions = res.get("job_descriptions", [])
        kept_jobs = []

        for job in job_descriptions:
            title = job.get("title", "")
            company = job.get("company", "")
            snippet = job.get("description", "")[:300]  # first 300 chars
            h = job_hash(title, company, snippet)
            if h not in seen:
                seen.add(h)
                kept_jobs.append(job)
        deduped_results.append({
            "skill": skill,
            "total_jobs": len(kept_jobs),  # note: it's the deduped count
            "job_descriptions": kept_jobs,
            "related_skills": res.get("related_skills", []),
            "search_query": res.get("search_query", "")
        })
    return deduped_results


def run_ingest(skills: List[str],
               location: str = DEFAULT_LOCATION,
               max_results: int = DEFAULT_MAX_RESULTS,
               save_to_disk: bool = True) -> Dict:
    """
    Full scrape -> process pipeline for the input skills.
    Returns a dict with processed data and paths if saved.
    """
    print("🚀 Starting ingest pipeline")
    print(f"Skills: {skills} | location: {location} | max_results: {max_results}")

    # Step 1: Scrape
    scraped = scraper.scrape_multiple_skills(skills)  # respects internal rate limiting
    print(f"🔎 Scraped {len(scraped)} skill groups")

    # Step 2: Deduplicate
    deduped = dedupe_scraped_results(scraped)
    total_jobs = sum(len(r.get("job_descriptions", [])) for r in deduped)
    print(f"🧹 After dedupe: {total_jobs} job descriptions across skills")

    # Step 3: Process (clean, chunk, skill freq)
    processed = processor.process_scraped_data(deduped)
    stats = processed.get("statistics", {})
    print(f"✅ Processed: {stats.get('total_jobs_processed')} jobs into {stats.get('total_chunks_created')} chunks")

    result = {
        "scraped_raw": scraped,
        "scraped_deduped": deduped,
        "processed": processed
    }

    # Step 4: Persist processed to disk
    if save_to_disk:
        ts = int(time.time())
        out_path = DATA_DIR / f"processed_jobs_{ts}.pkl"
        with open(out_path, "wb") as f:
            pickle.dump(processed, f)
        result["saved_to"] = str(out_path)
        print(f"💾 Processed data saved to {out_path}")

    print("🏁 Ingest pipeline finished")
    return result


# CLI helper to run from commandline
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run job market ingest pipeline")
    parser.add_argument("--skills", "-s", nargs="+", required=True, help="Skills to scrape (e.g. Python React)")
    parser.add_argument("--location", "-l", default=DEFAULT_LOCATION, help="Location for job search")
    parser.add_argument("--max_results", "-n", type=int, default=DEFAULT_MAX_RESULTS, help="Max results per skill")
    parser.add_argument("--no-save", action="store_true", help="Do not save processed output to disk")
    args = parser.parse_args()

    run_ingest(skills=args.skills, location=args.location, max_results=args.max_results, save_to_disk=not args.no_save)
