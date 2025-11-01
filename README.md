# Orange Sage - AI-Powered Cybersecurity Assessment Platform

Orange Sage is a comprehensive web-based cybersecurity assessment platform that leverages AI agents to perform autonomous security testing. It provides a modern web interface for managing security assessments, viewing findings, and generating reports.

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - For backend development
- **Node.js 18+** - For frontend development
- **Git** - For version control

### Local Development Setup

#### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file based on env.example
cp env.example .env

# Update .env with your API keys
# DATABASE_URL=sqlite:///./orange_sage.db
# SECRET_KEY=your-secret-key
# GEMINI_API_KEY=your-gemini-api-key

# Start backend
python start.py
# or
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`
- API Docs: http://localhost:8000/api/v1/docs

#### 2. Frontend Setup

```bash
cd frontend
npm install --legacy-peer-deps

# Start frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Demo User

For testing, a demo user is automatically created:
- **Email**: `user@gmail.com`
- **Password**: `12345678`

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Uvicorn
- **Database**: SQLite with Litestream (for persistent storage in production)
- **LLM Integration**: Google Gemini API
- **Authentication**: JWT tokens
- **Deployment**: Google Cloud Run

### Frontend (Next.js)
- **Framework**: Next.js 14 with React 19
- **Language**: TypeScript
- **UI Library**: shadcn/ui with Tailwind CSS
- **Deployment**: Google Cloud Run

## 📁 Project Structure

```
Orange-Sage/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/           # Core configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── agents/         # AI agent implementations
│   │   └── utils/          # Utilities
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Docker image for Cloud Run
│   ├── litestream.yml      # Litestream configuration
│   └── start_with_litestream.sh  # Startup script
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app directory
│   │   ├── (auth)/       # Authentication pages
│   │   ├── dashboard/    # Dashboard page
│   │   ├── projects/     # Projects page
│   │   ├── scans/        # Scans page
│   │   ├── findings/     # Findings page
│   │   ├── reports/      # Reports page
│   │   └── settings/     # Settings page
│   ├── components/       # React components
│   ├── lib/              # Utilities and services
│   ├── Dockerfile        # Docker image for Cloud Run
│   └── package.json      # Node dependencies
├── .github/
│   └── workflows/        # GitHub Actions CI/CD
│       ├── deploy-backend.yml
│       └── deploy-frontend.yml
└── README.md
```

## 🔧 Configuration

### Backend Configuration

Create `backend/.env` based on `backend/env.example`:

```env
# Database (SQLite for local, Cloud Run uses Litestream + GCS)
DATABASE_URL=sqlite:///./orange_sage.db

# Security
SECRET_KEY=your-super-secret-key-here-change-in-production

# API Keys
GEMINI_API_KEY=your-gemini-api-key-here
```

### Frontend Configuration

The frontend automatically detects the backend URL:
- **Local development**: Uses `http://localhost:8000`
- **Production**: Uses HTTPS backend URL from `NEXT_PUBLIC_API_URL` environment variable
- **Runtime**: Automatically converts HTTP to HTTPS if the page is served over HTTPS (prevents mixed content errors)

## 🚀 Features

### Core Features
- **User Authentication** - Secure login and registration with JWT tokens
- **Project Management** - Create and manage security assessment projects
- **Target Management** - Add URLs, repositories, or file uploads
- **Scan Orchestration** - Comprehensive security scans with AI agents
- **Real-time Monitoring** - View scan progress and status
- **Findings Management** - Track vulnerabilities with severity levels
- **Report Generation** - Generate detailed PDF and HTML reports
- **Settings Management** - User profile and preferences
- **AI Chatbot** - Gemini-powered assistant for app and cybersecurity questions

### Security Testing Capabilities
- **SQL Injection Detection**
- **XSS (Cross-Site Scripting) Detection**
- **IDOR (Insecure Direct Object Reference) Detection**
- **Security Headers Analysis**
- **Weak Password Policy Detection**
- **Sensitive Data Exposure Detection**
- **Outdated Library Detection**
- **Rate Limiting Analysis**
- **DNS Security Checks**
- **Email Spoofing Detection**
- **Phishing Detection**
- **Cloud Storage Security Analysis**

## 🛠️ Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt

# Start with auto-reload
uvicorn app.main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend
npm install --legacy-peer-deps

# Start development server
npm run dev
```

### Database Migrations

The backend automatically handles schema migrations on startup for SQLite. When new columns are added to models, they are automatically added to the database.

## 🚀 Production Deployment

### Google Cloud Run Deployment

Orange Sage is deployed to Google Cloud Run using GitHub Actions.

#### Prerequisites
1. Google Cloud Project with billing enabled
2. Google Cloud Service Account with required permissions
3. GitHub repository with secrets configured

#### Required GitHub Secrets

```
GCP_SA_KEY              # Google Cloud Service Account JSON key
BACKEND_URL             # HTTPS URL of deployed backend (e.g., https://orange-sage-backend-xxx.run.app)
GCP_SERVICE_ACCOUNT_EMAIL # Service account email
DATABASE_URL            # SQLite database path (sqlite:////app/orange_sage.db)
SECRET_KEY              # JWT secret key
GEMINI_API_KEY          # Google Gemini API key
LITESTREAM_GCS_BUCKET   # GCS bucket name for Litestream database replication
```

#### Deployment Process

1. **Automatic Deployment**: Pushes to `main` branch automatically trigger deployment
   - Backend: Deploys on changes to `backend/**`
   - Frontend: Deploys on changes to `frontend/**`

2. **Manual Deployment**: Use GitHub Actions "Run workflow" button

3. **Litestream Setup**: 
   - Create a GCS bucket for database replication
   - Set `LITESTREAM_GCS_BUCKET` secret to bucket name
   - Litestream automatically backs up and restores the SQLite database

#### Backend Deployment

- **Container**: Docker image built from `backend/Dockerfile`
- **Platform**: Google Cloud Run
- **Database**: SQLite with Litestream replication to GCS
- **Startup**: Uses `start_with_litestream.sh` to restore database and start FastAPI

#### Frontend Deployment

- **Container**: Docker image built from `frontend/Dockerfile`
- **Platform**: Google Cloud Run
- **Build-time**: `NEXT_PUBLIC_API_URL` is set from `BACKEND_URL` secret
- **Runtime**: Automatically uses HTTPS if page is served over HTTPS

### Post-Deployment

1. **Initialize Demo User**: The demo user is automatically created on first startup
2. **Test Registration**: Users can register new accounts
3. **Test Scans**: Create projects and run comprehensive scans
4. **Generate Reports**: Download PDF or HTML reports

## 📊 API Documentation

Once the backend is running:
- **Swagger UI**: `http://localhost:8000/api/v1/docs` (local) or `https://your-backend-url.run.app/api/v1/docs` (production)
- **ReDoc**: `http://localhost:8000/api/v1/redoc`

## 🔒 Security

- **JWT Authentication** - Secure token-based authentication
- **Password Hashing** - Argon2 password hashing
- **Input Validation** - Pydantic schema validation
- **SQL Injection Protection** - SQLAlchemy ORM with parameterized queries
- **CORS Configuration** - Properly configured for Cloud Run deployment
- **HTTPS Enforcement** - Frontend automatically uses HTTPS in production
- **Database Encryption** - SQLite database with Litestream backups

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/api/v1/docs`
- Review the codebase documentation

## 🔮 Roadmap

- [ ] Enhanced AI agent capabilities
- [ ] Advanced reporting features with charts and graphs
- [ ] Integration with CI/CD pipelines
- [ ] Webhook support for scan notifications
- [ ] Advanced analytics dashboard
- [ ] Custom agent development framework
- [ ] Multi-tenant support
