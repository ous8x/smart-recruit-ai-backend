
# 🚀 Smart Recruit AI - Backend

AI-Powered CV Filtering System for HR Recruitment using FastAPI

## 📋 Features

- ✅ **JWT Authentication** - Secure user registration and login
- 📝 **Job Management** - Create and manage job postings
- 📄 **Bulk CV Upload** - Upload up to 1000 CVs simultaneously
- 🤖 **AI Processing**:
  - Text extraction from PDF/DOCX files (Docling)
  - Candidate name extraction (mDeBERTa)
  - Semantic CV matching (Sentence Transformers)
- ⚡ **Background Processing** - Non-blocking CV analysis
- 🎯 **Smart Ranking** - Automatic candidate scoring
- 🗄️ **PostgreSQL Database** - Production-ready async database

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.109+
- **Database**: PostgreSQL + SQLAlchemy (Async)
- **Authentication**: JWT (python-jose)
- **AI Models**:
  - `timpal0l/mdeberta-v3-base-squad2` (Name Extraction)
  - `paraphrase-multilingual-MiniLM-L12-v2` (Semantic Matching)
  - `Docling` (PDF/DOCX Text Extraction)

## 📦 Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd smart-recruit-ai-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

Install PostgreSQL and create database:

```sql
CREATE DATABASE smart_recruit_db;
```

### 5. Configure Environment

Copy `.env.example` to `.env` and update:

```bash
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

Edit `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/smart_recruit_db
SECRET_KEY=your-super-secret-key-min-32-characters
```

### 6. Run Migrations

```bash
alembic upgrade head
```

### 7. Start Server

```bash
python run.py
```

Server will start at: **http://localhost:8000**

## 📖 API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new HR user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Jobs
- `POST /api/v1/jobs/` - Create job posting
- `GET /api/v1/jobs/` - List all my jobs
- `GET /api/v1/jobs/{job_id}` - Get job details with applications
- `PUT /api/v1/jobs/{job_id}` - Update job
- `DELETE /api/v1/jobs/{job_id}` - Delete job

### Applications
- `POST /api/v1/applications/{job_id}/upload` - Upload CVs (bulk)
- `GET /api/v1/applications/{job_id}/applications` - List all applications
- `GET /api/v1/applications/application/{id}` - Get application details

## 🧪 Testing

```bash
pytest tests/
```

## 📁 Project Structure

```
smart-recruit-ai-backend/
├── app/
│   ├── ai/              # AI processing modules
│   ├── api/             # API endpoints
│   ├── core/            # Config & security
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── utils/           # Helper functions
├── alembic/             # Database migrations
├── uploads/             # Uploaded CV files
└── tests/               # Unit tests
```

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📄 License

MIT License

***

## 🚀 **خطوات التشغيل النهائية:**

### **1. تثبيت PostgreSQL**
```bash
# قم بتثبيت PostgreSQL من:
# https://www.postgresql.org/download/windows/
```

### **2. إنشاء قاعدة البيانات**
```sql
-- افتح pgAdmin أو psql
CREATE DATABASE smart_recruit_db;
```

### **3. تفعيل البيئة الافتراضية**
```cmd
cd smart-recruit-ai-backend
venv\Scripts\activate
```

### **4. تشغيل السيرفر**
```cmd
python run.py
```

### **5. افتح المتصفح**
```
http://localhost:8000/docs
```

for me how creat requirements.txt stable : pip freeze > requirements.txt

***

