#!/usr/bin/env python3
"""
Main startup script for Orange Sage
"""
import os
import sys
import subprocess
import time
import requests
import threading
from pathlib import Path

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Docker is not available")
    print("   Please install Docker Desktop and ensure it's running")
    return False

def start_services():
    """Start required services with Docker Compose"""
    print("🐳 Starting required services with Docker Compose...")
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("✅ Services started")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to start services")
        return False

def check_service(url, name, timeout=60):
    """Check if a service is running"""
    print(f"🔍 Checking {name} at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} is running")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(3)
    print(f"❌ {name} is not responding after {timeout}s")
    return False

def start_backend():
    """Start the backend in a separate thread"""
    print("🚀 Starting Orange Sage Backend...")
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "start.py"], check=True)
    except KeyboardInterrupt:
        print("👋 Backend stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend error: {e}")

def start_frontend():
    """Start the frontend in a separate thread"""
    print("🚀 Starting Orange Sage Frontend...")
    try:
        os.chdir("frontend")
        subprocess.run([sys.executable, "start.py"], check=True)
    except KeyboardInterrupt:
        print("👋 Frontend stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend error: {e}")

def main():
    print("🚀 Starting Orange Sage Application...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the Orange_sage directory")
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("\n❌ Docker is required but not available.")
        print("   Please install Docker Desktop and try again.")
        sys.exit(1)
    
    # Start services
    if not start_services():
        print("\n❌ Failed to start required services.")
        sys.exit(1)
    
    # Wait for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    time.sleep(10)
    
    # Check services
    services_ok = True
    
    if not check_service("http://localhost:9000", "MinIO"):
        services_ok = False
    
    if not check_service("http://localhost:6379", "Redis"):
        services_ok = False
    
    if not services_ok:
        print("\n❌ Some services are not ready. Please check Docker Compose logs.")
        sys.exit(1)
    
    print("\n✅ All services are ready!")
    
    # Start backend and frontend
    print("\n🚀 Starting Orange Sage components...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for backend to start
    time.sleep(5)
    
    # Start frontend
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Shutting down Orange Sage...")
        print("   Stopping services...")
        subprocess.run(["docker-compose", "down"], check=False)
        print("✅ Shutdown complete")

if __name__ == "__main__":
    main()
