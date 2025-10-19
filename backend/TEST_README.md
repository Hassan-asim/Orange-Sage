# Orange Sage AI Agent Tests

This directory contains test files for the Orange Sage AI agents system.

## Files

- `test_agents.py` - Main test file for AI agents functionality
- `run_agent_tests.py` - Simple test runner script
- `test_requirements.txt` - Dependencies needed for testing
- `TEST_README.md` - This file

## Quick Start

### 1. Install Dependencies

```bash
# Install test dependencies
pip install -r test_requirements.txt

# Or install minimal requirements
pip install requests asyncio
```

### 2. Run Tests

#### Option A: Using the test runner (recommended)

```bash
python run_agent_tests.py
```

#### Option B: Direct execution

```bash
python test_agents.py
```

## What the Tests Cover

### 1. PentestingAgent Tests

- ✅ Target parsing (URLs, hostnames, IPs)
- ✅ HTTP request functionality
- ✅ Response analysis
- ✅ Security header detection
- ✅ Vulnerability payload testing
- ✅ SQL injection detection
- ✅ XSS detection
- ✅ Command injection detection
- ✅ Path traversal detection

### 2. AgentFactory Tests

- ✅ Agent type registration
- ✅ Agent creation
- ✅ Invalid agent type handling
- ✅ Configuration passing

### 3. Individual Agent Tests

- ✅ OrangeSageAgent execution
- ✅ ReconnaissanceAgent functionality
- ✅ VulnerabilityAgent testing
- ✅ Assessment initialization
- ✅ Finding generation

### 4. AgentManager Tests (Mock)

- ✅ Manager initialization
- ✅ Method availability
- ✅ Structure verification

## Test Targets

The tests use safe, public targets for testing:

- `https://httpbin.org` - Safe HTTP testing service
- `https://example.com` - Basic website
- `127.0.0.1` - Local testing

## Expected Output

When tests run successfully, you should see:

```
============================================================
ORANGE SAGE AI AGENT TESTING
============================================================

🔍 Testing PentestingAgent...
  ✓ Created PentestingAgent for target: https://httpbin.org
  ✓ Target parsing successful: web
  ✓ HTTP request successful: 200
  ✓ Response analysis completed
  ✓ SQL Injection payloads: 10
  ✓ XSS payloads: 10
  ✓ Command injection payloads: 10
  ✓ Path traversal payloads: 7
  ✓ SQL injection detection: True
  ✓ Command injection detection: True
  ✓ Path traversal detection: True

🏭 Testing AgentFactory...
  ✓ Available agent types: ['OrangeSageAgent', 'ReconnaissanceAgent', 'VulnerabilityAgent']
  ✓ Created OrangeSageAgent: OrangeSageAgent
  ✓ Created ReconnaissanceAgent: ReconnaissanceAgent
  ✓ Created VulnerabilityAgent: VulnerabilityAgent
  ✓ Correctly rejected invalid agent type: Unknown agent type: InvalidAgent

🤖 Testing Individual Agents...
  Testing OrangeSageAgent...
    ✓ Assessment initialization: comprehensive
    ✓ Reconnaissance: 3 data points
    ✓ Vulnerability testing: 10 tests
    ✓ Generated 2 findings
    ✓ Full execution: True
  Testing ReconnaissanceAgent...
    ✓ Reconnaissance data: 4 items
    ✓ Reconnaissance execution: True
  Testing VulnerabilityAgent...
    ✓ Vulnerability data: 5 tests
    ✓ Vulnerability execution: True

📊 Testing AgentManager (Mock)...
  ✓ AgentManager class imported successfully
  ✓ AgentManager methods available:
    - start_scan()
    - get_scan_status()
    - get_scan_agents()
    - cancel_scan()
    - cleanup()
  ✓ AgentManager initialized successfully
  ✓ Active agents: 0
  ✓ Active scans: 0

============================================================
TEST RESULTS SUMMARY
============================================================
Total Tests: 4
Passed: 4
Failed: 0
Success Rate: 100.0%

Detailed Results:
  ✓ PentestingAgent: PASS
  ✓ AgentFactory: PASS
  ✓ Individual Agents: PASS
  ✓ AgentManager: PASS

============================================================
🎉 All tests passed! Orange Sage AI Agents are working correctly.
============================================================
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'app'**

   - Make sure you're running from the backend directory
   - Check that the app directory exists

2. **ModuleNotFoundError: No module named 'requests'**

   - Install dependencies: `pip install -r test_requirements.txt`

3. **Network errors during HTTP tests**

   - Check your internet connection
   - Some corporate networks may block external requests

4. **Permission errors**
   - Make sure you have write permissions in the current directory

### Debug Mode

To run tests with more verbose output:

```bash
python test_agents.py 2>&1 | tee test_output.log
```

## Contributing

When adding new agent types or functionality:

1. Update the test file to include new tests
2. Add new test cases for any new methods
3. Ensure all tests pass before committing
4. Update this README if needed

## Notes

- Tests are designed to be safe and non-destructive
- No actual exploitation attempts are made
- All HTTP requests use safe, public targets
- Tests can be run multiple times safely
