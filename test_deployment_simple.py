#!/usr/bin/env python3
"""
Simple test script for LangGraph deployment using direct HTTP requests
"""

import requests
import json
from datetime import datetime

# Deployment configuration
DEPLOYMENT_ID = "03e9a719-ff0b-40bb-8e5c-548ff6ae0abf"
DEPLOYMENT_URL = f"https://langraph-cloud-{DEPLOYMENT_ID}.app.langgraph.dev"
LANGSMITH_API_KEY = "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"
ASSISTANT_ID = "agent"

def test_deployment_health():
    """Test if deployment is accessible"""
    print(f"\n=== Testing Deployment Health ===")
    print(f"URL: {DEPLOYMENT_URL}")
    
    try:
        # Try to access the base URL
        response = requests.get(
            DEPLOYMENT_URL,
            headers={"X-Api-Key": LANGSMITH_API_KEY},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response.status_code < 500
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print(f"\n=== Testing API Endpoints ===")
    
    endpoints = [
        "/health",
        "/assistants",
        f"/assistants/{ASSISTANT_ID}",
    ]
    
    for endpoint in endpoints:
        url = f"{DEPLOYMENT_URL}{endpoint}"
        print(f"\nTesting {endpoint}...")
        try:
            response = requests.get(
                url,
                headers={"X-Api-Key": LANGSMITH_API_KEY},
                timeout=10
            )
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                print(f"  Response: {json.dumps(response.json(), indent=2)[:200]}...")
        except Exception as e:
            print(f"  ❌ Failed: {str(e)}")

def test_conversation_api():
    """Test conversation via REST API"""
    print(f"\n=== Testing Conversation API ===")
    
    url = f"{DEPLOYMENT_URL}/runs/stream"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": LANGSMITH_API_KEY
    }
    
    payload = {
        "assistant_id": ASSISTANT_ID,
        "input": {
            "contact_id": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "conversation_id": f"conv-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "message": "Hello, I need help with a website",
            "conversation_history": []
        },
        "stream_mode": "updates"
    }
    
    print(f"Sending request to: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
            stream=True
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response stream:")
            for line in response.iter_lines():
                if line:
                    print(f"  {line.decode('utf-8')}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

def main():
    print(f"""
    ====================================
    LangGraph Deployment Simple Test
    ====================================
    Deployment ID: {DEPLOYMENT_ID}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    """)
    
    # First check if we can resolve the hostname
    import socket
    try:
        hostname = f"langraph-cloud-{DEPLOYMENT_ID}.app.langgraph.dev"
        print(f"\nResolving hostname: {hostname}")
        ip = socket.gethostbyname(hostname)
        print(f"✅ Resolved to: {ip}")
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        print("\nPossible issues:")
        print("1. The deployment URL might be incorrect")
        print("2. The deployment might not be active")
        print("3. There might be network/DNS issues")
        
        # Try alternative URL formats
        alt_urls = [
            f"https://{DEPLOYMENT_ID}.langraph.app",
            f"https://api.langraph.cloud/deployments/{DEPLOYMENT_ID}",
            f"https://langraph-api-{DEPLOYMENT_ID}.langchain.com"
        ]
        
        print("\nTrying alternative URL formats:")
        for alt_url in alt_urls:
            try:
                hostname = alt_url.replace("https://", "").split("/")[0]
                print(f"\n  Trying: {hostname}")
                ip = socket.gethostbyname(hostname)
                print(f"  ✅ Resolved to: {ip}")
                DEPLOYMENT_URL = alt_url
                break
            except:
                print(f"  ❌ Failed")
                continue
    
    # Run tests
    test_deployment_health()
    test_api_endpoints()
    test_conversation_api()

if __name__ == "__main__":
    main()