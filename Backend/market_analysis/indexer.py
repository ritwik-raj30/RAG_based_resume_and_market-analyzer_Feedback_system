# indexer.py
"""
Builds FAISS index from processed job chunks.
- Loads the processed pickle file from ingest.py
- Embeds chunks using SentenceTransformer (mpnet)
- Saves FAISS index + metadata mapping
"""

import os
import pickle
import faiss
import numpy as np
from pathlib import Path
from typing import Dict, List

from sentence_transformers import SentenceTransformer

DATA_DIR = Path(os.getenv("MARKET_DATA_DIR", "./market_analysis/market_data"))
DATA_DIR.mkdir(exist_ok=True, parents=True)

EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-mpnet-base-v2")

INDEX_PATH = DATA_DIR / "faiss_index.bin"
META_PATH = DATA_DIR / "faiss_metadata.pkl"


def build_faiss_index(processed_pickle_path: str,
                       index_save_path: str = str(INDEX_PATH),
                       metadata_save_path: str = str(META_PATH)):
    """
    processed_pickle_path: Path to processed_jobs_*.pkl from ingest.py
    """
    print("🚀 Loading processed data...")
    with open(processed_pickle_path, "rb") as f:
        processed = pickle.load(f)

    chunks = processed["all_chunks"]
    if not chunks:
        raise ValueError("No chunks found to index.")

    print(f"📦 Loaded {len(chunks)} chunks")

    # Load embedding model
    print("🔢 Loading embedding model:", EMBED_MODEL)
    model = SentenceTransformer(EMBED_MODEL)

    # Compute embeddings in batches
    BATCH = 64
    all_embeddings = []

    print("⚙️ Generating embeddings...")
    for i in range(0, len(chunks), BATCH):
        batch = [c["cleaned_chunk"] for c in chunks[i:i+BATCH]]
        emb = model.encode(batch, normalize_embeddings=True)
        all_embeddings.append(emb)

    embeddings = np.vstack(all_embeddings).astype("float32")
    print(f"🧠 Embeddings shape: {embeddings.shape}")

    # Build FAISS index (cosine similarity → using inner product)
    dim = embeddings.shape[1]
    index = faiss.IndexIDMap(faiss.IndexFlatIP(dim))

    print("📥 Adding embeddings to FAISS index...")
    ids = np.arange(len(embeddings)).astype("int64")
    index.add_with_ids(embeddings, ids)

    # Save index
    print("💾 Saving FAISS index to:", index_save_path)
    faiss.write_index(index, index_save_path)

    # Save metadata (mapping ID → chunk info)
    print("💾 Saving metadata to:", metadata_save_path)
    metadata = {i: chunks[i] for i in range(len(chunks))}

    with open(metadata_save_path, "wb") as f:
        pickle.dump(metadata, f)

    print("🎉 Index build complete!")
    return {
        "index_path": index_save_path,
        "metadata_path": metadata_save_path,
        "total_chunks": len(chunks)
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build FAISS index from processed data")
    parser.add_argument("--pkl", required=True, help="Path to processed_jobs pickle file")
    args = parser.parse_args()

    build_faiss_index(args.pkl)
