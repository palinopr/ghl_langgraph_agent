#!/usr/bin/env python3
"""
Test script for LangSmith hosted deployment
"""

import asyncio
import os
from datetime import datetime
from langgraph_sdk import get_client
import json
import requests

# Configuration from the deployment URL
ORGANIZATION_ID = "d46348af-8871-4fc1-bb27-5d17f0589bd5"
DEPLOYMENT_ID = "03e9a719-ff0b-40bb-8e5c-548ff6ae0abf"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")
ASSISTANT_ID = "agent"

# LangSmith hosted deployments use a specific URL format
DEPLOYMENT_URL = f"https://api.smith.langchain.com"


async def test_with_sdk():
    """Test using the LangGraph SDK"""
    print("\n=== Testing with LangGraph SDK ===")
    
    try:
        # For LangSmith hosted deployments, we need to use the deployment ID
        client = get_client(
            url=DEPLOYMENT_URL,
            api_key=LANGSMITH_API_KEY,
            default_headers={
                "X-Deployment-Id": DEPLOYMENT_ID,
                "X-Organization-Id": ORGANIZATION_ID
            }
        )
        
        # Create test input
        test_input = {
            "contact_id": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "conversation_id": f"conv-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "message": "Hello, I need help with a battery storage system for my home",
            "conversation_history": []
        }
        
        print(f"Sending message: {test_input['message']}")
        print("Streaming response...")
        
        # Stream the conversation
        response_data = []
        async for chunk in client.runs.stream(
            None,  # No thread (stateless)
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            print(f"\n📥 Event: {chunk.event}")
            if hasattr(chunk, 'data') and chunk.data:
                print(f"Data: {json.dumps(chunk.data, indent=2) if isinstance(chunk.data, dict) else chunk.data}")
                response_data.append(chunk.data)
        
        print(f"\n✅ SUCCESS! Received {len(response_data)} response chunks")
        return True
        
    except Exception as e:
        print(f"\n❌ SDK test failed: {str(e)}")
        return False


def test_with_requests():
    """Test using direct HTTP requests"""
    print("\n=== Testing with HTTP Requests ===")
    
    # Try different endpoint patterns
    endpoints = [
        f"{DEPLOYMENT_URL}/v1/deployments/{DEPLOYMENT_ID}/runs/stream",
        f"{DEPLOYMENT_URL}/deployments/{DEPLOYMENT_ID}/runs/stream",
        f"{DEPLOYMENT_URL}/o/{ORGANIZATION_ID}/deployments/{DEPLOYMENT_ID}/runs/stream",
    ]
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": LANGSMITH_API_KEY,
        "Authorization": f"Bearer {LANGSMITH_API_KEY}",
    }
    
    payload = {
        "assistant_id": ASSISTANT_ID,
        "input": {
            "contact_id": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "conversation_id": f"conv-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "message": "Hello, I need help with a battery storage system",
            "conversation_history": []
        },
        "stream_mode": "updates"
    }
    
    for endpoint in endpoints:
        print(f"\nTrying endpoint: {endpoint}")
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=30,
                stream=True
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Success! Response:")
                for line in response.iter_lines():
                    if line:
                        print(f"  {line.decode('utf-8')}")
                        # Just show first few lines
                        break
                return True
            else:
                print(f"Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
    
    return False


def show_curl_commands():
    """Show curl commands for manual testing"""
    print("\n=== Manual Testing Commands ===")
    
    print("\nOption 1: With deployment ID in header")
    print(f"""
curl -X POST https://api.smith.langchain.com/runs/stream \\
  -H 'Content-Type: application/json' \\
  -H 'X-API-Key: {LANGSMITH_API_KEY}' \\
  -H 'X-Deployment-Id: {DEPLOYMENT_ID}' \\
  -H 'X-Organization-Id: {ORGANIZATION_ID}' \\
  -d '{{
    "assistant_id": "{ASSISTANT_ID}",
    "input": {{
      "contact_id": "test-123",
      "conversation_id": "conv-123",
      "message": "Hello, I need help with a battery system",
      "conversation_history": []
    }},
    "stream_mode": "updates"
  }}'
""")
    
    print("\nOption 2: With deployment ID in URL")
    print(f"""
curl -X POST https://api.smith.langchain.com/v1/deployments/{DEPLOYMENT_ID}/runs/stream \\
  -H 'Content-Type: application/json' \\
  -H 'X-API-Key: {LANGSMITH_API_KEY}' \\
  -d '{{
    "assistant_id": "{ASSISTANT_ID}",
    "input": {{
      "contact_id": "test-123",
      "conversation_id": "conv-123",
      "message": "Hello, I need help with a battery system",
      "conversation_history": []
    }},
    "stream_mode": "updates"
  }}'
""")


async def main():
    print(f"""
    ====================================
    LangSmith Deployment Test
    ====================================
    Organization ID: {ORGANIZATION_ID}
    Deployment ID: {DEPLOYMENT_ID}
    Assistant ID: {ASSISTANT_ID}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    """)
    
    # Test with SDK
    sdk_success = await test_with_sdk()
    
    # Test with direct HTTP
    http_success = test_with_requests()
    
    # Show manual commands
    show_curl_commands()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"SDK Test: {'✅ PASSED' if sdk_success else '❌ FAILED'}")
    print(f"HTTP Test: {'✅ PASSED' if http_success else '❌ FAILED'}")
    
    if not sdk_success and not http_success:
        print("\n📋 Troubleshooting:")
        print("1. Verify the deployment is active in LangSmith")
        print("2. Check that environment variables are set in the deployment")
        print("3. Ensure the API key has proper permissions")
        print("4. Try the manual curl commands above")
        print("\n🔗 Deployment URL:")
        print(f"   https://smith.langchain.com/o/{ORGANIZATION_ID}/host/deployments/{DEPLOYMENT_ID}")


if __name__ == "__main__":
    asyncio.run(main())