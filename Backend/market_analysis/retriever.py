# retriever.py
"""
Retriever utility to query FAISS index.
"""

import os
import pickle
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict

from sentence_transformers import SentenceTransformer

DATA_DIR = Path(os.getenv("MARKET_DATA_DIR", "./market_analysis/market_data"))
INDEX_PATH = DATA_DIR / "faiss_index.bin"
META_PATH = DATA_DIR / "faiss_metadata.pkl"

EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-mpnet-base-v2")


class MarketRetriever:
    def __init__(self,
                 index_path: str = str(INDEX_PATH),
                 metadata_path: str = str(META_PATH)):
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at: {index_path}")

        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata not found at: {metadata_path}")

        print("📥 Loading FAISS index...")
        self.index = faiss.read_index(index_path)

        print("📥 Loading metadata...")
        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

        print(f"📦 Loaded metadata for {len(self.metadata)} items")

        self.model = SentenceTransformer(EMBED_MODEL)

    def query(self, text: str, top_k: int = 5) -> List[Dict]:
        """
        Returns top-k job chunks matching the query.
        """
        # Embed query
        q_emb = self.model.encode([text], normalize_embeddings=True).astype("float32")

        # Search
        scores, ids = self.index.search(q_emb, top_k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue

            meta = self.metadata[idx]

            results.append({
                "chunk_id": int(idx),
                "score": float(score),
                "chunk_text": meta["cleaned_chunk"],
                "skill": meta.get("skill"),
                "source_job_title": meta.get("job_title"),
                "source_company": meta.get("company"),
                "source_snippet": meta.get("original_snippet"),
                "full_job_description": meta.get("full_description")
            })

        return results


# CLI for quick testing
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Query FAISS job index")
    parser.add_argument("--q", required=True, help="Search query")
    parser.add_argument("--k", type=int, default=5, help="Top K")
    args = parser.parse_args()

    retriever = MarketRetriever()
    hits = retriever.query(args.q, top_k=args.k)

    print("\n🔍 Results:")
    for h in hits:
        print("\n--------------------")
        print(f"Score: {h['score']:.4f}")
        print(f"Skill: {h['skill']}")
        print(f"Title: {h['source_job_title']}")
        print(f"Company: {h['source_company']}")
        print("Chunk:", h["chunk_text"][:200], "...")
