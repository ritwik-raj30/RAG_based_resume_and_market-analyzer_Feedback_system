# 📄 **Resume Matcher Optimizer Tracker**

🌐 **Live Demo:** 👉 **https://ragresume.netlify.app/**  
Anyone can use the application directly from this link.

An **AI-powered resume analysis and matching system** built to help **job seekers improve resumes** and **HR professionals identify the best candidates** using **modern NLP, ML, and scalable backend architecture**.

---

## 🚀 **Overview**

**Resume Matcher Optimizer Tracker** analyzes resumes, extracts skills, evaluates semantic relevance, and ranks candidates against job descriptions using a **hybrid AI scoring approach**.

The system is designed with **performance, scalability, and real-world production use cases** in mind.

---

## ✨ **Key Features**

### 👤 **For Job Seekers**
- 📤 Upload and analyze resumes (PDF)
- 🧠 AI-generated improvement feedback
- 📊 Skill matching and similarity scores
- 🕒 Resume analysis history tracking
- 📈 **Market Analysis** using Google SERP API + RAG insights

### 🧑‍💼 **For HR Professionals**
- 📝 Upload detailed job descriptions
- 🏆 AI-powered resume ranking
- ⚖️ Multiple scoring algorithms:
  - Skill Match
  - TF-IDF Similarity
  - BERT Semantic Similarity
- 🔍 View matched skills per candidate
- 📄 Direct resume access via stored links

---

## 🧠 **Scoring Algorithm**

A **hybrid weighted scoring model** ensures both **keyword accuracy** and **semantic understanding**:

| Algorithm | Weight |
|---------|--------|
| **Skill Matching (spaCy)** | **50%** |
| **BERT Similarity (Sentence Transformers)** | **30%** |
| **TF-IDF Similarity** | **20%** |

---

## 🏗️ **System Architecture**

The application follows a **Three-Tier Architecture**:

### **1️⃣ Presentation Tier**
- ⚛️ React 19 frontend
- 🔐 JWT-based authentication
- 🧠 Zustand for global state management

### **2️⃣ Application Tier**
- ⚡ FastAPI backend
- 🧩 Modular router-based design
- 🧵 Non-blocking ML execution using **ThreadPoolExecutor**
- 🚀 Parallel resume processing using **asyncio.gather**

### **3️⃣ Data Tier**
- 🗄️ MongoDB with singleton connection pooling
- ☁️ Cloudinary for PDF storage
- 🤖 Groq LLM API for AI feedback
- 🌍 Google SERP API for market insights

---

## 🛠️ **Technology Stack**

### 🎨 **Frontend**
- React 19
- React Router
- Zustand
- Axios
- Tailwind CSS
- Framer Motion
- React Hot Toast

### ⚙️ **Backend**
- FastAPI
- Uvicorn (ASGI)
- MongoDB (motor + pymongo)
- Pydantic
- JWT (python-jose, bcrypt, passlib)

### 🧠 **ML & NLP**
- spaCy (`en_core_web_sm`)
- Sentence Transformers (MiniLM)
- scikit-learn (TF-IDF)
- FAISS (vector search)
- PyMuPDF (PDF parsing)
- NumPy, PyTorch

### 🌐 **External Services**
- **Cloudinary** – Resume storage
- **Groq API (LLaMA 3.3 70B)** – AI feedback
- **Google SERP API** – Market analysis

---

## ⚡ **Performance & Scalability**

- ✅ Non-blocking FastAPI event loop
- 🔁 ThreadPoolExecutor for CPU-heavy ML tasks
- 🚀 **20× faster** HR matching via parallel processing
- 🔌 MongoDB connection pooling (min 10, max 50)
- ♻️ Graceful startup & shutdown lifecycle handling

---

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or cloud)
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd Backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Create environment file:**
   Create a `.env` file in the Backend directory:
   ```
   MONGODB_URI=mongodb uri goes here 
   JWT_SECRET_KEY=your-secret-key-here
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Start the backend server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd resume-analyzer-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Access the application:**
   - Main app: [http://localhost:3000](http://localhost:3000)
   - HR Dashboard: [http://localhost:3000/hr-dashboard](http://localhost:3000/hr-dashboard)

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

### Resume Management
- `POST /resume/upload` - Upload resume
- `GET /getme/resumes` - Get user's resumes

### HR Dashboard
- `POST /hr/top-matches` - Get top matching resumes for job description

## Usage Guide

### For HR Professionals

1. **Access HR Dashboard:**
   - Navigate to `http://localhost:3000/hr-dashboard`

2. **Test Connection:**
   - Click "Test Backend Connection" to verify API connectivity

3. **Find Best Matches:**
   - Enter a detailed job description
   - Click "Find Best Matches"
   - View ranked candidates with detailed scores

4. **Analyze Results:**
   - Review overall scores (Excellent: 80%+, Good: 60%+, Fair: <60%)
   - Check individual scoring components (Skill Match, TF-IDF, BERT)
   - View matched skills for each candidate
   - Access original resumes via "View Resume" links

### For Job Seekers

1. **Register/Login:**
   - Create an account or login at `http://localhost:3000`

2. **Upload Resume:**
   - Navigate to the upload section
   - Upload your resume in PDF format

3. **View Analysis:**
   - Check detailed feedback and scores
   - Review skill matching results
   - Access improvement suggestions

## Scoring Algorithm

The system uses a hybrid scoring approach combining three algorithms:

1. **Skill Match Score (40%)** - Direct skill keyword matching
2. **TF-IDF Score (30%)** - Term frequency-inverse document frequency similarity
3. **BERT Score (30%)** - Semantic similarity using BERT embeddings

## Troubleshooting

### Backend Issues
- Ensure MongoDB is running and accessible
- Check that all Python dependencies are installed
- Verify spaCy model is downloaded: `python -m spacy download en_core_web_sm`
- Confirm .env file is properly configured

### Frontend Issues
- Check if backend server is running on port 8000
- Verify CORS configuration in backend
- Check browser console for error messages
- Ensure all npm dependencies are installed

### Common Errors
- **"No resumes found"** - Upload some resumes first
- **"Backend connection failed"** - Check if server is running on port 8000
- **"Server error"** - Verify all dependencies are installed





### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
