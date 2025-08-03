#!/usr/bin/env python3
"""
Test script for LangGraph deployment: 03e9a719-ff0b-40bb-8e5c-548ff6ae0abf
Tests the GHL customer service agent deployment on LangSmith
"""

import asyncio
import os
from datetime import datetime
from langgraph_sdk import get_client
import json
from typing import Dict, Any

# Deployment configuration
DEPLOYMENT_ID = "03e9a719-ff0b-40bb-8e5c-548ff6ae0abf"
DEPLOYMENT_URL = f"https://langraph-cloud-{DEPLOYMENT_ID}.app.langgraph.dev"
ASSISTANT_ID = "agent"  # From langgraph.json

# Get API key from environment
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
if not LANGSMITH_API_KEY:
    print("Error: LANGSMITH_API_KEY environment variable not set")
    print("Please set it with: export LANGSMITH_API_KEY='your-api-key'")
    exit(1)

# Test contact IDs for different scenarios
TEST_CONTACT_ID = f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}"
TEST_CONVERSATION_ID = f"conv-{datetime.now().strftime('%Y%m%d%H%M%S')}"


async def test_basic_conversation():
    """Test basic conversation flow"""
    print("\n=== Testing Basic Conversation ===")
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    try:
        print(f"Using contact ID: {TEST_CONTACT_ID}")
        print("Sending: 'Hello, I need help with a website'")
        
        response_text = ""
        async for chunk in client.runs.stream(
            None,  # Threadless run
            ASSISTANT_ID,
            input={
                "contact_id": TEST_CONTACT_ID,
                "conversation_id": TEST_CONVERSATION_ID,
                "message": "Hello, I need help with a website",
                "conversation_history": []
            },
            stream_mode="updates",
        ):
            print(f"\nEvent type: {chunk.event}")
            if chunk.data:
                print(f"Data: {json.dumps(chunk.data, indent=2)}")
                # Extract response message if available
                if isinstance(chunk.data, dict) and "response" in chunk.data:
                    response_text = chunk.data["response"]
        
        print(f"\n✅ Basic conversation test completed")
        print(f"Agent response: {response_text}")
        return True
        
    except Exception as e:
        print(f"\n❌ Basic conversation test failed: {str(e)}")
        return False


async def test_qualification_flow():
    """Test lead qualification with budget discussion"""
    print("\n=== Testing Lead Qualification Flow ===")
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    # Simulate conversation history
    conversation_history = [
        {
            "role": "assistant",
            "content": "Hello! I'd love to help you with your website project. To better understand your needs, could you tell me more about what kind of website you're looking for?"
        },
        {
            "role": "user", 
            "content": "I need an e-commerce website for my small business"
        }
    ]
    
    try:
        print(f"Using contact ID: {TEST_CONTACT_ID}")
        print("Testing budget qualification...")
        print("Sending: 'My budget is around $3000'")
        
        response_text = ""
        async for chunk in client.runs.stream(
            None,
            ASSISTANT_ID,
            input={
                "contact_id": TEST_CONTACT_ID,
                "conversation_id": TEST_CONVERSATION_ID,
                "message": "My budget is around $3000",
                "conversation_history": conversation_history
            },
            stream_mode="updates",
        ):
            print(f"\nEvent type: {chunk.event}")
            if chunk.data:
                print(f"Data: {json.dumps(chunk.data, indent=2)}")
                if isinstance(chunk.data, dict) and "response" in chunk.data:
                    response_text = chunk.data["response"]
        
        print(f"\n✅ Qualification test completed")
        print(f"Agent response: {response_text}")
        print("Expected: Agent should indicate budget doesn't meet $5000 minimum")
        return True
        
    except Exception as e:
        print(f"\n❌ Qualification test failed: {str(e)}")
        return False


async def test_qualified_lead():
    """Test flow with a qualified lead (budget > $5000)"""
    print("\n=== Testing Qualified Lead Flow ===")
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    qualified_contact_id = f"qualified-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Simulate conversation history for qualified lead
    conversation_history = [
        {
            "role": "assistant",
            "content": "Hello! I'd love to help you with your website project. Could you tell me more about what you're looking for?"
        },
        {
            "role": "user",
            "content": "I need a professional website with custom features"
        },
        {
            "role": "assistant",
            "content": "That sounds great! To ensure we can deliver the quality you need, could you share your budget range for this project?"
        }
    ]
    
    try:
        print(f"Using contact ID: {qualified_contact_id}")
        print("Sending: 'My budget is $8000'")
        
        response_text = ""
        async for chunk in client.runs.stream(
            None,
            ASSISTANT_ID,
            input={
                "contact_id": qualified_contact_id,
                "conversation_id": f"conv-qualified-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "message": "My budget is $8000",
                "conversation_history": conversation_history
            },
            stream_mode="updates",
        ):
            print(f"\nEvent type: {chunk.event}")
            if chunk.data:
                print(f"Data: {json.dumps(chunk.data, indent=2)}")
                if isinstance(chunk.data, dict) and "response" in chunk.data:
                    response_text = chunk.data["response"]
        
        print(f"\n✅ Qualified lead test completed")
        print(f"Agent response: {response_text}")
        print("Expected: Agent should proceed to schedule appointment")
        return True
        
    except Exception as e:
        print(f"\n❌ Qualified lead test failed: {str(e)}")
        return False


async def test_thread_conversation():
    """Test conversation with thread persistence"""
    print("\n=== Testing Thread-based Conversation ===")
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    try:
        # Create a thread
        thread = await client.threads.create()
        print(f"Created thread: {thread['thread_id']}")
        
        # Send first message
        print("\nSending first message: 'Hi, I need a website'")
        async for chunk in client.runs.stream(
            thread["thread_id"],
            ASSISTANT_ID,
            input={
                "contact_id": TEST_CONTACT_ID,
                "conversation_id": TEST_CONVERSATION_ID,
                "message": "Hi, I need a website",
                "conversation_history": []
            },
            stream_mode="updates",
        ):
            if chunk.event == "updates":
                print(f"Update: {chunk.data}")
        
        # Send follow-up message
        print("\nSending follow-up: 'It's for my restaurant business'")
        async for chunk in client.runs.stream(
            thread["thread_id"],
            ASSISTANT_ID,
            input={
                "contact_id": TEST_CONTACT_ID,
                "conversation_id": TEST_CONVERSATION_ID,
                "message": "It's for my restaurant business",
                "conversation_history": []  # Thread should maintain history
            },
            stream_mode="updates",
        ):
            if chunk.event == "updates":
                print(f"Update: {chunk.data}")
        
        print(f"\n✅ Thread conversation test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Thread conversation test failed: {str(e)}")
        return False


async def main():
    """Run all tests"""
    print(f"""
    ====================================
    LangGraph Deployment Test Suite
    ====================================
    Deployment ID: {DEPLOYMENT_ID}
    URL: {DEPLOYMENT_URL}
    Assistant: {ASSISTANT_ID}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    """)
    
    # Run tests
    tests = [
        ("Basic Conversation", test_basic_conversation),
        ("Lead Qualification", test_qualification_flow),
        ("Qualified Lead", test_qualified_lead),
        ("Thread Conversation", test_thread_conversation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")


if __name__ == "__main__":
    asyncio.run(main())