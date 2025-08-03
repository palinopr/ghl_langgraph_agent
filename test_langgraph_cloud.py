#!/usr/bin/env python3
"""
Test script for LangGraph Cloud deployment
Helps identify the correct deployment URL format
"""

import os
import asyncio
from datetime import datetime
from langgraph_sdk import get_client
import json

# LangSmith API key from environment
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")

# Possible deployment URL formats based on documentation
DEPLOYMENT_URLS = [
    # Most common format based on docs
    "https://ghl-customer-agent-palinopr.app.langgraph.dev",
    "https://ghl-customer-agent.app.langgraph.dev",
    
    # With deployment ID
    f"https://deployment-03e9a719-ff0b-40bb-8e5c-548ff6ae0abf.app.langgraph.dev",
    f"https://03e9a719-ff0b-40bb-8e5c-548ff6ae0abf.app.langgraph.dev",
    
    # Legacy formats
    f"https://langraph-cloud-03e9a719-ff0b-40bb-8e5c-548ff6ae0abf.app.langgraph.dev",
    
    # Alternative patterns
    "https://api.smith.langchain.com/deployments/ghl-customer-agent",
    f"https://api.smith.langchain.com/deployments/03e9a719-ff0b-40bb-8e5c-548ff6ae0abf",
]

ASSISTANT_ID = "agent"  # From langgraph.json


async def test_deployment_url(url):
    """Test if a deployment URL is valid"""
    print(f"\n📡 Testing URL: {url}")
    
    try:
        # Try to create a client
        client = get_client(url=url, api_key=LANGSMITH_API_KEY)
        
        # Try to list assistants
        print("  🔍 Checking assistants...")
        assistants = await client.assistants.list()
        print(f"  ✅ Found {len(assistants)} assistants")
        
        # Try to get specific assistant
        try:
            assistant = await client.assistants.get(ASSISTANT_ID)
            print(f"  ✅ Found assistant '{ASSISTANT_ID}'")
            return url, True
        except Exception as e:
            print(f"  ⚠️  Assistant '{ASSISTANT_ID}' not found: {str(e)}")
            return url, False
            
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        return url, False


async def test_simple_conversation(client):
    """Test a simple conversation"""
    print("\n🤖 Testing conversation...")
    
    contact_id = f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    try:
        # Stream a simple message
        print(f"  📤 Sending message...")
        response_chunks = []
        
        async for chunk in client.runs.stream(
            None,  # Threadless run
            ASSISTANT_ID,
            input={
                "contact_id": contact_id,
                "conversation_id": f"conv-{contact_id}",
                "message": "Hello, I need help with a battery system for my home",
                "conversation_history": []
            },
            stream_mode="updates",
        ):
            print(f"  📥 Event: {chunk.event}")
            if chunk.data:
                response_chunks.append(chunk.data)
                
        print(f"  ✅ Conversation successful!")
        print(f"  💬 Received {len(response_chunks)} response chunks")
        return True
        
    except Exception as e:
        print(f"  ❌ Conversation failed: {str(e)}")
        return False


async def main():
    print(f"""
    ====================================
    LangGraph Cloud Deployment Tester
    ====================================
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Testing multiple URL formats...
    ====================================
    """)
    
    # Test all possible URLs
    print("🔍 Phase 1: Finding correct deployment URL")
    valid_urls = []
    
    for url in DEPLOYMENT_URLS:
        result_url, is_valid = await test_deployment_url(url)
        if is_valid:
            valid_urls.append(result_url)
    
    if not valid_urls:
        print("\n❌ No valid deployment URLs found!")
        print("\n📋 Troubleshooting steps:")
        print("1. Check deployment name in LangSmith UI")
        print("2. Verify deployment is active")
        print("3. Check API key permissions")
        print("\n💡 To find your deployment URL:")
        print("   1. Go to https://smith.langchain.com")
        print("   2. Click on 'Deployments' in sidebar")
        print("   3. Find 'ghl-customer-agent' deployment")
        print("   4. Copy the deployment URL")
        return
    
    # Use the first valid URL for conversation test
    deployment_url = valid_urls[0]
    print(f"\n✅ Found valid deployment URL: {deployment_url}")
    
    # Test conversation
    print("\n🔍 Phase 2: Testing conversation")
    client = get_client(url=deployment_url, api_key=LANGSMITH_API_KEY)
    
    success = await test_simple_conversation(client)
    
    if success:
        print(f"\n🎉 SUCCESS! Your deployment is working at:")
        print(f"   {deployment_url}")
        print(f"\n📝 Use this URL in your applications:")
        print(f"   client = get_client(url='{deployment_url}', api_key=LANGSMITH_API_KEY)")
    else:
        print(f"\n⚠️  Deployment found but conversation test failed")
        print("Check your agent configuration and environment variables")


if __name__ == "__main__":
    # First, let's check if we can import the SDK
    try:
        from langgraph_sdk import get_client
        print("✅ LangGraph SDK is installed")
    except ImportError:
        print("❌ LangGraph SDK not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "langgraph-sdk"])
        from langgraph_sdk import get_client
    
    # Run the tests
    asyncio.run(main())