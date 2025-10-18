#!/usr/bin/env python3
"""
Startup script for Orange Sage Frontend
"""
import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_backend():
    """Check if the backend is running"""
    print("🔍 Checking if backend is running...")
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("❌ Backend is not running")
    print("   Please start the backend first: cd Orange_sage/backend && python start.py")
    return False

def main():
    print("🚀 Starting Orange Sage Frontend...")
    
    # Check if we're in the right directory
    if not Path("src").exists():
        print("❌ Please run this script from the Orange_sage/frontend directory")
        sys.exit(1)
    
    # Check if package.json exists
    if not Path("package.json").exists():
        print("❌ package.json not found. Please run 'npm install' first.")
        sys.exit(1)
    
    # Check if node_modules exists
    if not Path("node_modules").exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Check if backend is running
    if not check_backend():
        print("\n⚠️  Backend is not running. The frontend will start but API calls will fail.")
        print("   Start the backend with: cd Orange_sage/backend && python start.py")
    
    # Start the development server
    print("\n🚀 Starting Vite development server...")
    try:
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
