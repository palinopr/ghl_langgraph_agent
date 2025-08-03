#!/usr/bin/env python3
"""
Simple test for LangGraph Cloud deployment using correct SDK methods
"""

import asyncio
import os
from datetime import datetime
from langgraph_sdk import get_client
import json

# Configuration
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")
ASSISTANT_ID = "agent"

# Test URLs - you need to find the correct one from LangSmith UI
TEST_URLS = [
    # Most likely format based on deployment name
    "https://ghl-customer-agent.app.langchain.com",
    "https://ghl-customer-agent.langgraph.app", 
    "https://ghl-customer-agent-76c2a36c0d.app.langgraph.dev",
    
    # Using deployment ID
    "https://03e9a719-ff0b-40bb-8e5c-548ff6ae0abf.app.langgraph.dev",
    "https://deployment-03e9a719-ff0b-40bb-8e5c-548ff6ae0abf.app.langgraph.dev",
]


async def test_deployment(url):
    """Test a deployment URL with a simple conversation"""
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    print(f"{'='*60}")
    
    try:
        # Create client
        client = get_client(url=url, api_key=LANGSMITH_API_KEY)
        
        # Create test input
        test_input = {
            "contact_id": f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "conversation_id": f"conv-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "message": "Hello, I need help with a battery storage system",
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
                print(f"Data type: {type(chunk.data)}")
                print(f"Data: {json.dumps(chunk.data, indent=2) if isinstance(chunk.data, dict) else chunk.data}")
                response_data.append(chunk.data)
        
        print(f"\n✅ SUCCESS! Deployment is working at: {url}")
        print(f"Total chunks received: {len(response_data)}")
        
        # Save working URL
        with open("working_deployment_url.txt", "w") as f:
            f.write(f"DEPLOYMENT_URL={url}\n")
            f.write(f"ASSISTANT_ID={ASSISTANT_ID}\n")
            f.write(f"Tested at: {datetime.now()}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed: {str(e)}")
        if "404" in str(e):
            print("   → Deployment not found at this URL")
        elif "401" in str(e) or "403" in str(e):
            print("   → Authentication failed - check API key")
        elif "NameResolutionError" in str(e) or "nodename" in str(e):
            print("   → URL doesn't exist")
        else:
            print(f"   → Error details: {type(e).__name__}")
        return False


async def test_with_curl_format():
    """Show curl command format for manual testing"""
    print("\n" + "="*60)
    print("Manual Testing with curl")
    print("="*60)
    
    print("\nIf the SDK tests fail, try these curl commands:")
    
    for url in TEST_URLS[:3]:  # Show first 3 examples
        print(f"\n# Test {url}")
        print(f"curl -X POST {url}/runs/stream \\")
        print(f"  -H 'Content-Type: application/json' \\")
        print(f"  -H 'X-Api-Key: {LANGSMITH_API_KEY}' \\")
        print(f"  -d '{{")
        print(f'    "assistant_id": "{ASSISTANT_ID}",')
        print(f'    "input": {{')
        print(f'      "contact_id": "test-123",')
        print(f'      "conversation_id": "conv-123",')
        print(f'      "message": "Hello",')
        print(f'      "conversation_history": []')
        print(f'    }},')
        print(f'    "stream_mode": "updates"')
        print(f"  }}'")


async def main():
    print(f"""
    ====================================
    LangGraph Cloud Simple Tester
    ====================================
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Assistant ID: {ASSISTANT_ID}
    ====================================
    
    IMPORTANT: The deployment URL should be visible in:
    1. LangSmith UI → Deployments → ghl-customer-agent
    2. The deployment details page
    3. Or in the deployment confirmation email
    """)
    
    # Test each URL
    success = False
    for url in TEST_URLS:
        if await test_deployment(url):
            success = True
            break
    
    if not success:
        print("\n" + "="*60)
        print("❌ No working deployment URL found")
        print("="*60)
        
        await test_with_curl_format()
        
        print("\n📋 Next Steps:")
        print("1. Go to https://smith.langchain.com")
        print("2. Navigate to Deployments")
        print("3. Find 'ghl-customer-agent' or deployment ID '03e9a719-ff0b-40bb-8e5c-548ff6ae0abf'")
        print("4. Copy the exact deployment URL shown there")
        print("5. Update TEST_URLS in this script with the correct URL")
    else:
        print("\n🎉 Deployment test successful!")
        print("Check 'working_deployment_url.txt' for the working configuration")


if __name__ == "__main__":
    asyncio.run(main())