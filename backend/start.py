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
    
    # Check if required services are running
    print("\n🔍 Checking required services...")
    
    services_ok = True
    
    # Check PostgreSQL
    if not check_service("http://localhost:5432", "PostgreSQL"):
        print("   Please start PostgreSQL or run: docker-compose up -d postgres")
        services_ok = False
    
    # Check Redis
    if not check_service("http://localhost:6379", "Redis"):
        print("   Please start Redis or run: docker-compose up -d redis")
        services_ok = False
    
    # Check MinIO
    if not check_service("http://localhost:9000", "MinIO"):
        print("   Please start MinIO or run: docker-compose up -d minio")
        services_ok = False
    
    if not services_ok:
        print("\n❌ Some required services are not running.")
        print("   Run 'docker-compose up -d' from the Orange_sage directory to start all services.")
        sys.exit(1)
    
    print("\n✅ All services are running!")
    
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
