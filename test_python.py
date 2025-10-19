#!/usr/bin/env python3
"""
Simple Python test script to verify installation
"""
import sys
import platform

print("🐍 Python Installation Test")
print("=" * 30)
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.architecture()}")

# Test basic imports
try:
    import fastapi
    print("✅ FastAPI available")
except ImportError:
    print("❌ FastAPI not installed")

try:
    import uvicorn
    print("✅ Uvicorn available")
except ImportError:
    print("❌ Uvicorn not installed")

try:
    import sqlalchemy
    print("✅ SQLAlchemy available")
except ImportError:
    print("❌ SQLAlchemy not installed")

print("\n🎉 Python is working correctly!")
print("You can now run: setup.bat")
