#!/usr/bin/env python3
"""
Simple test runner for Orange Sage AI Agents
Run this script to test the AI agents functionality
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the agent tests"""
    print("🚀 Orange Sage AI Agent Test Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("test_agents.py"):
        print("❌ Error: test_agents.py not found in current directory")
        print("Please run this script from the backend directory")
        return 1
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {python_version.major}.{python_version.minor}")
        return 1
    
    print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if required modules are available
    try:
        import requests
        print("✓ requests module available")
    except ImportError:
        print("❌ Error: requests module not found")
        print("Please install required dependencies: pip install requests")
        return 1
    
    try:
        import asyncio
        print("✓ asyncio module available")
    except ImportError:
        print("❌ Error: asyncio module not found")
        return 1
    
    print("\n🔍 Running AI Agent Tests...")
    print("-" * 50)
    
    try:
        # Run the test script
        result = subprocess.run([sys.executable, "test_agents.py"], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print("\n✅ All tests completed successfully!")
            return 0
        else:
            print(f"\n❌ Tests failed with return code: {result.returncode}")
            return result.returncode
            
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
