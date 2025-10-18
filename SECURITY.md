# Security Guidelines for Orange Sage

## 🔒 Critical Security Rules

### 1. NEVER Commit Secrets
- ❌ **NEVER** commit `.env` files
- ❌ **NEVER** commit API keys
- ❌ **NEVER** commit passwords
- ❌ **NEVER** commit tokens
- ❌ **NEVER** commit private keys
- ❌ **NEVER** commit database credentials

### 2. Environment Variables
Always use environment variables for sensitive data:

```bash
# ✅ GOOD - Use environment variables
export OPENAI_API_KEY="sk-your-key-here"
export GEMINI_API_KEY="AIzaSyC-your-key-here"
export SECRET_KEY="your-secret-key-here"

# ❌ BAD - Never hardcode in source code
OPENAI_API_KEY = "sk-your-key-here"  # DON'T DO THIS!
```

### 3. File Patterns to Avoid
The following file patterns are automatically ignored by `.gitignore`:

```
# Environment files
.env
.env.*
.env.local
.env.production
env.local
env.production

# API Keys and Secrets
*api*key*
*secret*
*password*
*token*
*credential*
*private*
*key*

# Database files
*.db
*.sqlite
*.sqlite3
database.yml
database.json

# Cloud credentials
.aws/
.azure/
.gcp/
credentials.json
service-account*.json
```

## 🛡️ Security Checklist

Before committing code, verify:

- [ ] No `.env` files are staged
- [ ] No API keys in source code
- [ ] No hardcoded passwords
- [ ] No database credentials
- [ ] No private keys or certificates
- [ ] No cloud provider credentials
- [ ] No Docker secrets
- [ ] No backup files with sensitive data

## 🔍 Pre-commit Security Check

Run this command before committing:

```bash
# Check for potential secrets
git diff --cached | grep -E "(api[_-]?key|secret|password|token|credential)" -i

# Check for environment files
git diff --cached --name-only | grep -E "\.env|env\." 

# Check for database files
git diff --cached --name-only | grep -E "\.db$|\.sqlite$"
```

## 🚨 If You Accidentally Commit Secrets

1. **Immediately** remove the sensitive data:
   ```bash
   git rm --cached .env
   git commit -m "Remove sensitive .env file"
   ```

2. **Rotate** any exposed credentials:
   - Generate new API keys
   - Change passwords
   - Regenerate tokens

3. **Force push** to remove from history:
   ```bash
   git push --force-with-lease origin main
   ```

4. **Notify** team members to pull the updated history

## 📋 Environment Setup

### Backend Environment
Create `Orange_sage/backend/.env` with:

```env
# App Configuration
SECRET_KEY=your-super-secret-key-here
APP_ENV=development

# Database
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/orange_sage
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/orange_sage

# API Keys (REPLACE WITH YOUR ACTUAL KEYS)
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=AIzaSyC-your-gemini-key-here

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# S3/MinIO
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=orange-sage
```

### Frontend Environment
Create `Orange_sage/frontend/.env` with:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🔐 Production Security

### Environment Variables
- Use a secure secret management system
- Rotate secrets regularly
- Use different secrets for different environments
- Monitor for secret exposure

### Database Security
- Use strong passwords
- Enable SSL/TLS connections
- Regular security updates
- Backup encryption

### API Security
- Rate limiting
- Input validation
- Authentication required
- HTTPS only

## 📞 Security Incident Response

If you discover a security issue:

1. **Immediately** remove sensitive data from repository
2. **Rotate** all exposed credentials
3. **Notify** the team
4. **Document** the incident
5. **Review** security practices

## 🎯 Best Practices

1. **Use environment variables** for all secrets
2. **Never commit** `.env` files
3. **Use strong, unique** passwords
4. **Rotate credentials** regularly
5. **Monitor** for secret exposure
6. **Use secret scanning** tools
7. **Review** commits before pushing
8. **Use** pre-commit hooks for security checks

## 🛠️ Security Tools

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Install security hooks
pre-commit install
```

### Secret Scanning
```bash
# Install truffleHog for secret scanning
pip install truffleHog

# Scan repository
truffleHog --regex --entropy=False .
```

### Git Hooks
```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
# Check for secrets
if git diff --cached | grep -E "(api[_-]?key|secret|password|token)" -i; then
    echo "❌ Potential secrets detected in commit!"
    exit 1
fi
```

Remember: **Security is everyone's responsibility!** 🛡️
