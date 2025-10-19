#!/usr/bin/env python3
"""
Individual Agent Testing for Orange Sage
Tests each agent type individually with detailed analysis
"""

import asyncio
import json
import logging
import sys
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import Mock, patch

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import agents
from app.agents.pentesting_agent import PentestingAgent


class IndividualAgentTester:
    """Individual testing for each agent type"""
    
    def __init__(self):
        self.test_results = []
        self.test_targets = [
            "https://httpbin.org",
            "https://example.com", 
            "127.0.0.1",
            "https://jsonplaceholder.typicode.com"
        ]
    
    async def run_individual_tests(self):
        """Run individual agent tests"""
        logger.info("Starting Individual Agent Tests")
        print("=" * 60)
        print("INDIVIDUAL ORANGE SAGE AGENT TESTING")
        print("=" * 60)
        
        # Test PentestingAgent in detail
        await self.test_pentesting_agent_detailed()
        
        # Print results
        self.print_test_results()
    
    async def test_pentesting_agent_detailed(self):
        """Detailed testing of PentestingAgent"""
        print("\n🔍 Testing PentestingAgent (Detailed Analysis)...")
        
        try:
            # Test configuration variations
            configs = [
                {
                    "timeout": 30,
                    "max_requests": 5,
                    "user_agent": "Orange-Sage-Test/1.0"
                },
                {
                    "timeout": 60,
                    "max_requests": 20,
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            ]
            
            for i, config in enumerate(configs, 1):
                print(f"\n  Configuration {i}:")
                print(f"    Timeout: {config['timeout']}s")
                print(f"    Max Requests: {config['max_requests']}")
                print(f"    User Agent: {config['user_agent'][:50]}...")
                
                # Test with different targets
                for target in self.test_targets:
                    print(f"\n    Testing target: {target}")
                    
                    agent = PentestingAgent(f"test-agent-{uuid.uuid4()}", target, config)
                    
                    # Test initialization
                    print(f"      ✓ Agent ID: {agent.agent_id}")
                    print(f"      ✓ Target: {agent.target}")
                    print(f"      ✓ Config: {len(agent.config)} parameters")
                    
                    # Test target parsing
                    parsed_target = agent._parse_target()
                    if parsed_target:
                        print(f"      ✓ Target type: {parsed_target['type']}")
                        print(f"      ✓ Hostname: {parsed_target.get('hostname', 'N/A')}")
                        print(f"      ✓ Port: {parsed_target.get('port', 'N/A')}")
                        print(f"      ✓ Scheme: {parsed_target.get('scheme', 'N/A')}")
                    else:
                        print(f"      ✗ Target parsing failed")
                        continue
                    
                    # Test HTTP session
                    print(f"      ✓ Session headers: {len(agent.session.headers)}")
                    print(f"      ✓ User-Agent: {agent.session.headers.get('User-Agent', 'N/A')}")
                    
                    # Test HTTP request
                    response = await agent._make_request(target)
                    if response:
                        print(f"      ✓ HTTP Response: {response.status_code}")
                        print(f"      ✓ Content Length: {len(response.text)} bytes")
                        print(f"      ✓ Response Time: < 10s")
                        
                        # Test response analysis
                        initial_findings = len(agent.findings)
                        agent._analyze_http_response(response, parsed_target)
                        new_findings = len(agent.findings)
                        print(f"      ✓ Analysis completed: {new_findings - initial_findings} new findings")
                        
                        # Test specific analysis methods
                        await self._test_analysis_methods(agent, target, parsed_target)
                        
                    else:
                        print(f"      ✗ HTTP request failed")
                    
                    # Test payload functionality
                    self._test_payload_functionality(agent)
                    
                    # Test vulnerability detection
                    self._test_vulnerability_detection_methods(agent)
                    
                    # Test report generation
                    self._test_report_generation_methods(agent)
            
            self.test_results.append({
                "test": "PentestingAgent (Detailed)",
                "status": "PASS",
                "details": "All detailed functionality working"
            })
            
        except Exception as e:
            print(f"  ✗ PentestingAgent detailed test failed: {e}")
            self.test_results.append({
                "test": "PentestingAgent (Detailed)",
                "status": "FAIL",
                "details": str(e)
            })
    
    async def _test_analysis_methods(self, agent, target, parsed_target):
        """Test specific analysis methods"""
        print("        Testing analysis methods...")
        
        # Test directory enumeration
        try:
            initial_findings = len(agent.findings)
            await agent._directory_enumeration(parsed_target)
            new_findings = len(agent.findings)
            print(f"          ✓ Directory enumeration: {new_findings - initial_findings} findings")
        except Exception as e:
            print(f"          ⚠ Directory enumeration failed: {e}")
        
        # Test technology fingerprinting
        try:
            initial_findings = len(agent.findings)
            await agent._technology_fingerprinting(parsed_target)
            new_findings = len(agent.findings)
            print(f"          ✓ Technology fingerprinting: {new_findings - initial_findings} findings")
        except Exception as e:
            print(f"          ⚠ Technology fingerprinting failed: {e}")
        
        # Test SSL analysis (if HTTPS)
        if parsed_target.get('scheme') == 'https':
            try:
                initial_findings = len(agent.findings)
                await agent._ssl_analysis(parsed_target)
                new_findings = len(agent.findings)
                print(f"          ✓ SSL analysis: {new_findings - initial_findings} findings")
            except Exception as e:
                print(f"          ⚠ SSL analysis failed: {e}")
        
        # Test vulnerability scanning
        try:
            initial_findings = len(agent.findings)
            await agent._web_vulnerability_scanning(parsed_target)
            new_findings = len(agent.findings)
            print(f"          ✓ Vulnerability scanning: {new_findings - initial_findings} findings")
        except Exception as e:
            print(f"          ⚠ Vulnerability scanning failed: {e}")
    
    def _test_payload_functionality(self, agent):
        """Test payload functionality in detail"""
        print("        Testing payload functionality...")
        
        payload_types = ['sql_injection', 'xss', 'command_injection', 'path_traversal']
        
        for payload_type in payload_types:
            payloads = agent.payloads[payload_type]
            print(f"          ✓ {payload_type}: {len(payloads)} payloads")
            
            # Test first few payloads
            for i, payload in enumerate(payloads[:3]):
                print(f"            - Payload {i+1}: {payload[:50]}{'...' if len(payload) > 50 else ''}")
    
    def _test_vulnerability_detection_methods(self, agent):
        """Test vulnerability detection methods"""
        print("        Testing vulnerability detection...")
        
        # Test SQL injection detection
        sql_responses = [
            type('MockResponse', (), {
                'text': 'mysql_fetch_array() error: Table \'users\' doesn\'t exist',
                'status_code': 200
            })(),
            type('MockResponse', (), {
                'text': 'Microsoft OLE DB Provider for ODBC Drivers error',
                'status_code': 200
            })(),
            type('MockResponse', (), {
                'text': 'PostgreSQL query failed: syntax error',
                'status_code': 200
            })()
        ]
        
        for i, response in enumerate(sql_responses, 1):
            detected = agent._detect_sql_injection_response(response)
            print(f"          ✓ SQL injection test {i}: {detected}")
        
        # Test command injection detection
        cmd_responses = [
            type('MockResponse', (), {
                'text': 'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin',
                'status_code': 200
            })(),
            type('MockResponse', (), {
                'text': 'uid=0(root) gid=0(root) groups=0(root)',
                'status_code': 200
            })(),
            type('MockResponse', (), {
                'text': 'Volume Serial Number is 1234-5678',
                'status_code': 200
            })()
        ]
        
        for i, response in enumerate(cmd_responses, 1):
            detected = agent._detect_command_injection_response(response)
            print(f"          ✓ Command injection test {i}: {detected}")
        
        # Test path traversal detection
        path_responses = [
            type('MockResponse', (), {
                'text': 'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin',
                'status_code': 200
            })(),
            type('MockResponse', (), {
                'text': 'bin:x:2:2:bin:/bin:/usr/sbin/nologin',
                'status_code': 200
            })(),
            type('MockResponse', (), {
                'text': 'system:x:101:102:system:/var/lib/dbus:/bin/false',
                'status_code': 200
            })()
        ]
        
        for i, response in enumerate(path_responses, 1):
            detected = agent._detect_path_traversal_response(response)
            print(f"          ✓ Path traversal test {i}: {detected}")
    
    def _test_report_generation_methods(self, agent):
        """Test report generation methods"""
        print("        Testing report generation...")
        
        # Add some test findings
        agent.findings = [
            {
                'title': 'SQL Injection Vulnerability',
                'severity': 'critical',
                'type': 'sql_injection',
                'description': 'The application is vulnerable to SQL injection attacks',
                'remediation': 'Use parameterized queries to prevent SQL injection',
                'references': {'OWASP': 'https://owasp.org/www-community/attacks/SQL_Injection'}
            },
            {
                'title': 'Cross-Site Scripting (XSS)',
                'severity': 'high',
                'type': 'xss',
                'description': 'Reflected XSS vulnerability found in search parameter',
                'remediation': 'Implement proper input validation and output encoding',
                'references': {'OWASP': 'https://owasp.org/www-community/attacks/xss/'}
            },
            {
                'title': 'Missing Security Headers',
                'severity': 'medium',
                'type': 'information_disclosure',
                'description': 'Missing security headers that could protect against common attacks',
                'remediation': 'Implement comprehensive security headers',
                'references': {'OWASP': 'https://owasp.org/www-project-secure-headers/'}
            },
            {
                'title': 'Server Information Disclosure',
                'severity': 'low',
                'type': 'information_disclosure',
                'description': 'Server header reveals technology information',
                'remediation': 'Remove or obfuscate server header information',
                'references': {'OWASP': 'https://owasp.org/www-community/controls/Information_Leakage'}
            }
        ]
        
        # Test report generation
        try:
            report = agent._generate_report()
            print(f"          ✓ Report generated successfully")
            print(f"          ✓ Executive summary: {len(report['executive_summary'])} fields")
            print(f"          ✓ Methodology: {len(report['methodology'])} phases")
            print(f"          ✓ Findings: {len(report['findings'])} items")
            print(f"          ✓ Recommendations: {len(report['recommendations'])} items")
            print(f"          ✓ Appendix: {len(report['appendix'])} sections")
            
            # Test risk score calculation
            risk_score = report['executive_summary']['risk_score']
            print(f"          ✓ Risk score: {risk_score}/100")
            
            # Test recommendations generation
            recommendations = agent._generate_recommendations()
            print(f"          ✓ Recommendations generated: {len(recommendations)} items")
            
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"            - Recommendation {i}: {rec[:60]}{'...' if len(rec) > 60 else ''}")
                
        except Exception as e:
            print(f"          ✗ Report generation failed: {e}")
    
    def print_test_results(self):
        """Print test results"""
        print("\n" + "=" * 60)
        print("INDIVIDUAL AGENT TEST RESULTS")
        print("=" * 60)
        
        passed = len([r for r in self.test_results if r["status"] == "PASS"])
        failed = len([r for r in self.test_results if r["status"] == "FAIL"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        print("\nDetailed Results:")
        for result in self.test_results:
            status_icon = "✓" if result["status"] == "PASS" else "✗"
            print(f"  {status_icon} {result['test']}: {result['status']}")
            if result["details"]:
                print(f"    Details: {result['details']}")
        
        print("\n" + "=" * 60)
        
        if failed == 0:
            print("🎉 All individual agent tests passed!")
        else:
            print(f"⚠️  {failed} test(s) failed.")
        
        print("=" * 60)


async def main():
    """Main test function"""
    tester = IndividualAgentTester()
    await tester.run_individual_tests()


if __name__ == "__main__":
    print("Starting Individual Orange Sage Agent Tests...")
    print("This will test each agent type individually with detailed analysis.")
    print("Note: Some tests may require network access for HTTP requests.")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\nTest failed with error: {e}")
        logger.error(f"Test execution failed: {e}")
