"""
RAG Store using FAISS for Job Market Data
Stores and retrieves job descriptions using semantic search
"""

import faiss
import numpy as np
import pickle
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class MarketRAGStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG store with BERT embeddings
        """
        print(f"🧠 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.metadata = []
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
        print("✅ RAG Store initialized")
    
    def build_index(self, chunks: List[Dict]):
        """
        Build FAISS index from job description chunks
        
        Args:
            chunks: List of {
                "text": "job description...",
                "metadata": {"skill": "Python", "title": "..."}
            }
        """
        print(f"🔨 Building FAISS index from {len(chunks)} chunks...")
        
        if not chunks:
            print("⚠️ No chunks provided")
            return
        
        # Extract texts
        texts = [chunk["text"] for chunk in chunks]
        self.chunks = texts
        self.metadata = [chunk["metadata"] for chunk in chunks]
        
        # Create embeddings
        print("🔄 Creating embeddings...")
        embeddings = self.model.encode(texts, 
                                       show_progress_bar=True,
                                       convert_to_numpy=True)
        
        # Build FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))
        
        print(f"✅ Index built successfully with {self.index.ntotal} vectors")
    
    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """
        Query RAG store for relevant job descriptions
        
        Args:
            query_text: Search query
            top_k: Number of results to return
        
        Returns:
            List of {
                "text": "job description",
                "metadata": {...},
                "score": 0.85
            }
        """
        if self.index is None or self.index.ntotal == 0:
            print("⚠️ Index is empty")
            return []
        
        # Create query embedding
        query_embedding = self.model.encode([query_text], 
                                           convert_to_numpy=True)
        
        # Search
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            min(top_k, self.index.ntotal)
        )
        
        # Format results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):  # Valid index
                results.append({
                    "text": self.chunks[idx],
                    "metadata": self.metadata[idx],
                    "score": float(1 / (1 + distances[0][i]))  # Convert distance to similarity
                })
        
        return results
    
    def query_by_skill(self, skill: str, top_k: int = 10) -> List[Dict]:
        """
        Get job descriptions specifically for a skill
        """
        query = f"Job requirements and skills for {skill} developer positions"
        return self.query(query, top_k)
    
    def find_related_skills(self, skill: str, top_k: int = 10) -> Dict:
        """
        Find skills commonly mentioned with the given skill
        """
        results = self.query_by_skill(skill, top_k)
        
        # Extract all text and analyze
        all_text = " ".join([r["text"] for r in results])
        
        # Common tech skills
        tech_skills = [
            "python", "java", "javascript", "typescript", "go", "rust",
            "react", "angular", "vue", "node.js", "django", "flask", "fastapi",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
            "mongodb", "postgresql", "mysql", "redis",
            "machine learning", "llm", "rag", "pytorch", "tensorflow"
        ]
        
        # Count occurrences
        skill_counts = {}
        text_lower = all_text.lower()
        
        for tech_skill in tech_skills:
            if tech_skill.lower() != skill.lower():  # Exclude the query skill
                count = text_lower.count(tech_skill)
                if count > 0:
                    skill_counts[tech_skill] = count
        
        # Sort by frequency
        sorted_skills = sorted(skill_counts.items(), 
                              key=lambda x: x[1], 
                              reverse=True)[:10]
        
        return {
            "skill": skill,
            "related_skills": [
                {"skill": s[0], "mentions": s[1]} 
                for s in sorted_skills
            ],
            "context_analyzed": len(results)
        }
    
    def get_skill_context(self, skills: List[str]) -> Dict:
        """
        Get comprehensive context for multiple skills
        Used for LLM report generation
        """
        context = {}
        
        for skill in skills:
            print(f"📊 Analyzing context for: {skill}")
            
            # Get top job descriptions
            results = self.query_by_skill(skill, top_k=5)
            
            # Get related skills
            related = self.find_related_skills(skill, top_k=5)
            
            context[skill] = {
                "sample_jobs": [
                    {
                        "title": r["metadata"].get("title", "Unknown"),
                        "excerpt": r["text"][:200] + "..."
                    }
                    for r in results[:3]
                ],
                "related_skills": related["related_skills"][:5],
                "context_strength": len(results)
            }
        
        return context
    
    def save_index(self, filepath: str = "market_rag_index"):
        """Save FAISS index and metadata to disk"""
        if self.index is None:
            print("⚠️ No index to save")
            return
        
        # Save FAISS index
        faiss.write_index(self.index, f"{filepath}.faiss")
        
        # Save metadata
        with open(f"{filepath}_metadata.pkl", "wb") as f:
            pickle.dump({
                "chunks": self.chunks,
                "metadata": self.metadata
            }, f)
        
        print(f"💾 Index saved to {filepath}")
    
    def load_index(self, filepath: str = "market_rag_index"):
        """Load FAISS index and metadata from disk"""
        try:
            # Load FAISS index
            self.index = faiss.read_index(f"{filepath}.faiss")
            
            # Load metadata
            with open(f"{filepath}_metadata.pkl", "rb") as f:
                data = pickle.load(f)
                self.chunks = data["chunks"]
                self.metadata = data["metadata"]
            
            print(f"✅ Index loaded from {filepath}")
            print(f"📊 Loaded {self.index.ntotal} vectors")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load index: {e}")
            return False


# -------------------------
# Test Function
# -------------------------
if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTING RAG STORE")
    print("="*60)
    
    # Create mock chunks
    mock_chunks = [
        {
            "text": "Python developer needed with Django, AWS, and Docker experience. Must have 3+ years experience building REST APIs.",
            "metadata": {"skill": "Python", "title": "Senior Python Developer"}
        },
        {
            "text": "React frontend engineer required. Experience with TypeScript, Node.js, and modern CSS frameworks essential.",
            "metadata": {"skill": "React", "title": "Frontend Engineer"}
        },
        {
            "text": "Full-stack developer proficient in Python, React, and PostgreSQL. AWS and Docker knowledge preferred.",
            "metadata": {"skill": "Python", "title": "Full Stack Developer"}
        }
    ]
    
    # Initialize and build index
    rag_store = MarketRAGStore()
    rag_store.build_index(mock_chunks)
    
    # Test queries
    print("\n" + "="*60)
    print("🔍 TESTING QUERIES")
    print("="*60)
    
    # Query 1: Python jobs
    print("\n📌 Query: Python developer requirements")
    results = rag_store.query("What skills are needed for Python developer jobs?", top_k=2)
    
    for i, result in enumerate(results, 1):
        print(f"\n  Result {i} (Score: {result['score']:.3f})")
        print(f"  Title: {result['metadata']['title']}")
        print(f"  Text: {result['text'][:100]}...")
    
    # Query 2: Related skills
    print("\n📌 Finding skills related to Python:")
    related = rag_store.find_related_skills("Python")
    
    for skill in related["related_skills"][:5]:
        print(f"  • {skill['skill']}: {skill['mentions']} mentions")
    
    print("\n✅ Tests completed!")
