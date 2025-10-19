# Orange Sage Setup Guide

## 🚀 Quick Start

Orange Sage is a comprehensive AI-powered cybersecurity assessment platform. This guide will help you get it running.

## 📋 Prerequisites

### Required Software
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Docker Desktop** - [Download Docker](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download Git](https://git-scm.com/)

### Verify Installation
```bash
python --version    # Should show Python 3.8+
node --version      # Should show Node.js 18+
docker --version    # Should show Docker version
```

## 🛠️ Installation Steps

### 1. Clone and Navigate
```bash
git clone <your-repo-url>
cd Orange_sage
```

### 2. Start Required Services
```bash
# Start PostgreSQL, Redis, and MinIO
docker-compose up -d

# Verify services are running
docker ps
```

### 3. Setup Backend
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your-openai-key-here
# GEMINI_API_KEY=your-gemini-key-here
# SECRET_KEY=your-secret-key-here

# Start backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Setup Frontend (New Terminal)
```bash
cd frontend

# Install Node.js dependencies
npm install

# Create environment file
cp env.example .env
# Edit .env:
# VITE_API_BASE_URL=http://localhost:8000/api/v1

# Start frontend
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **MinIO Console**: http://localhost:9001 (admin/admin)

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# API Keys (Required)
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=AIzaSyC-your-gemini-key-here

# Database
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orange_sage
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orange_sage

# Security
SECRET_KEY=your-super-secret-key-here

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🎯 Features Available

### 🤖 AI-Powered Pentesting
- **Automated Vulnerability Detection**
  - SQL Injection testing
  - Cross-Site Scripting (XSS) detection
  - Command injection testing
  - Path traversal detection
  - Authentication bypass testing
  - Session management analysis

### 🔍 Advanced Security Analysis
- **Network Security Scanning**
  - Port scanning and service enumeration
  - SSL/TLS configuration analysis
  - Security header assessment
  - Technology fingerprinting

### 📊 Comprehensive Reporting
- **Professional PDF Reports**
  - Executive summaries
  - Detailed technical findings
  - Risk assessment and scoring
  - Remediation recommendations
  - Multiple output formats

### 🏗️ Microservices Architecture
- **Scalable Service Design**
  - Vulnerability Scanner Service
  - Network Analyzer Service
  - Code Analyzer Service
  - Compliance Checker Service
  - Threat Intelligence Service
  - Report Generator Service

## 🚀 Usage Workflow

### 1. Create Project
- Navigate to Projects page
- Click "Create New Project"
- Enter project details

### 2. Add Target
- Go to your project
- Click "Add Target"
- Specify URL, repository, or upload files

### 3. Start Comprehensive Scan
- Click "Start Comprehensive Scan"
- Choose scan configuration
- Monitor real-time progress

### 4. Review Findings
- View detailed vulnerability analysis
- Filter by severity and type
- Review remediation recommendations

### 5. Generate Reports
- Click "Generate Report"
- Choose format (PDF/HTML)
- Download professional reports

## 🔒 Security Features

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (Admin, Developer, Auditor)
- Secure session management

### Data Protection
- Encrypted API keys storage
- Secure database connections
- Input validation and sanitization

### Network Security
- CORS configuration
- Rate limiting
- Request validation

## 🐛 Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Windows
# Install Python from python.org or Microsoft Store
# Make sure to check "Add Python to PATH" during installation

# Verify installation
python --version
```

#### Node.js Not Found
```bash
# Install Node.js from nodejs.org
# Verify installation
node --version
npm --version
```

#### Docker Not Running
```bash
# Start Docker Desktop
# Verify Docker is running
docker --version
docker ps
```

#### Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# Kill the process or use different ports
```

### Service Status Check
```bash
# Check Docker services
docker ps

# Check backend health
curl http://localhost:8000/api/v1/health

# Check frontend
curl http://localhost:5173
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🆘 Support

If you encounter issues:
1. Check the logs in the terminal
2. Verify all services are running
3. Check environment variables
4. Review the troubleshooting section
5. Create an issue on GitHub

## 🎉 Success!

Once everything is running, you should see:
- ✅ Backend API responding at http://localhost:8000
- ✅ Frontend interface at http://localhost:5173
- ✅ Database connected
- ✅ All services healthy

Happy security testing! 🛡️
