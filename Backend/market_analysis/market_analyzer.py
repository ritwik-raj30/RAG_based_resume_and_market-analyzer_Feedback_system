"""
market_analyzer.py
Main orchestrator for Job Market Analysis pipeline.

Functions:
 - run_full_pipeline(skills, location, max_results)
 - index_from_last_processed(pkl_path)
 - query_and_report(query, top_k, use_llm=True)

This file assumes the following modules exist in the same folder:
 - ingest.py       (run_ingest)
 - indexer.py      (build_faiss_index)
 - retriever.py    (MarketRetriever)
 - llm_reporter.py (generate_report)
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# local imports (same folder)
from .ingest import run_ingest
from .indexer import build_faiss_index
from .retriever import MarketRetriever
from .llm_reporter import generate_report

DATA_DIR = Path(os.getenv("MARKET_DATA_DIR", "./market_analysis/market_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)


def run_full_pipeline(skills: List[str],
                      location: str = "United States",
                      max_results: int = 10,
                      save_to_disk: bool = True) -> Dict[str, Any]:
    """
    End-to-end: scrape -> dedupe -> process -> save processed pickle.
    Then build FAISS index from the saved pickle.
    Returns metadata about saved artifact paths.
    """
    print("🚀 Starting full market analysis pipeline")
    # Step A: Scrape + process (ingest.py)
    ingest_result = run_ingest(skills=skills, location=location, max_results=max_results, save_to_disk=save_to_disk)

    # ingest_result includes 'saved_to' with processed pickle path when save_to_disk=True
    processed_pkl = ingest_result.get("saved_to")
    if not processed_pkl:
        raise RuntimeError("Processed pickle path not found. Make sure run_ingest saved processed output.")

    print(f"📦 Processed data saved at: {processed_pkl}")

    # Step B: Build index (indexer.py)
    idx_result = build_faiss_index(processed_pickle_path=processed_pkl)
    print(f"🗂️ Index built: {idx_result}")

    return {
        "processed_pickle": processed_pkl,
        "index_path": idx_result["index_path"],
        "metadata_path": idx_result["metadata_path"],
        "total_chunks": idx_result["total_chunks"]
    }


def index_from_existing_pkl(processed_pkl_path: str) -> Dict[str, Any]:
    """
    Build index from an existing processed pickle file (if you already have one).
    """
    return build_faiss_index(processed_pickle_path=processed_pkl_path)


def query_and_report(query: str,
                     top_k: int = 5,
                     use_llm: bool = True,
                     index_path: Optional[str] = None,
                     metadata_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Query the FAISS retriever and produce a final report.
    If use_llm is True and llm key is configured, attempt to generate LLM-based report;
    otherwise produce a simple synthesized report from chunks.
    """
    print(f"🔍 Querying for: {query} (top_k={top_k})")

    # Instantiate retriever (uses default DATA_DIR paths if not provided)
    retr = MarketRetriever(index_path=index_path or None, metadata_path=metadata_path or None)

    hits = retr.query(query, top_k=top_k)
    print(f"🔎 Retrieved {len(hits)} hits")

    # Build a context payload for the reporter
    context = {
        "query": query,
        "top_k": top_k,
        "hits": hits
    }

    # Generate report via LLM reporter (or fallback)
    report = generate_report(context, use_llm=use_llm)
    return {
        "query": query,
        "hits": hits,
        "report": report
    }


# CLI helper for quick runs
# CLI helper for quick runs
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Market Analyzer Orchestrator")
    parser.add_argument("--skills", "-s", nargs="+", required=False, default=["Python", "React", "AI"], help="Skills to analyze")
    parser.add_argument("--location", "-l", default="United States")
    parser.add_argument("--max_results", "-n", type=int, default=10)
    parser.add_argument("--run_index", action="store_true", help="Also build FAISS index after ingest")
    parser.add_argument("--query", type=str, help="If set, run a query and produce report after index is available")
    parser.add_argument("--top_k", type=int, default=5)
    args = parser.parse_args()

    # Step 1: run ingest + index
    artifact_info = run_full_pipeline(
        skills=args.skills,
        location=args.location,
        max_results=args.max_results,
        save_to_disk=True
    )

    # Step 2: run query + LLM report if query provided
    if args.query:
        out = query_and_report(
            args.query,
            top_k=args.top_k,
            index_path=artifact_info["index_path"],
            metadata_path=artifact_info["metadata_path"],
            use_llm=True
        )

        print("\n==== REPORT ====\n")
        print(out["report"])


