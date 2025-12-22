# Resume Analyzer Backend API

A production-grade FastAPI backend for analyzing resumes against job descriptions using advanced ML techniques including BERT embeddings, TF-IDF similarity, RAG (Retrieval-Augmented Generation), and AI-powered feedback generation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Performance Optimizations](#performance-optimizations)
- [Contributing](#contributing)

---

## 🎯 Overview

This backend provides a comprehensive resume analysis system that:

- **Analyzes resumes** against job descriptions using multiple ML models
- **Generates AI feedback** using Groq LLM (Llama 3.3 70B)
- **Provides scoring** using hybrid approach (Skills + TF-IDF + BERT similarity)
- **Offers RAG-enhanced analysis** with FAISS vector search
- **Matches resumes** for HR dashboards
- **Performs market analysis** for job trends

### Key Highlights

- ✅ **Production-Ready**: Singleton database pattern, connection pooling, proper logging
- ✅ **Scalable**: ThreadPoolExecutor for non-blocking ML operations
- ✅ **High Performance**: Parallel processing, 20x faster batch operations
- ✅ **Enterprise-Grade**: Comprehensive error handling, graceful shutdown
- ✅ **AI-Powered**: LLM-based feedback generation with strict validation

---

## ✨ Features

### Core Features

1. **Resume Upload & Analysis**
   - PDF upload or Google Drive URL
   - Multi-model analysis (Skills, TF-IDF, BERT)
   - Hybrid scoring algorithm
   - RAG-enhanced context retrieval

2. **AI-Powered Feedback**
   - Groq LLM (Llama 3.3 70B) feedback generation
   - Strict field validation (CGPA, Degree, Branch, Experience)
   - Actionable improvement suggestions
   - Company-specific insights

3. **HR Dashboard**
   - Top matching resumes for job descriptions
   - Parallel processing for multiple resumes
   - Score-based ranking
   - Email-based deduplication

4. **Market Analysis**
   - Job market scraping
   - FAISS-based semantic search
   - LLM-powered market reports
   - Salary insights and skill demand analysis

5. **Authentication & Authorization**
   - JWT-based authentication
   - Secure password hashing (bcrypt)
   - Cookie-based sessions
   - User profile management

---

## 🛠 Tech Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server

### Database
- **MongoDB** - NoSQL database with connection pooling

### ML & AI
- **spaCy** - NLP for text processing
- **SentenceTransformers** - BERT embeddings
- **scikit-learn** - TF-IDF vectorization
- **FAISS** - Vector similarity search
- **PyTorch** - Deep learning framework
- **Groq API** - LLM for feedback generation (Llama 3.3 70B)

### Utilities
- **PyMuPDF (fitz)** - PDF text extraction
- **Cloudinary** - File storage
- **BeautifulSoup4** - Web scraping
- **pydantic** - Data validation

### Authentication
- **python-jose** - JWT tokens
- **passlib** - Password hashing

---

## 📁 Project Structure

```
Backend/
│
├── 📄 main.py                    # FastAPI app entry point, route registration
├── 📄 app.py                     # (Legacy) Alternative app file
│
├── 🗄️ database.py                # Database singleton pattern with connection pooling
├── 📊 ml_executor.py             # ThreadPoolExecutor for non-blocking ML operations
├── 📝 logging_config.py          # Centralized logging configuration
│
├── 🔐 auth.py                    # Authentication endpoints (signup, login, logout)
├── 🔐 auth_utils.py              # Authentication utilities (JWT validation)
│
├── 📤 uploads.py                 # Resume upload and analysis endpoints
├── 🧮 calculation.py             # ML models (BERT, TF-IDF, RAG, scoring)
├── 🤖 ai_feedback.py             # LLM-powered feedback generation
│
├── 👥 hr_matches.py              # HR dashboard endpoints (top matching resumes)
├── 📊 getData.py                 # User data retrieval endpoints
│
├── 📋 schemas.py                 # Pydantic models (UserCreate, UserLogin, UserOut)
├── 📋 resume_Schemas.py          # Resume-related schemas
│
├── 🛠️ utils.py                   # Utility functions (JWT, Cloudinary upload)
├── 🛠️ setup_env.py               # Environment setup helper
│
├── 📊 market_analysis/           # Market analysis module
│   ├── __init__.py
│   ├── router.py                 # Market analysis API endpoints
│   ├── market_analyzer.py        # Main market analysis pipeline
│   ├── ingest.py                 # Job data ingestion
│   ├── serp_scraper.py           # Job posting scraper
│   ├── data_processor.py         # Data cleaning and processing
│   ├── indexer.py                # FAISS index building
│   ├── retriever.py              # FAISS-based retrieval
│   ├── rag_store.py              # RAG store implementation
│   └── llm_reporter.py           # LLM-based report generation
│
├── 🧪 test_all_apis.py           # Comprehensive API testing
├── 🧪 test_auth.py               # Authentication tests
├── 🧪 test_db.py                 # Database connection tests
│
├── 📈 locustfile.py              # Load testing configuration
│
├── 📦 requirements.txt           # Python dependencies
├── 🐳 Dockerfile                 # Docker configuration
│
├── 📚 README.md                  # This file
├── 📚 SETUP.md                   # Setup instructions
├── 📚 IMPROVEMENTS.md            # Code improvements documentation
│
├── 📁 logs/                      # Application logs (auto-generated)
│   └── app.log                   # Rotating log file
│
├── 📁 market_data/               # Market analysis data storage
│   └── (FAISS indexes, metadata)
│
└── 📁 __pycache__/               # Python bytecode cache
```

---

## 🏗 Architecture

### High-Level Architecture

```
┌─────────────┐
│   Frontend  │
│  (React)    │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────┐
│         FastAPI Application         │
│  ┌───────────────────────────────┐ │
│  │   API Endpoints (Routers)     │ │
│  │  - /auth                      │ │
│  │  - /resume                    │ │
│  │  - /hr                        │ │
│  │  - /getme                     │ │
│  │  - /market                    │ │
│  └──────────────┬────────────────┘ │
│                 │                   │
│  ┌──────────────▼────────────────┐ │
│  │   ThreadPoolExecutor          │ │
│  │   (ML Operations)             │ │
│  └──────────────┬────────────────┘ │
└─────────────────┼──────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ MongoDB │  │ Groq    │  │Cloudinary│
│         │  │  LLM    │  │  (Files) │
└─────────┘  └─────────┘  └─────────┘
```

### ML Pipeline Architecture

```
Resume PDF/URL
    │
    ▼
Text Extraction (PyMuPDF)
    │
    ├──► Skill Extraction (spaCy)
    ├──► Field Extraction (Regex + spaCy)
    │
    ▼
Analysis Pipeline
    ├──► Skill Matching Score
    ├──► TF-IDF Similarity
    ├──► BERT Embeddings (SentenceTransformer)
    └──► RAG Retrieval (FAISS)
    │
    ▼
Hybrid Score Calculation
    │
    ▼
AI Feedback Generation (Groq LLM)
    ├──► RAG Context
    ├──► Strict Validation
    └──► Actionable Feedback
    │
    ▼
Response to Frontend
```

### Database Architecture

```
MongoDB: resume_db
│
├── user_data (Collection)
│   ├── _id
│   ├── fullName
│   ├── email
│   └── password (hashed)
│
└── resumes (Collection)
    ├── _id
    ├── email
    ├── resumeUrl
    ├── driveUrl
    ├── companyName
    ├── companyUrl
    ├── aiFeedback
    ├── scores
    │   ├── skillScore
    │   ├── tfidfScore
    │   ├── bertScore
    │   └── hybridScore
    ├── ragData
    └── uploadedAt
```

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- Node.js 16+ (for frontend)
- spaCy English model

### Step 1: Clone Repository

```bash
cd Resume/Backend
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 4: Environment Configuration

Create a `.env` file in the Backend directory:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/resume_db
# Or MongoDB Atlas: mongodb+srv://user:password@cluster.mongodb.net/resume_db

# JWT Configuration
JWT_SECRET=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cloudinary Configuration (for file uploads)
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

# Groq API (for LLM feedback)
GROQ_API_KEY=your-groq-api-key

# Optional: Market Analysis
EMBED_MODEL=sentence-transformers/all-mpnet-base-v2
MARKET_DATA_DIR=./market_analysis/market_data
```

### Step 5: Start MongoDB

**Local MongoDB:**
```bash
mongod  # or use systemd service
```

**MongoDB Atlas:** No local setup needed, use connection string in `.env`

### Step 6: Run the Application

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

### Step 7: Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 API Documentation

### Authentication Endpoints

#### POST `/auth/signup`
Register a new user.

**Request Body:**
```json
{
  "fullName": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "_id": "user_id",
  "fullName": "John Doe",
  "email": "john@example.com"
}
```

#### POST `/auth/login`
Login user and set JWT cookie.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### POST `/auth/logout`
Logout user (clears JWT cookie).

#### GET `/auth/check-auth`
Check if user is authenticated.

---

### Resume Analysis Endpoints

#### POST `/resume/upload-resume-analyze`
Upload and analyze a resume against a job description.

**Form Data:**
- `file`: PDF file (optional if `drive_url` provided)
- `jd_text`: Job description text (required)
- `drive_url`: Google Drive URL (optional)
- `company_name`: Company name (optional)
- `company_url`: Company website URL (optional)

**Response:**
```json
{
  "message": "Resume uploaded and analyzed successfully",
  "resumeId": "resume_id",
  "resumeUrl": "cloudinary_url",
  "driveUrl": "drive_url",
  "companyName": "Company Name",
  "companyUrl": "https://company.com",
  "resumeText": "extracted text...",
  "resumeSkills": ["Python", "JavaScript", ...],
  "jdSkills": ["Python", "React", ...],
  "matchedSkills": ["Python", ...],
  "missingSkills": ["React", ...],
  "skillScore": 75.5,
  "tfidfScore": 68.2,
  "bertScore": 82.1,
  "hybridScore": 76.8,
  "aiFeedback": {
    "feedback": ["feedback point 1", "feedback point 2", ...],
    "overallScore": 76.8,
    "feedbackType": "LLM-Powered (RAG Enhanced)",
    "strictValidation": {...},
    "hasCriticalIssues": false
  },
  "ragData": {
    "topChunks": [...],
    "companyInfo": "...",
    "ragEnabled": true
  }
}
```

#### POST `/resume/guest-analyze`
Analyze a sample resume (no authentication required).

---

### HR Dashboard Endpoints

#### POST `/hr/top-matches`
Get top matching resumes for a job description.

**Form Data:**
- `jd_text`: Job description text (required)

**Response:**
```json
{
  "message": "Top matching resumes retrieved",
  "jd": "job description text...",
  "count": 10,
  "topResumes": [
    {
      "resumeId": "id",
      "email": "user@example.com",
      "resumeUrl": "url",
      "driveUrl": "drive_url",
      "matchedSkills": ["Python", ...],
      "scores": {
        "skillScore": 85.0,
        "tfidfScore": 78.5,
        "bertScore": 88.2,
        "hybridScore": 84.5
      }
    },
    ...
  ]
}
```

---

### User Data Endpoints

#### GET `/getme/resumes`
Get all resumes for the authenticated user.

**Response:**
```json
{
  "email": "user@example.com",
  "count": 3,
  "resumes": [
    {
      "id": "resume_id",
      "email": "user@example.com",
      "resumeUrl": "url",
      "driveUrl": "drive_url",
      "aiFeedback": {...},
      "scores": {...},
      "uploadedAt": "2024-01-15T10:30:00"
    },
    ...
  ]
}
```

#### GET `/getme/?email=user@example.com`
Get resumes by email (query parameter).

---

### Market Analysis Endpoints

#### POST `/market/quick-analyze`
Perform market analysis for a job query.

**Request Body:**
```json
{
  "query": "Python developer",
  "location": "United States",
  "top_k": 5,
  "use_llm": true
}
```

**Response:**
```json
{
  "success": true,
  "query": "Python developer",
  "location": "United States",
  "skills_analyzed": ["Python", "JavaScript", ...],
  "total_results": 20,
  "hits": [...],
  "report": {
    "demand_level": "HIGH",
    "demand_reason": [...],
    "top_skills": [...],
    "salary_insights": {...},
    "recommendations": "..."
  }
}
```

#### GET `/market/health`
Health check for market analysis service.

---

### Utility Endpoints

#### GET `/`
Root endpoint - API status.

**Response:**
```json
{
  "message": "Resume Analyzer Backend is running!"
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "Backend is operational",
  "database": "connected",
  "jwt_secret_configured": true
}
```

---

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MONGODB_URI` | MongoDB connection string | ✅ Yes | - |
| `JWT_SECRET` | Secret key for JWT tokens | ✅ Yes | - |
| `JWT_ALGORITHM` | JWT algorithm | ❌ No | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | ❌ No | `30` |
| `CLOUDINARY_URL` | Cloudinary credentials | ✅ Yes | - |
| `GROQ_API_KEY` | Groq API key for LLM | ✅ Yes | - |
| `EMBED_MODEL` | Embedding model name | ❌ No | `all-MiniLM-L6-v2` |
| `MARKET_DATA_DIR` | Market data directory | ❌ No | `./market_analysis/market_data` |

---

## 🏃 Running the Application

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Run with multiple workers
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or use Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker

```bash
# Build image
docker build -t resume-analyzer-backend .

# Run container
docker run -p 8000:8000 --env-file .env resume-analyzer-backend
```

---

## 🧪 Testing

### Run All Tests

```bash
python test_all_apis.py
```

### Test Authentication

```bash
python test_auth.py
```

### Test Database Connection

```bash
python test_db.py
```

### Load Testing (Locust)

```bash
locust -f locustfile.py --host=http://localhost:8000
```

Access Locust UI at: http://localhost:8089

---

## ⚡ Performance Optimizations

### 1. Database Singleton Pattern
- **Connection Pooling**: 50 max connections, 10 min connections
- **Automatic Retry**: Retries on network errors
- **Connection Reuse**: Efficient connection management

### 2. ThreadPoolExecutor for ML Operations
- **Non-Blocking**: ML work runs in background threads
- **Parallel Processing**: 4 workers for concurrent ML operations
- **Event Loop Freedom**: FastAPI stays responsive during ML processing

### 3. Parallel Resume Processing
- **HR Matches**: Processes multiple resumes simultaneously
- **20x Faster**: Batch operations are significantly faster
- **Scalable**: Handles enterprise-scale resume databases

### 4. Logging & Monitoring
- **Rotating Logs**: 10MB max, 5 backups
- **Structured Logging**: Easy to parse and analyze
- **Production-Ready**: Comprehensive error tracking

See [IMPROVEMENTS.md](./IMPROVEMENTS.md) for detailed performance improvements.

---

## 📊 Key Algorithms

### Hybrid Scoring

The final score is calculated using a weighted combination:

```
hybridScore = 0.5 × skillScore + 0.2 × tfidfScore + 0.3 × bertScore
```

- **skillScore**: Percentage of JD skills found in resume
- **tfidfScore**: TF-IDF cosine similarity (0-100)
- **bertScore**: BERT embedding cosine similarity (0-100)

### RAG (Retrieval-Augmented Generation)

1. **Chunking**: Resume text split into 500-character chunks
2. **Embedding**: BERT embeddings generated for each chunk
3. **Indexing**: FAISS index built from embeddings
4. **Retrieval**: Top-k relevant chunks retrieved based on JD similarity
5. **Context**: Retrieved chunks used as context for LLM feedback

---

## 🔒 Security Features

- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **Password Hashing**: bcrypt with salt
- ✅ **HTTPS Ready**: CORS configured for secure origins
- ✅ **Input Validation**: Pydantic models for data validation
- ✅ **SQL Injection Safe**: MongoDB (NoSQL) prevents SQL injection
- ✅ **Environment Variables**: Sensitive data not hardcoded

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is part of the Resume Analyzer application.

---

## 👥 Authors

- Backend Development Team
- ML/AI Integration Team

---

## 📞 Support

For issues, questions, or contributions, please open an issue on the repository.

---

## 🎯 Future Enhancements

- [ ] Real-time WebSocket updates for analysis progress
- [ ] Support for more file formats (DOCX, TXT)
- [ ] Advanced resume parsing (structured data extraction)
- [ ] Integration with LinkedIn API
- [ ] Resume versioning and comparison
- [ ] Multi-language support
- [ ] GraphQL API option
- [ ] Kubernetes deployment configurations

---

## 📚 Additional Documentation

- [SETUP.md](./SETUP.md) - Detailed setup instructions
- [IMPROVEMENTS.md](./IMPROVEMENTS.md) - Code improvements and architecture decisions

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Status**: Production Ready ✅
