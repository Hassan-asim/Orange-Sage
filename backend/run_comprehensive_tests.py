#!/usr/bin/env python3
"""
Comprehensive Test Runner for Orange Sage AI Agents and Services
This script runs all comprehensive tests for agents and services
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    """Run all comprehensive tests"""
    print("🚀 Orange Sage Comprehensive Test Runner")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("test_comprehensive_agents.py"):
        print("❌ Error: test_comprehensive_agents.py not found in current directory")
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
    required_modules = ['requests', 'asyncio', 'unittest.mock']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} module available")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} module not found")
    
    if missing_modules:
        print(f"\n❌ Missing required modules: {', '.join(missing_modules)}")
        print("Please install required dependencies: pip install requests")
        return 1
    
    print("\n🔍 Running Comprehensive Tests...")
    print("-" * 60)
    
    # Test 1: Comprehensive Agents and Services Test
    print("\n1. Running Comprehensive Agents & Services Test...")
    try:
        result = subprocess.run([sys.executable, "test_comprehensive_agents.py"], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Comprehensive test completed successfully!")
        else:
            print(f"❌ Comprehensive test failed with return code: {result.returncode}")
            return result.returncode
            
    except Exception as e:
        print(f"❌ Error running comprehensive test: {e}")
        return 1
    
    # Test 2: Individual Agents Test
    print("\n2. Running Individual Agents Test...")
    try:
        result = subprocess.run([sys.executable, "test_individual_agents.py"], 
                              capture_output=False, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Individual agents test completed successfully!")
        else:
            print(f"❌ Individual agents test failed with return code: {result.returncode}")
            return result.returncode
            
    except Exception as e:
        print(f"❌ Error running individual agents test: {e}")
        return 1
    
    # Test 3: Original Agent Tests (if available)
    if os.path.exists("test_agents.py"):
        print("\n3. Running Original Agent Tests...")
        try:
            result = subprocess.run([sys.executable, "test_agents.py"], 
                                  capture_output=False, 
                                  text=True)
            
            if result.returncode == 0:
                print("✅ Original agent tests completed successfully!")
            else:
                print(f"❌ Original agent tests failed with return code: {result.returncode}")
                return result.returncode
                
        except Exception as e:
            print(f"❌ Error running original agent tests: {e}")
            return 1
    
    print("\n" + "=" * 60)
    print("🎉 All comprehensive tests completed successfully!")
    print("Orange Sage AI Agents and Services are working correctly.")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
