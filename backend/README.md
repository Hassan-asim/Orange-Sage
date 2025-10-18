# Orange Sage Backend

A comprehensive cybersecurity assessment platform with AI agents for automated security testing.

## Features

- **AI-Powered Security Assessment**: Automated vulnerability scanning using advanced AI agents
- **Multi-LLM Support**: Integration with OpenAI and Google Gemini APIs
- **Docker Sandboxing**: Secure execution environment for security testing
- **Comprehensive Reporting**: PDF, DOCX, and HTML report generation
- **RESTful API**: FastAPI-based backend with OpenAPI documentation
- **User Authentication**: JWT-based authentication system
- **Project Management**: Multi-tenant project and target management

## Architecture

### Core Components

- **Agent Manager**: Orchestrates AI agents for security assessments
- **LLM Service**: Manages interactions with OpenAI and Gemini APIs
- **Sandbox Service**: Handles Docker container management for secure execution
- **Report Generator**: Creates comprehensive security reports in multiple formats
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite support

### AI Agents

- **Orange Sage Agent**: Main security assessment agent
- **Reconnaissance Agent**: Information gathering and enumeration
- **Vulnerability Agent**: Specialized vulnerability testing
- **Custom Agents**: Extensible agent system for specific security tests

## Installation

### Prerequisites

- Python 3.11+
- Docker
- Redis (optional, for caching)
- PostgreSQL (optional, SQLite for development)

### Setup

1. **Clone and navigate to backend directory**
   ```bash
   cd Orange_sage/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database**
   ```bash
   # Database tables will be created automatically on first run
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
DEFAULT_LLM_MODEL=gpt-4o-mini
FALLBACK_LLM_MODEL=gemini-1.5-flash

# Database
DATABASE_URL=sqlite:///./orange_sage.db

# Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Docker/Sandbox
SANDBOX_IMAGE=orange_sage/sandbox:latest
SANDBOX_MEMORY_LIMIT=2g
SANDBOX_CPU_LIMIT=1.0
```

### API Keys

The application supports both OpenAI and Google Gemini APIs:

- **OpenAI**: Set `OPENAI_API_KEY` for GPT models
- **Gemini**: Set `GEMINI_API_KEY` for Google's Gemini models
- **Fallback**: If primary model fails, automatically falls back to secondary

## API Documentation

Once running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/projects` - List projects
- `POST /api/v1/scans` - Create security scan
- `GET /api/v1/scans/{scan_id}` - Get scan status
- `GET /api/v1/findings` - List security findings
- `POST /api/v1/reports/generate` - Generate report

## Security Features

### Sandboxing

- **Docker Containers**: Each agent runs in isolated Docker containers
- **Resource Limits**: CPU and memory limits for security
- **Network Isolation**: Controlled network access for agents
- **File System**: Restricted file system access

### Authentication

- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: bcrypt password hashing
- **Token Expiration**: Configurable token expiration
- **User Roles**: Role-based access control

## Development

### Project Structure

```
app/
├── api/           # API routes and endpoints
├── core/          # Core configuration and database
├── models/        # Database models
├── schemas/       # Pydantic schemas
├── services/      # Business logic services
├── tasks/         # Background tasks
└── utils/         # Utility functions
```

### Adding New Agents

1. Create agent class inheriting from `BaseAgent`
2. Implement `execute()` method
3. Register in `AgentFactory`
4. Add to agent configuration

### Adding New Report Formats

1. Implement format-specific generation method
2. Add format to `ReportFormat` enum
3. Update report generation logic

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t orange-sage-backend .

# Run container
docker run -p 8000:8000 --env-file .env orange-sage-backend
```

### Production Considerations

- Use PostgreSQL for production database
- Configure Redis for caching
- Set up proper logging
- Configure reverse proxy (nginx)
- Use HTTPS in production
- Set up monitoring and alerting

## Monitoring

### Health Checks

- `GET /health` - Basic health check
- `GET /health/detailed` - Detailed service status

### Metrics

- Agent execution times
- LLM API usage and costs
- Database performance
- Docker container metrics

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

This project is licensed under the MIT License.
