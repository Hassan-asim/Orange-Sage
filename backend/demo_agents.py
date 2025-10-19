#!/usr/bin/env python3
"""
Demo script for Orange Sage AI Agents
This script demonstrates how to use the AI agents for security testing
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.agents.pentesting_agent import PentestingAgent
from app.utils.agent_factory import AgentFactory


async def demo_pentesting_agent():
    """Demonstrate PentestingAgent functionality"""
    print("🔍 PentestingAgent Demo")
    print("-" * 40)
    
    # Configuration for the agent
    config = {
        "timeout": 30,
        "max_requests": 5,
        "user_agent": "Orange-Sage-Demo/1.0"
    }
    
    # Test target (safe public service)
    target = "https://httpbin.org"
    
    print(f"Target: {target}")
    print(f"Config: {json.dumps(config, indent=2)}")
    print()
    
    # Create agent
    agent = PentestingAgent("demo-agent-1", target, config)
    print("✓ PentestingAgent created")
    
    # Parse target
    parsed_target = agent._parse_target()
    print(f"✓ Target parsed: {parsed_target['type']} - {parsed_target['hostname']}")
    
    # Make a test request
    print("Making test HTTP request...")
    response = await agent._make_request(target)
    if response:
        print(f"✓ HTTP request successful: {response.status_code}")
        print(f"  Response size: {len(response.text)} bytes")
        print(f"  Server: {response.headers.get('server', 'Unknown')}")
    else:
        print("✗ HTTP request failed")
        return
    
    # Analyze response for security issues
    print("Analyzing response for security issues...")
    agent._analyze_http_response(response, parsed_target)
    print(f"✓ Response analysis completed")
    
    # Show payloads
    print(f"\nPayloads available:")
    print(f"  SQL Injection: {len(agent.payloads['sql_injection'])} payloads")
    print(f"  XSS: {len(agent.payloads['xss'])} payloads")
    print(f"  Command Injection: {len(agent.payloads['command_injection'])} payloads")
    print(f"  Path Traversal: {len(agent.payloads['path_traversal'])} payloads")
    
    # Test vulnerability detection
    print("\nTesting vulnerability detection methods...")
    
    # Mock SQL injection response
    sql_response = type('MockResponse', (), {
        'text': 'mysql_fetch_array() error: Table \'users\' doesn\'t exist',
        'status_code': 200
    })()
    
    sql_detected = agent._detect_sql_injection_response(sql_response)
    print(f"✓ SQL injection detection: {sql_detected}")
    
    # Mock command injection response
    cmd_response = type('MockResponse', (), {
        'text': 'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin',
        'status_code': 200
    })()
    
    cmd_detected = agent._detect_command_injection_response(cmd_response)
    print(f"✓ Command injection detection: {cmd_detected}")
    
    # Mock path traversal response
    path_response = type('MockResponse', (), {
        'text': 'root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin',
        'status_code': 200
    })()
    
    path_detected = agent._detect_path_traversal_response(path_response)
    print(f"✓ Path traversal detection: {path_detected}")
    
    print("\n✓ PentestingAgent demo completed successfully!")


async def demo_agent_factory():
    """Demonstrate AgentFactory functionality"""
    print("\n🏭 AgentFactory Demo")
    print("-" * 40)
    
    # Create factory
    factory = AgentFactory()
    print("✓ AgentFactory created")
    
    # Show available agent types
    available_types = factory.get_available_agent_types()
    print(f"✓ Available agent types: {available_types}")
    
    # Configuration for agents
    config = {
        "agent_id": "demo-agent-1",
        "task": "Perform security assessment of https://httpbin.org",
        "sandbox_info": {"workspace_id": "demo-workspace"},
        "llm_config": {
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 2000
        }
    }
    
    print(f"Agent config: {json.dumps(config, indent=2)}")
    print()
    
    # Create different agent types
    for agent_type in available_types:
        try:
            agent = factory.create_agent(agent_type, config)
            print(f"✓ Created {agent_type}: {type(agent).__name__}")
            
            # Test agent execution (mock)
            if hasattr(agent, 'execute'):
                print(f"  - Has execute() method: ✓")
            if hasattr(agent, 'cancel'):
                print(f"  - Has cancel() method: ✓")
            if hasattr(agent, 'config'):
                print(f"  - Has config: ✓")
                
        except Exception as e:
            print(f"✗ Failed to create {agent_type}: {e}")
    
    print("\n✓ AgentFactory demo completed successfully!")


async def demo_individual_agents():
    """Demonstrate individual agent functionality"""
    print("\n🤖 Individual Agents Demo")
    print("-" * 40)
    
    # Configuration
    config = {
        "agent_id": "demo-agent-1",
        "task": "Comprehensive security assessment",
        "sandbox_info": {"workspace_id": "demo-workspace"},
        "llm_config": {"model_name": "gpt-3.5-turbo"}
    }
    
    # Test OrangeSageAgent
    print("Testing OrangeSageAgent...")
    try:
        from app.utils.agent_factory import OrangeSageAgent
        orange_agent = OrangeSageAgent(config)
        
        # Test initialization
        assessment = await orange_agent._initialize_assessment()
        print(f"✓ Assessment initialized: {assessment['assessment_type']}")
        
        # Test reconnaissance
        recon = await orange_agent._perform_reconnaissance()
        print(f"✓ Reconnaissance completed: {len(recon)} data points")
        
        # Test vulnerability testing
        vuln = await orange_agent._perform_vulnerability_testing()
        print(f"✓ Vulnerability testing: {vuln['tests_performed']} tests")
        
        # Test finding generation
        findings = await orange_agent._generate_findings(assessment, recon, vuln)
        print(f"✓ Generated {len(findings)} findings")
        
        # Show sample findings
        if findings:
            print("  Sample findings:")
            for i, finding in enumerate(findings[:2]):  # Show first 2 findings
                print(f"    {i+1}. {finding['title']} ({finding['severity']})")
        
    except Exception as e:
        print(f"✗ OrangeSageAgent demo failed: {e}")
    
    print("\n✓ Individual agents demo completed!")


async def main():
    """Main demo function"""
    print("🚀 Orange Sage AI Agents Demo")
    print("=" * 50)
    print("This demo shows the functionality of Orange Sage AI agents")
    print("for security testing and assessment.")
    print()
    
    try:
        # Demo 1: PentestingAgent
        await demo_pentesting_agent()
        
        # Demo 2: AgentFactory
        await demo_agent_factory()
        
        # Demo 3: Individual Agents
        await demo_individual_agents()
        
        print("\n" + "=" * 50)
        print("🎉 All demos completed successfully!")
        print("Orange Sage AI agents are ready for security testing.")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    print("Starting Orange Sage AI Agents Demo...")
    print("This will demonstrate the functionality of various AI agents.")
    print("Note: Some demos may require network access for HTTP requests.")
    print()
    
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nDemo failed with error: {e}")
        sys.exit(1)
