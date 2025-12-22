# Complete Project File Structure

## 📁 Backend Directory Structure

```
Backend/
│
├── 🚀 Core Application Files
│   ├── main.py                          # FastAPI app entry point, route registration, lifecycle events
│   └── app.py                           # (Legacy) Alternative app configuration
│
├── 🗄️ Database & Infrastructure
│   ├── database.py                      # Database singleton pattern with MongoDB connection pooling
│   ├── ml_executor.py                   # ThreadPoolExecutor for non-blocking ML operations
│   └── logging_config.py                # Centralized logging configuration with file rotation
│
├── 🔐 Authentication Module
│   ├── auth.py                          # Authentication endpoints (signup, login, logout, check-auth)
│   └── auth_utils.py                    # JWT token validation and user authentication utilities
│
├── 📤 Resume Upload & Analysis Module
│   ├── uploads.py                       # Resume upload and analysis API endpoints
│   ├── calculation.py                   # ML models: BERT, TF-IDF, RAG, scoring algorithms
│   └── ai_feedback.py                   # LLM-powered feedback generation (Groq API)
│
├── 👥 HR & User Management Module
│   ├── hr_matches.py                    # HR dashboard endpoints (top matching resumes)
│   └── getData.py                       # User data retrieval endpoints
│
├── 📊 Market Analysis Module
│   └── market_analysis/
│       ├── __init__.py                  # Package initialization
│       ├── router.py                    # Market analysis API endpoints (/market/*)
│       ├── market_analyzer.py           # Main market analysis pipeline orchestrator
│       ├── ingest.py                    # Job data ingestion and scraping orchestration
│       ├── serp_scraper.py              # Job posting scraper (web scraping)
│       ├── data_processor.py            # Data cleaning, chunking, and processing
│       ├── indexer.py                   # FAISS index building for job data
│       ├── retriever.py                 # FAISS-based semantic retrieval
│       ├── rag_store.py                 # RAG store implementation
│       ├── llm_reporter.py              # LLM-based market report generation
│       ├── market_data/                 # Generated data directory
│       │   ├── faiss_index.bin          # FAISS vector index
│       │   └── faiss_metadata.pkl       # Metadata for indexed jobs
│       └── market_analysis/             # Additional analysis data
│
├── 📋 Data Models & Schemas
│   ├── schemas.py                       # Pydantic models: UserCreate, UserLogin, UserOut
│   └── resume_Schemas.py                # Resume-related data schemas
│
├── 🛠️ Utility Files
│   ├── utils.py                         # Utility functions (JWT generation, Cloudinary upload)
│   └── setup_env.py                     # Environment setup helper script
│
├── 🧪 Testing Files
│   ├── test_all_apis.py                 # Comprehensive API endpoint testing
│   ├── test_auth.py                     # Authentication-specific tests
│   └── test_db.py                       # Database connection tests
│
├── 📈 Performance Testing
│   └── locustfile.py                    # Locust load testing configuration
│
├── 📦 Configuration & Dependencies
│   ├── requirements.txt                 # Python package dependencies
│   ├── Dockerfile                       # Docker container configuration
│   └── .env                             # Environment variables (not in git)
│
├── 📚 Documentation
│   ├── README.md                        # Main project documentation
│   ├── SETUP.md                         # Setup instructions
│   ├── IMPROVEMENTS.md                  # Code improvements documentation
│   └── PROJECT_STRUCTURE.md             # This file
│
├── 📁 Generated Directories
│   ├── logs/                            # Application logs (auto-generated)
│   │   └── app.log                      # Rotating log file (max 10MB, 5 backups)
│   ├── __pycache__/                     # Python bytecode cache (auto-generated)
│   └── venv/                            # Python virtual environment (not in git)
│
└── 📁 External Dependencies
    └── (Node modules, etc. if any)
```

---

## 📄 File Descriptions

### Core Application Files

#### `main.py`
- **Purpose**: FastAPI application entry point
- **Key Features**:
  - Application initialization
  - Route registration (auth, resume, hr, getme, market)
  - Startup/shutdown event handlers
  - Health check endpoint
  - CORS middleware configuration
- **Routes Registered**: 5 router prefixes
- **Lifecycle Events**: Startup validation, graceful shutdown

#### `database.py`
- **Purpose**: Database connection management with singleton pattern
- **Key Features**:
  - Thread-safe singleton implementation
  - Connection pooling (50 max, 10 min)
  - Automatic retry on failures
  - Graceful connection cleanup
- **Exports**: `collection`, `resume_collection`, `client`, `db`

#### `ml_executor.py`
- **Purpose**: Thread pool executor for ML operations
- **Key Features**:
  - Non-blocking ML operation execution
  - Configurable worker threads (default: 4)
  - Graceful shutdown handler
- **Usage**: `await execute_ml_work(function, *args, **kwargs)`

#### `logging_config.py`
- **Purpose**: Centralized logging configuration
- **Key Features**:
  - Console and file handlers
  - Log rotation (10MB max, 5 backups)
  - Structured formatting with timestamps
  - Log level filtering

---

### Authentication Module

#### `auth.py`
- **Endpoints**:
  - `POST /auth/signup` - User registration
  - `POST /auth/login` - User login (sets JWT cookie)
  - `POST /auth/logout` - User logout (clears cookie)
  - `GET /auth/check-auth` - Check authentication status
- **Dependencies**: `schemas.py`, `utils.py`, `database.py`

#### `auth_utils.py`
- **Functions**:
  - `get_current_user(request)` - Extract and validate JWT token
- **Returns**: User object with `_id`, `fullName`, `email`

---

### Resume Upload & Analysis Module

#### `uploads.py`
- **Endpoints**:
  - `POST /resume/upload-resume-analyze` - Upload and analyze resume
  - `POST /resume/guest-analyze` - Guest analysis (no auth)
- **Features**:
  - PDF file upload via Cloudinary
  - Google Drive URL support
  - Company information (name, URL)
  - Async ML processing via ThreadPoolExecutor

#### `calculation.py`
- **Purpose**: Core ML analysis algorithms
- **Key Functions**:
  - `extract_text_from_url()` - PDF text extraction
  - `extract_skills()` - Skill extraction using spaCy
  - `tfidf_similarity()` - TF-IDF cosine similarity
  - `bert_similarity()` - BERT embedding similarity
  - `analyze_resume_against_jd()` - Main analysis function
  - `build_faiss_index()` - RAG index building
  - `retrieve_top_chunks()` - RAG retrieval
- **ML Models**:
  - spaCy (`en_core_web_sm`)
  - SentenceTransformer (`all-MiniLM-L6-v2`)
  - FAISS (vector search)

#### `ai_feedback.py`
- **Purpose**: AI-powered feedback generation
- **Key Functions**:
  - `generate_feedback()` - Main feedback generator
  - `validate_strict_requirements()` - Field validation (CGPA, Degree, etc.)
  - `generate_feedback_with_llm()` - Groq LLM integration
  - `generate_rule_based_feedback()` - Fallback rule-based feedback
- **LLM**: Groq API (Llama 3.3 70B)

---

### HR & User Management Module

#### `hr_matches.py`
- **Endpoints**:
  - `POST /hr/top-matches` - Get top matching resumes for JD
- **Features**:
  - Parallel resume processing (asyncio.gather)
  - Email-based deduplication
  - Top 10 results ranking
  - Non-blocking ML analysis

#### `getData.py`
- **Endpoints**:
  - `GET /getme/resumes` - Get authenticated user's resumes
  - `GET /getme/?email=...` - Get resumes by email
- **Features**:
  - JWT authentication
  - Resume serialization
  - Score-based sorting

---

### Market Analysis Module

#### `market_analysis/router.py`
- **Endpoints**:
  - `POST /market/quick-analyze` - Full market analysis pipeline
  - `GET /market/health` - Health check
- **Features**:
  - Skill detection from query
  - Full pipeline execution (scrape + index + analyze)
  - LLM-powered market reports

#### `market_analysis/market_analyzer.py`
- **Purpose**: Orchestrates market analysis pipeline
- **Functions**:
  - `run_full_pipeline()` - Complete analysis workflow

#### `market_analysis/ingest.py`
- **Purpose**: Job data ingestion
- **Functions**:
  - `run_ingest()` - Scrape and process job data
  - `dedupe_scraped_results()` - Remove duplicates

#### `market_analysis/serp_scraper.py`
- **Purpose**: Web scraping for job postings
- **Features**: Rate limiting, error handling

#### `market_analysis/data_processor.py`
- **Purpose**: Data cleaning and chunking
- **Features**: Text cleaning, skill frequency analysis

#### `market_analysis/indexer.py`
- **Purpose**: FAISS index building
- **Functions**: `build_faiss_index()` - Create vector index

#### `market_analysis/retriever.py`
- **Purpose**: Semantic retrieval from FAISS index
- **Class**: `MarketRetriever` - Query interface

#### `market_analysis/llm_reporter.py`
- **Purpose**: LLM-based report generation
- **Features**: Market insights, salary analysis, recommendations

---

### Data Models & Schemas

#### `schemas.py`
- **Models**:
  - `UserCreate` - Registration input
  - `UserLogin` - Login credentials
  - `UserOut` - User output model

#### `resume_Schemas.py`
- **Models**: Resume-related data structures

---

### Utility Files

#### `utils.py`
- **Functions**:
  - `generate_token(user_id)` - JWT token generation
  - `upload_pdf_to_cloudinary(file)` - File upload to Cloudinary

#### `setup_env.py`
- **Purpose**: Environment setup helper
- **Functions**: Environment file creation, dependency checking

---

### Testing Files

#### `test_all_apis.py`
- **Purpose**: Comprehensive API testing
- **Tests**: All endpoints, authentication flow, error cases

#### `test_auth.py`
- **Purpose**: Authentication-specific tests

#### `test_db.py`
- **Purpose**: Database connection validation

---

### Configuration Files

#### `requirements.txt`
- **Key Dependencies**:
  - FastAPI, Uvicorn
  - MongoDB (pymongo)
  - ML: spaCy, SentenceTransformers, scikit-learn, FAISS, PyTorch
  - AI: Groq API
  - Utilities: PyMuPDF, Cloudinary, BeautifulSoup4

#### `Dockerfile`
- **Purpose**: Docker container configuration
- **Base**: Python 3.8+

---

## 🔄 Data Flow

### Resume Analysis Flow

```
1. User uploads resume (PDF/Drive URL)
   ↓
2. uploads.py → upload_and_analyze_resume()
   ↓
3. Cloudinary upload (if PDF file)
   ↓
4. ThreadPoolExecutor → calculation.py → analyze_resume_against_jd()
   ↓
5. ML Processing:
   - Text extraction (PyMuPDF)
   - Skill extraction (spaCy)
   - TF-IDF similarity
   - BERT embeddings
   - RAG retrieval (FAISS)
   ↓
6. Hybrid score calculation
   ↓
7. ThreadPoolExecutor → ai_feedback.py → generate_feedback()
   ↓
8. LLM feedback generation (Groq API)
   ↓
9. Store in MongoDB
   ↓
10. Return response to frontend
```

### HR Matches Flow

```
1. HR submits job description
   ↓
2. hr_matches.py → get_top_matching_resumes()
   ↓
3. Fetch all resumes from MongoDB
   ↓
4. Parallel processing (asyncio.gather):
   - analyze_single_resume() × N resumes
   - Each runs in ThreadPoolExecutor
   ↓
5. Group by email, keep best resume per email
   ↓
6. Sort by hybridScore, return top 10
   ↓
7. Return to frontend
```

---

## 🗄️ Database Schema

### Collection: `user_data`

```javascript
{
  "_id": ObjectId,
  "fullName": String,
  "email": String,        // Indexed, unique
  "password": String      // bcrypt hashed
}
```

### Collection: `resumes`

```javascript
{
  "_id": ObjectId,
  "email": String,        // Foreign key to user_data
  "resumeUrl": String,    // Cloudinary URL
  "driveUrl": String,     // Google Drive URL (optional)
  "companyName": String,
  "companyUrl": String,
  "aiFeedback": Object,   // Feedback structure
  "scores": {
    "skillScore": Number,
    "tfidfScore": Number,
    "bertScore": Number,
    "hybridScore": Number
  },
  "ragData": {
    "topChunks": Array,
    "companyInfo": String,
    "ragEnabled": Boolean
  },
  "uploadedAt": DateTime
}
```

---

## 🔐 Security Considerations

1. **Authentication**: JWT tokens with secure cookies
2. **Password Hashing**: bcrypt with salt
3. **Input Validation**: Pydantic models
4. **Environment Variables**: Sensitive data not hardcoded
5. **CORS**: Configured for specific origins
6. **Error Handling**: No sensitive data in error messages

---

## 📊 Performance Optimizations

1. **Database**: Connection pooling (50 max connections)
2. **ML Operations**: ThreadPoolExecutor (4 workers)
3. **Parallel Processing**: asyncio.gather for batch operations
4. **Caching**: ML models loaded once at startup
5. **Logging**: Rotating logs to prevent disk fill

---

## 🔄 API Request/Response Examples

See [README.md](./README.md) for detailed API documentation with examples.

---

**Last Updated**: December 2024  
**Maintained By**: Backend Development Team


