#!/usr/bin/env python3
"""
Final test script for LangGraph Cloud deployment
Using the correct deployment URL from LangSmith
"""

import asyncio
import os
from datetime import datetime
from langgraph_sdk import get_client
import json
import time

# Configuration
DEPLOYMENT_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")
ASSISTANT_ID = "ghl_agent"  # The registered graph name


async def test_basic_conversation():
    """Test basic conversation flow"""
    print("\n" + "="*60)
    print("TEST 1: Basic Conversation")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    test_input = {
        "contact_id": f"test-basic-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-basic-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "message": "Hello, I need help with a battery storage system for my home",
        "conversation_history": []
    }
    
    print(f"Contact ID: {test_input['contact_id']}")
    print(f"Message: {test_input['message']}")
    print("\nStreaming response...")
    
    try:
        response_text = ""
        event_count = 0
        
        async for chunk in client.runs.stream(
            None,  # Threadless run
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            event_count += 1
            print(f"\n📥 Event {event_count}: {chunk.event}")
            
            if hasattr(chunk, 'data') and chunk.data:
                if isinstance(chunk.data, dict):
                    print(f"Data keys: {list(chunk.data.keys())}")
                    
                    # Extract response text if available
                    if 'response' in chunk.data:
                        response_text = chunk.data['response']
                        print(f"Response: {response_text}")
                    
                    # Show other relevant data
                    for key, value in chunk.data.items():
                        if key != 'response' and value:
                            print(f"{key}: {json.dumps(value, indent=2) if isinstance(value, (dict, list)) else value}")
        
        print(f"\n✅ Test completed successfully!")
        print(f"Total events received: {event_count}")
        if response_text:
            print(f"\nAgent's final response:\n{response_text}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def test_qualification_flow():
    """Test lead qualification with different budget scenarios"""
    print("\n" + "="*60)
    print("TEST 2: Lead Qualification Flow")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    # Test unqualified lead (budget < $5000)
    print("\n--- Testing Unqualified Lead (Low Budget) ---")
    
    conversation_history = [
        {
            "role": "assistant",
            "content": "Hello! I'd love to help you with your battery storage needs. Could you tell me more about your project?"
        },
        {
            "role": "user",
            "content": "I need a battery system for my small cabin"
        }
    ]
    
    test_input = {
        "contact_id": f"test-unqualified-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-unqualified-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "message": "My budget is around $3000",
        "conversation_history": conversation_history
    }
    
    print(f"Testing with budget: $3000 (below $5000 minimum)")
    
    try:
        response_text = ""
        async for chunk in client.runs.stream(
            None,
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                if 'response' in chunk.data:
                    response_text = chunk.data['response']
        
        print(f"\nAgent response: {response_text}")
        print("Expected: Agent should politely indicate budget doesn't meet minimum")
        
    except Exception as e:
        print(f"❌ Unqualified lead test failed: {str(e)}")
    
    # Wait a bit before next test
    await asyncio.sleep(2)
    
    # Test qualified lead (budget >= $5000)
    print("\n--- Testing Qualified Lead (High Budget) ---")
    
    conversation_history = [
        {
            "role": "assistant",
            "content": "Hello! I'd love to help you with your battery storage needs. Could you tell me more about your project?"
        },
        {
            "role": "user",
            "content": "I need a comprehensive battery backup system for my business"
        }
    ]
    
    test_input = {
        "contact_id": f"test-qualified-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-qualified-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "message": "My budget is $15000",
        "conversation_history": conversation_history
    }
    
    print(f"Testing with budget: $15000 (above $5000 minimum)")
    
    try:
        response_text = ""
        tool_calls = []
        
        async for chunk in client.runs.stream(
            None,
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                if 'response' in chunk.data:
                    response_text = chunk.data['response']
                if 'tool_calls' in chunk.data:
                    tool_calls.extend(chunk.data['tool_calls'])
        
        print(f"\nAgent response: {response_text}")
        print("Expected: Agent should proceed to schedule appointment")
        
        if tool_calls:
            print(f"\nTool calls made: {[tc.get('tool', 'unknown') for tc in tool_calls]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Qualified lead test failed: {str(e)}")
        return False


async def test_thread_persistence():
    """Test conversation with thread persistence"""
    print("\n" + "="*60)
    print("TEST 3: Thread Persistence")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    try:
        # Create a thread
        thread = await client.threads.create()
        thread_id = thread["thread_id"]
        print(f"Created thread: {thread_id}")
        
        contact_id = f"test-thread-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # First message
        print("\n--- First Message ---")
        test_input = {
            "contact_id": contact_id,
            "conversation_id": f"conv-thread-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "message": "Hi, I'm interested in battery storage",
            "conversation_history": []
        }
        
        async for chunk in client.runs.stream(
            thread_id,
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                if 'response' in chunk.data:
                    print(f"Response: {chunk.data['response']}")
        
        # Wait a bit
        await asyncio.sleep(2)
        
        # Follow-up message
        print("\n--- Follow-up Message ---")
        test_input["message"] = "It's for a 5000 sq ft warehouse"
        
        async for chunk in client.runs.stream(
            thread_id,
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                if 'response' in chunk.data:
                    print(f"Response: {chunk.data['response']}")
        
        print(f"\n✅ Thread persistence test completed")
        return True
        
    except Exception as e:
        print(f"\n❌ Thread test failed: {str(e)}")
        return False


async def test_battery_specific_conversation():
    """Test battery-specific consultation flow"""
    print("\n" + "="*60)
    print("TEST 4: Battery Consultation Specifics")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    test_scenarios = [
        {
            "name": "Solar Integration",
            "message": "I have a 10kW solar system and want to add battery backup",
            "budget": "$12000"
        },
        {
            "name": "Business Continuity",
            "message": "I need backup power for my data center, critical loads only",
            "budget": "$25000"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- Scenario: {scenario['name']} ---")
        
        contact_id = f"test-{scenario['name'].lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Initial message
        test_input = {
            "contact_id": contact_id,
            "conversation_id": f"conv-{contact_id}",
            "message": scenario["message"],
            "conversation_history": []
        }
        
        try:
            response_text = ""
            async for chunk in client.runs.stream(
                None,
                ASSISTANT_ID,
                input=test_input,
                stream_mode="updates",
            ):
                if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                    if 'response' in chunk.data:
                        response_text = chunk.data['response']
            
            print(f"Initial response: {response_text[:200]}...")
            
            # Follow up with budget
            await asyncio.sleep(2)
            
            test_input["message"] = f"My budget is {scenario['budget']}"
            test_input["conversation_history"] = [
                {"role": "assistant", "content": response_text},
                {"role": "user", "content": scenario["message"]}
            ]
            
            async for chunk in client.runs.stream(
                None,
                ASSISTANT_ID,
                input=test_input,
                stream_mode="updates",
            ):
                if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                    if 'response' in chunk.data:
                        response_text = chunk.data['response']
            
            print(f"Budget response: {response_text[:200]}...")
            
        except Exception as e:
            print(f"❌ Scenario failed: {str(e)}")
        
        await asyncio.sleep(2)
    
    return True


async def main():
    print(f"""
    ====================================
    LangGraph Cloud Deployment Test
    ====================================
    Deployment URL: {DEPLOYMENT_URL}
    Assistant ID: {ASSISTANT_ID}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    """)
    
    # Save deployment info
    with open("deployment_info.txt", "w") as f:
        f.write(f"DEPLOYMENT_URL={DEPLOYMENT_URL}\n")
        f.write(f"ASSISTANT_ID={ASSISTANT_ID}\n")
        f.write(f"LANGSMITH_API_KEY={LANGSMITH_API_KEY}\n")
        f.write(f"Tested at: {datetime.now()}\n")
    
    # Run all tests
    tests = [
        ("Basic Conversation", test_basic_conversation),
        ("Lead Qualification", test_qualification_flow),
        ("Thread Persistence", test_thread_persistence),
        ("Battery Consultation", test_battery_specific_conversation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🚀 Starting: {test_name}")
            success = await test_func()
            results.append((test_name, success))
            await asyncio.sleep(3)  # Pause between tests
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    print(f"\n🔗 Deployment URL: {DEPLOYMENT_URL}")
    print("📄 Deployment info saved to: deployment_info.txt")


if __name__ == "__main__":
    asyncio.run(main())