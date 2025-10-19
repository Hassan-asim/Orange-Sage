# Orange Sage - AI-Powered Cybersecurity Assessment Platform

Orange Sage is a comprehensive web-based cybersecurity assessment platform that leverages AI agents to perform autonomous security testing. it provides a modern web interface for managing security assessments, viewing findings, and generating reports.

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** - For running required services
- **Python 3.11+** - For backend development
- **Node.js 18+** - For frontend development
- **Git** - For version control

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Orange_sage
```

### 2. Start the Application

```bash
# Start everything (recommended)
python start.py
```

This will:
- Start PostgreSQL, Redis, and MinIO services
- Start the backend API server
- Start the frontend development server
- Open the application at http://localhost:5173

### 3. Alternative Manual Setup

If you prefer to start components separately:

```bash
# Start services
docker-compose up -d

# Start backend (in one terminal)
cd backend
python start.py

# Start frontend (in another terminal)
cd frontend
python start.py
```

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Uvicorn
- **Database**: PostgreSQL with SQLAlchemy
- **Task Queue**: Celery with Redis
- **LLM Integration**: LiteLLM (OpenAI, Gemini)
- **Object Storage**: MinIO/S3
- **Authentication**: JWT tokens

### Frontend (React)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: shadcn/ui with Tailwind CSS
- **State Management**: React Query
- **Routing**: React Router

### Services
- **PostgreSQL**: Primary database
- **Redis**: Task queue and caching
- **MinIO**: Object storage for reports and artifacts

## 📁 Project Structure

```
Orange_sage/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core configuration
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   └── utils/         # Utilities
│   ├── requirements.txt   # Python dependencies
│   └── start.py          # Backend startup script
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   └── services/     # API services
│   ├── package.json      # Node dependencies
│   └── start.py         # Frontend startup script
├── docker-compose.yml     # Service definitions
└── start.py              # Main startup script
```

## 🔧 Configuration

### Backend Configuration

Create `backend/.env` based on `backend/env.example`:

```env
# API Keys (Required)
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=AIzaSyC-your-gemini-key-here

# Database
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orange_sage
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orange_sage

# Security
SECRET_KEY=your-super-secret-key-here
```

### Frontend Configuration

Create `frontend/.env` based on `frontend/env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🚀 Features

### Core Features
- **User Authentication** - Secure login and registration
- **Project Management** - Organize security assessments
- **Target Management** - Add URLs, repositories, or file uploads
- **Scan Orchestration** - AI agent coordination
- **Real-time Monitoring** - Live scan progress and logs
- **Findings Management** - Vulnerability tracking and triage
- **Report Generation** - PDF, DOCX, and HTML reports
- **Settings Management** - User preferences and integrations

### AI Agent Capabilities
- **Autonomous Testing** - Self-directed security assessments
- **Multi-agent Coordination** - Specialized agents for different tasks
- **Real-time Adaptation** - Dynamic strategy adjustment
- **Comprehensive Coverage** - Black-box and white-box testing
- **Vulnerability Detection** - OWASP Top 10 and beyond

## 🛠️ Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## 🐳 Docker Services

The application uses Docker Compose for local development:

- **PostgreSQL** (port 5432) - Database
- **Redis** (port 6379) - Task queue
- **MinIO** (ports 9000, 9001) - Object storage

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🔒 Security

- **JWT Authentication** - Secure token-based auth
- **Role-based Access** - Admin, Developer, Auditor roles
- **Input Validation** - Pydantic schema validation
- **SQL Injection Protection** - SQLAlchemy ORM
- **CORS Configuration** - Controlled cross-origin requests

## 🚀 Deployment

### Production Deployment

1. **Backend**: Deploy to cloud provider (AWS, GCP, Azure)
2. **Frontend**: Deploy to static hosting (Vercel, Netlify)
3. **Database**: Use managed PostgreSQL service
4. **Storage**: Use managed S3-compatible storage
5. **Queue**: Use managed Redis service

### Environment Variables

Set the following environment variables in production:

```env
# Backend
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=sk-your-production-key
GEMINI_API_KEY=AIzaSyC-your-production-key

# Frontend
VITE_API_BASE_URL=https://your-api-domain.com/api/v1
```

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
- Check the documentation
- Review the API documentation

## 🔮 Roadmap

- [ ] Kubernetes deployment manifests
- [ ] Advanced reporting features
- [ ] Integration with CI/CD pipelines
- [ ] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Custom agent development framework
