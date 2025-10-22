# Windows Setup Guide for Orange Sage Backend

## Overview

The Orange Sage backend is fully compatible with Windows. However, some optional features require additional setup.

## Quick Start (Windows)

1. **Install Python 3.13** (already done ✅)

2. **Install dependencies**:
   ```bash
   cd backend
   uv pip install --system -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   python start.py
   ```

The server will start on `http://localhost:8000` 🚀

## Optional Features

### 1. Docker Sandbox Mode (Optional)

**What it does**: Runs security scanning agents in isolated Docker containers for enhanced security.

**Default behavior**: Uses mock sandbox mode (perfectly fine for development and testing).

**To enable**:
1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Start Docker Desktop
3. Restart the Orange Sage backend

**Status**: The backend works perfectly fine without Docker!

---

### 2. WeasyPrint PDF Generation (Optional)

**What it does**: Advanced HTML to PDF conversion with better styling options.

**Default behavior**: Uses ReportLab for PDF generation (fully functional).

**To enable on Windows**:
1. Download and install GTK3 runtime from: 
   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
2. Uncomment the `weasyprint` line in `requirements.txt`
3. Run: `uv pip install --system weasyprint`

**Alternative**: Use WSL2 (Windows Subsystem for Linux) where WeasyPrint works natively.

**Status**: ReportLab provides all the PDF functionality you need!

---

## Python 3.13 Compatibility

✅ **Fixed!** The backend now uses:
- `pydantic>=2.10.0` (Python 3.13 compatible)
- `pydantic-settings>=2.7.0` (Python 3.13 compatible)

The previous version (`pydantic==2.5.0`) had build issues on Python 3.13.

---

## Troubleshooting

### "WeasyPrint not available" message
- **This is normal on Windows!** The app uses ReportLab instead.
- No action needed unless you specifically need WeasyPrint features.

### "Docker not available" message
- **This is normal if Docker Desktop isn't running!**
- The app uses mock sandbox mode which works fine for development.
- No action needed for basic usage.

### Database issues
- The backend uses SQLite by default (no setup required).
- Database file: `orange_sage.db` in the backend directory.

---

## Environment Setup

1. Copy `env.local` to `.env`:
   ```bash
   copy env.local .env
   ```

2. Update API keys in `.env`:
   ```
   OPENAI_API_KEY=your-key-here
   GEMINI_API_KEY=your-key-here
   ```

3. (Optional) Configure other settings as needed.

---

## Running the Backend

```bash
# Development mode with auto-reload
python start.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Need Help?

- Check logs in the console output
- Ensure Python 3.13 is installed: `python --version`
- Ensure all dependencies are installed: `uv pip list --system`

---

**Last Updated**: October 2025  
**Compatible with**: Python 3.13+, Windows 10/11

