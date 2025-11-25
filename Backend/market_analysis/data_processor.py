"""
Data Processing Pipeline for Job Market Analysis
Cleans, chunks, and prepares data for RAG storage
"""

import re
from typing import List, Dict
from bs4 import BeautifulSoup
from collections import Counter

class JobDataProcessor:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size
    
    def process_scraped_data(self, scraped_results: List[Dict]) -> Dict:
        """
        Process raw scraped data into clean, structured format
        
        Args:
            scraped_results: List of results from JobScraper
        
        Returns:
            {
                "processed_jobs": [...],
                "all_chunks": [...],
                "skill_frequency": {...},
                "statistics": {...}
            }
        """
        print("🔧 Processing scraped job data...")
        
        all_jobs = []
        all_chunks = []
        skill_counter = Counter()
        
        for result in scraped_results:
            skill = result["skill"]
            job_descriptions = result.get("job_descriptions", [])
            
            for job in job_descriptions:
                # Clean description
                clean_desc = self.clean_text(job["description"])
                
                # Create chunks
                chunks = self.chunk_text(clean_desc, job["title"], skill)
                all_chunks.extend(chunks)
                
                # Process job
                processed_job = {
                    "skill": skill,
                    "title": job["title"],
                    "company": job["company"],
                    "clean_description": clean_desc,
                    "word_count": len(clean_desc.split()),
                    "chunks": len(chunks)
                }
                all_jobs.append(processed_job)
            
            # Count skill frequency
            for related_skill in result.get("related_skills", []):
                skill_counter[related_skill] += 1
        
        # Statistics
        stats = {
            "total_jobs_processed": len(all_jobs),
            "total_chunks_created": len(all_chunks),
            "avg_chunks_per_job": len(all_chunks) / len(all_jobs) if all_jobs else 0,
            "unique_skills_found": len(skill_counter),
            "most_common_skills": skill_counter.most_common(10)
        }
        
        print(f"✅ Processed {len(all_jobs)} jobs into {len(all_chunks)} chunks")
        print(f"📊 Found {len(skill_counter)} unique skills")
        
        return {
            "processed_jobs": all_jobs,
            "all_chunks": all_chunks,
            "skill_frequency": dict(skill_counter),
            "statistics": stats
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean HTML and formatting from text
        """
        # Remove HTML tags
        text = BeautifulSoup(text, "html.parser").get_text()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters (keep basic punctuation)
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, title: str, skill: str) -> List[Dict]:
        """
        Split text into chunks for RAG storage
        Each chunk includes metadata for better retrieval
        """
        if not text:
            return []
        
        chunks = []
        words = text.split()
        
        # Create overlapping chunks
        for i in range(0, len(words), self.chunk_size - 50):  # 50 word overlap
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append({
                "cleaned_chunk": chunk_text,
                "text": chunk_text,
                "metadata": {
                    "skill": skill,
                    "title": title,
                    "chunk_index": len(chunks),
                    "word_count": len(chunk_words)
                }
            })
        
        return chunks
    
    def extract_skill_patterns(self, all_chunks: List[Dict]) -> Dict[str, List[str]]:
        """
        Identify common skill co-occurrence patterns
        E.g., "Python jobs often require AWS and Docker"
        """
        skill_patterns = {}
        
        for chunk in all_chunks:
            skill = chunk["metadata"]["skill"]
            text_lower = chunk["text"].lower()
            
            # Common tech skills to look for
            tech_keywords = [
                "python", "java", "javascript", "react", "node.js",
                "aws", "docker", "kubernetes", "mongodb", "postgresql",
                "machine learning", "llm", "rag", "api", "rest"
            ]
            
            found_skills = [kw for kw in tech_keywords if kw in text_lower]
            
            if skill not in skill_patterns:
                skill_patterns[skill] = []
            
            skill_patterns[skill].extend(found_skills)
        
        # Count frequency for each skill
        for skill in skill_patterns:
            counter = Counter(skill_patterns[skill])
            skill_patterns[skill] = counter.most_common(5)
        
        return skill_patterns
    
    def analyze_skill_demand(self, scraped_results: List[Dict]) -> Dict:
        """
        Analyze and categorize skill demand levels
        """
        demand_analysis = {
            "high_demand": [],
            "medium_demand": [],
            "low_demand": [],
            "very_low_demand": []
        }
        
        for result in scraped_results:
            skill = result["skill"]
            total_jobs = result["total_jobs"]
            
            analysis = {
                "skill": skill,
                "job_count": total_jobs,
                "job_count_formatted": f"{total_jobs:,}"
            }
            
            # Categorize
            if total_jobs >= 10000:
                demand_analysis["high_demand"].append(analysis)
            elif total_jobs >= 5000:
                demand_analysis["medium_demand"].append(analysis)
            elif total_jobs >= 1000:
                demand_analysis["low_demand"].append(analysis)
            else:
                demand_analysis["very_low_demand"].append(analysis)
        
        # Sort by job count
        for category in demand_analysis:
            demand_analysis[category].sort(key=lambda x: x["job_count"], reverse=True)
        
        return demand_analysis
    
    def identify_trending_skills(self, skill_frequency: Dict[str, int], 
                                 top_n: int = 10) -> List[Dict]:
        """
        Identify most frequently mentioned skills across all jobs
        """
        sorted_skills = sorted(skill_frequency.items(), 
                              key=lambda x: x[1], 
                              reverse=True)[:top_n]
        
        trending = []
        for skill, count in sorted_skills:
            trending.append({
                "skill": skill.title(),
                "mentions": count,
                "trend": "🔥" if count > 20 else "⚡" if count > 10 else "📊"
            })
        
        return trending


# -------------------------
# Domain Grouping
# -------------------------
DOMAIN_MAPPING = {
    "AI & Machine Learning": [
        "python", "pytorch", "tensorflow", "machine learning", 
        "deep learning", "llm", "rag", "langchain", "hugging face"
    ],
    "Web Development": [
        "javascript", "typescript", "react", "angular", "vue",
        "node.js", "express", "html", "css", "next.js"
    ],
    "Backend Development": [
        "python", "java", "go", "rust", "django", "flask",
        "fastapi", "spring", "api", "rest", "graphql"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes",
        "terraform", "jenkins", "ci/cd", "linux"
    ],
    "Data Engineering": [
        "python", "sql", "spark", "kafka", "airflow",
        "etl", "data pipeline", "bigquery", "snowflake"
    ],
    "Mobile Development": [
        "react native", "flutter", "swift", "kotlin",
        "ios", "android", "mobile"
    ]
}

def group_skills_by_domain(scraped_results: List[Dict]) -> Dict:
    """
    Group analyzed skills into domains and calculate domain totals
    """
    domain_jobs = {}
    skill_to_jobs = {r["skill"].lower(): r["total_jobs"] for r in scraped_results}
    
    for domain, domain_skills in DOMAIN_MAPPING.items():
        total_jobs = 0
        matched_skills = []
        
        for domain_skill in domain_skills:
            for analyzed_skill, job_count in skill_to_jobs.items():
                if domain_skill in analyzed_skill.lower():
                    total_jobs += job_count
                    matched_skills.append({
                        "skill": analyzed_skill,
                        "jobs": job_count
                    })
        
        if matched_skills:
            domain_jobs[domain] = {
                "total_jobs": total_jobs,
                "matched_skills": sorted(matched_skills, 
                                        key=lambda x: x["jobs"], 
                                        reverse=True)[:5],  # Top 5 skills
                "skill_count": len(matched_skills)
            }
    
    # Sort domains by total jobs
    sorted_domains = sorted(domain_jobs.items(), 
                           key=lambda x: x[1]["total_jobs"], 
                           reverse=True)
    
    return dict(sorted_domains)


# -------------------------
# Test Function
# -------------------------
if __name__ == "__main__":
    # Mock scraped data for testing
    mock_data = [
        {
            "skill": "Python",
            "total_jobs": 15234,
            "job_descriptions": [
                {
                    "title": "Python Developer",
                    "company": "TechCorp",
                    "description": "We need a <b>Python developer</b> with experience in Django, AWS, and Docker. Must know REST APIs and PostgreSQL."
                }
            ],
            "related_skills": ["django", "aws", "docker", "postgresql"]
        }
    ]
    
    processor = JobDataProcessor()
    result = processor.process_scraped_data(mock_data)
    
    print("\n📊 Processing Results:")
    print(f"Jobs: {result['statistics']['total_jobs_processed']}")
    print(f"Chunks: {result['statistics']['total_chunks_created']}")
    print(f"Skills: {result['statistics']['unique_skills_found']}")
