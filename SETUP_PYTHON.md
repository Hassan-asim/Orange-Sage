# Python Installation Guide for Orange Sage

## 🐍 Installing Python on Windows

### Method 1: Official Python Website (Recommended)

1. **Download Python**:
   - Go to https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (latest version)
   - Choose "Windows installer (64-bit)"

2. **Install Python**:
   - Run the downloaded installer
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**:
   - Open Command Prompt or PowerShell
   - Type: `python --version`
   - You should see: `Python 3.11.x`

### Method 2: Microsoft Store (Alternative)

1. **Open Microsoft Store**:
   - Press `Windows + R`
   - Type `ms-windows-store:` and press Enter

2. **Search for Python**:
   - Search for "Python 3.11"
   - Click "Install"

3. **Verify Installation**:
   - Open Command Prompt or PowerShell
   - Type: `python --version`

## 🚀 Running Orange Sage After Python Installation

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements_local.txt
```

### Step 2: Start Backend
```bash
cd backend
python -m uvicorn app.main_local:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3: Install Frontend Dependencies (New Terminal)
```bash
cd frontend
npm install
```

### Step 4: Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs

## 🔧 Troubleshooting

### Python Not Found Error
If you get "Python was not found":

1. **Check if Python is installed**:
   - Open Command Prompt
   - Try: `python --version`
   - Try: `python3 --version` 
   - Try: `py --version`

2. **If none work, reinstall Python**:
   - Go to https://www.python.org/downloads/
   - Download Python 3.11.x
   - ⚠️ **CRITICAL**: Check "Add Python to PATH" at the bottom
   - Choose "Customize installation"
   - Check "Add Python to environment variables"
   - Complete installation

3. **Restart everything**:
   - Close all terminals/command prompts
   - Restart your computer (recommended)
   - Open new Command Prompt
   - Try again

4. **Test Python manually**:
   ```bash
   python test_python.py
   ```

5. **Alternative commands**:
   - Use `py` instead of `python`
   - Use `python3` instead of `python`

### Permission Errors
If you get permission errors:
```bash
# Try with --user flag
pip install --user -r requirements_local.txt
```

### Node.js Not Found
If you get Node.js errors:
1. Install Node.js from https://nodejs.org
2. Choose LTS version (18.x or higher)
3. Restart terminal after installation

## 📋 Quick Checklist

- [ ] Python 3.8+ installed and working
- [ ] Node.js 18+ installed and working
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173

## 🎯 What's Next?

Once Python is installed and working:

1. **Test Python**: `python --version`
2. **Install Backend Dependencies**: `cd backend && pip install -r requirements_local.txt`
3. **Start Backend**: `cd backend && python -m uvicorn app.main_local:app --reload`
4. **Install Frontend Dependencies**: `cd frontend && npm install`
5. **Start Frontend**: `cd frontend && npm run dev`

Then visit http://localhost:5173 to see Orange Sage! 🎉
