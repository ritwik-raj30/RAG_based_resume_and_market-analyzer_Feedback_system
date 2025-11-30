
import spacy
import requests
from io import BytesIO
import fitz  # PyMuPDF
import re
import torch
import torch.nn.functional as F
import json
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("⚠️ spaCy model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

# Load BERT model for RAG
try:
    bert_model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ BERT model loaded for RAG")
except Exception as e:
    print(f"⚠️ BERT model loading failed: {e}")
    bert_model = None

# # Hugging Face API Token


# Skill keywords
skill_keywords = {
    "python", "java", "c++", "sql", "react", "node.js", "django", "flask", "html", "css",
    "tensorflow", "keras", "pytorch", "mongodb", "git", "docker", "aws", "azure", "linux",
    "communication", "leadership", "problem solving", "teamwork", "javascript", "typescript",
    "next.js", "vue", "angular", "express", "fastapi", "mysql", "postgres", "firebase"
}

known_degrees = ["btech", "mtech", "b.e", "m.e", "bachelor", "master", "phd"]
known_branches = ["computer science", "information technology", "mechanical", "electrical", "electronics", "civil"]

# -------------------------
# PDF Text Extraction
# -------------------------
def extract_text_from_url(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise Exception("Failed to download PDF")
    doc = fitz.open(stream=BytesIO(response.content), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

# -------------------------
# Skill Extraction
# -------------------------
def extract_skills(text, keywords):
    text = text.lower()
    if not nlp:
        return {k for k in keywords if k in text}
    doc = nlp(text)
    return {token.text for token in doc if token.text in keywords}

# -------------------------
# Field Extraction (CGPA, Degree, Branch, Experience)
# -------------------------
def extract_fields(text):
    lower = text.lower()
    fields = {}

    # CGPA or GPA
    match = re.search(r'(?:cgpa|gpa)[^0-9]{0,5}([0-9]\.\d+)', lower)
    fields["cgpa"] = float(match.group(1)) if match else None

    # Experience
    match = re.search(r'(\d+)\+?\s*(?:years|yrs)\s+(?:of\s+)?experience', lower)
    fields["experience"] = int(match.group(1)) if match else None

    # Degree & Branch using spaCy matcher
    if nlp:
        doc = nlp(lower)

        degree_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        degree_matcher.add("DEGREE", [nlp.make_doc(d) for d in known_degrees])
        for _, start, end in degree_matcher(doc):
            fields["degree"] = doc[start:end].text
            break

        branch_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        branch_matcher.add("BRANCH", [nlp.make_doc(b) for b in known_branches])
        for _, start, end in branch_matcher(doc):
            fields["branch"] = doc[start:end].text
            break

    return fields

# -------------------------
# TF-IDF Similarity
# -------------------------
def tfidf_similarity(t1, t2):
    if not t1.strip() or not t2.strip():
        return 0.0
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([t1, t2])
    return cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100

# -------------------------
# BERT Similarity using Local Model (NO API NEEDED!)
# -------------------------
def bert_similarity(t1, t2):
    """
    Calculate semantic similarity using LOCAL SentenceTransformer model
    This is much faster and more reliable than API calls!
    """
    if not t1.strip() or not t2.strip():
        return 0.0
    
    if not bert_model:
        print("⚠️ BERT model not available, returning 0")
        return 0.0
    
    try:
        # Use the SAME local model that RAG uses
        emb1 = bert_model.encode(t1, convert_to_tensor=False)
        emb2 = bert_model.encode(t2, convert_to_tensor=False)
        
        # Calculate cosine similarity
        from numpy import dot
        from numpy.linalg import norm
        
        similarity = dot(emb1, emb2) / (norm(emb1) * norm(emb2))
        score = float(similarity) * 100
        
        print(f"✅ BERT similarity (local): {score:.2f}%")
        return score
        
    except Exception as e:
        print(f"❌ Local BERT similarity failed: {e}")
        return 0.0

# -------------------------
# Skill Match Score
# -------------------------
def skill_match_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0.0
    return (len(resume_skills & jd_skills) / len(jd_skills)) * 100

# -------------------------
# Hybrid Score
# -------------------------
def hybrid_score(skill_score, tfidf_score, bert_score, weights=(0.5, 0.2, 0.3)):
    return round(weights[0]*skill_score + weights[1]*tfidf_score + weights[2]*bert_score, 2)

# -------------------------
# RAG: Build FAISS Index
# -------------------------
def build_faiss_index(chunks):
    """Build FAISS index from text chunks using BERT embeddings"""
    if not bert_model:
        print("⚠️ BERT model not available for RAG")
        return None, None
    
    try:
        embeddings = bert_model.encode(chunks, convert_to_numpy=True)
        d = embeddings.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)
        print(f"✅ FAISS index built with {len(chunks)} chunks")
        return index, embeddings
    except Exception as e:
        print(f"❌ FAISS indexing failed: {e}")
        return None, None

# -------------------------
# RAG: Retrieve Top Chunks
# -------------------------
def retrieve_top_chunks(index, chunks, query_text, top_k=3):
    """Retrieve most relevant chunks using FAISS"""
    if not bert_model or index is None:
        return chunks[:top_k]  # Fallback to first chunks
    
    try:
        query_emb = bert_model.encode([query_text], convert_to_numpy=True)
        D, I = index.search(query_emb, k=min(top_k, len(chunks)))
        return [chunks[i] for i in I[0]]
    except Exception as e:
        print(f"❌ RAG retrieval failed: {e}")
        return chunks[:top_k]

# -------------------------
# Web Scraping: Extract Company Info
# -------------------------
def scrape_company_info(company_url):
    """Scrape basic info from company website"""
    if not company_url or company_url.strip() == "":
        return ""
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(company_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Simple text extraction (you can enhance with BeautifulSoup)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get text from common sections
        text_content = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
            text = tag.get_text(strip=True)
            if len(text) > 20:  # Filter short snippets
                text_content.append(text)
        
        company_info = " ".join(text_content[:50])  # Limit to first 50 paragraphs
        print(f"✅ Scraped {len(company_info)} chars from {company_url}")
        return company_info
    
    except Exception as e:
        print(f"⚠️ Company scraping failed: {e}")
        return ""

# -------------------------
# Main Analysis Function with RAG
# -------------------------
def analyze_resume_against_jd(resume_url, jd_text, company_name=None, company_url=None):
    """
    Enhanced resume analysis with RAG support
    """
    try:
        resume_text = extract_text_from_url(resume_url)
        resume_skills = extract_skills(resume_text, skill_keywords)
        jd_skills = extract_skills(jd_text, skill_keywords)
        resume_fields = extract_fields(resume_text)
        jd_fields = extract_fields(jd_text)

        # Calculate basic scores
        skill_score = skill_match_score(resume_skills, jd_skills)
        tfidf_score = tfidf_similarity(resume_text, jd_text)
        bert_score = bert_similarity(resume_text, jd_text)
        final_score = hybrid_score(skill_score, tfidf_score, bert_score)

        # --- RAG Enhancement ---
        rag_data = {
            "topChunks": [],
            "companyInfo": "",
            "ragEnabled": False
        }

        # Chunk resume for RA2
        chunk_size = 500
        resume_chunks = [resume_text[i:i+chunk_size] for i in range(0, len(resume_text), chunk_size)]
        
        # Build FAISS index and retrieve relevant chunks
        if bert_model:
            index, _ = build_faiss_index(resume_chunks)
            if index:
                top_chunks = retrieve_top_chunks(index, resume_chunks, jd_text, top_k=3)
                rag_data["topChunks"] = top_chunks
                rag_data["ragEnabled"] = True
                print(f"✅ RAG enabled: Retrieved {len(top_chunks)} relevant chunks")

        # Scrape company website if URL provided
        if company_url:
            company_info = scrape_company_info(company_url)
            rag_data["companyInfo"] = company_info

        return {
            "resumeText": resume_text,
            "resumeSkills": sorted(resume_skills),
            "jdSkills": sorted(jd_skills),
            "matchedSkills": sorted(resume_skills & jd_skills),
            "missingSkills": sorted(jd_skills - resume_skills),
            "resumeFields": resume_fields,
            "jdFields": jd_fields,
            "skillScore": round(skill_score, 2),
            "tfidfScore": round(tfidf_score, 2),
            "bertScore": round(bert_score, 2),
            "hybridScore": final_score,
            "ragData": rag_data,
            "companyName": company_name or "N/A",
            "companyUrl": company_url or "N/A"
        }

    except Exception as e:
        print(f"❌ Error in analysis: {e}")
        return {
            "resumeText": "",
            "resumeSkills": [], "jdSkills": [], "matchedSkills": [], "missingSkills": [],
            "resumeFields": {}, "jdFields": {},
            "skillScore": 0.0, "tfidfScore": 0.0, "bertScore": 0.0, "hybridScore": 0.0,
            "ragData": {"topChunks": [], "companyInfo": "", "ragEnabled": False},
            "companyName": "N/A", "companyUrl": "N/A"
        }
