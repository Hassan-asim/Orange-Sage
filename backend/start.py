#!/usr/bin/env python3
"""
Startup script for Orange Sage Backend
"""
import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_service(url, name, timeout=30):
    """Check if a service is running"""
    print(f"Checking {name} at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} is running")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)
    print(f"❌ {name} is not responding after {timeout}s")
    return False

def main():
    print("🚀 Starting Orange Sage Backend...")
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Please run this script from the Orange_sage/backend directory")
        sys.exit(1)
    
    # Check if .env file exists
    if not Path(".env").exists() and not Path("env.local").exists():
        print("⚠️  No .env file found. Using default configuration.")
        print("   Create a .env file based on env.example for production use.")
    
    # Check database configuration
    print("\n🔍 Checking database configuration...")
    
    # Check if using SQLite (local development)
    env_file = Path("env.local") if Path("env.local").exists() else Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
            if "sqlite" in env_content.lower():
                print("✅ Using SQLite database (local development mode)")
                print("   No external services required for SQLite")
            else:
                print("⚠️  Using external database - checking services...")
                # Check PostgreSQL
                if not check_service("http://localhost:5432", "PostgreSQL"):
                    print("   Please start PostgreSQL or run: docker-compose up -d postgres")
                    sys.exit(1)
                
                # Check Redis
                if not check_service("http://localhost:6379", "Redis"):
                    print("   Please start Redis or run: docker-compose up -d redis")
                    sys.exit(1)
                
                # Check MinIO
                if not check_service("http://localhost:9000", "MinIO"):
                    print("   Please start MinIO or run: docker-compose up -d minio")
                    sys.exit(1)
                
                print("\n✅ All external services are running!")
    else:
        print("✅ Using default SQLite configuration")
    
    # Start the FastAPI application
    print("\n🚀 Starting FastAPI server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
