#!/usr/bin/env python3
"""
Comprehensive test script for LangGraph Cloud deployment
Based on official LangGraph documentation
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import httpx

# Try both sync and async clients
try:
    from langgraph_sdk import get_client
    from langgraph_sdk import get_sync_client
    HAS_SDK = True
except ImportError:
    HAS_SDK = False
    print("⚠️  LangGraph SDK not installed. Install with: pip install langgraph-sdk")


class DeploymentTestConfig(BaseModel):
    """Configuration for deployment testing"""
    deployment_url: str
    api_key: str
    assistant_id: str = "ghl_agent"  # From your langgraph.json
    test_contact_id: str = "test-cloud-123"
    test_conversation_id: str = "conv-cloud-123"


async def test_with_sdk(config: DeploymentTestConfig):
    """Test deployment using the official LangGraph SDK"""
    print("\n=== Testing with LangGraph SDK (Async) ===\n")
    
    try:
        # Initialize client
        client = get_client(url=config.deployment_url, api_key=config.api_key)
        print(f"✅ Connected to deployment: {config.deployment_url}")
        
        # Test 1: List assistants
        print("\n📋 Listing assistants...")
        assistants = await client.assistants.search()
        print(f"Found {len(assistants)} assistants")
        for assistant in assistants:
            print(f"  - {assistant['name']} (ID: {assistant['assistant_id']})")
        
        # Test 2: Get specific assistant
        print(f"\n🔍 Getting assistant '{config.assistant_id}'...")
        try:
            assistant = await client.assistants.get(config.assistant_id)
            print(f"✅ Found assistant: {assistant['name']}")
            print(f"   Config: {json.dumps(assistant.get('config', {}), indent=2)}")
        except Exception as e:
            print(f"⚠️  Assistant not found, creating one...")
            # Create assistant if it doesn't exist
            assistant = await client.assistants.create(
                graph_id=config.assistant_id,
                name="GHL Battery Consultation Agent",
                config={
                    "configurable": {
                        "model_name": "gpt-4-turbo-preview",
                        "temperature": 0.7
                    }
                }
            )
            print(f"✅ Created assistant: {assistant['assistant_id']}")
        
        # Test 3: Create a thread
        print("\n🧵 Creating thread...")
        thread = await client.threads.create(
            metadata={
                "source": "cloud_test",
                "contact_id": config.test_contact_id
            }
        )
        thread_id = thread["thread_id"]
        print(f"✅ Created thread: {thread_id}")
        
        # Test 4: Run with streaming
        print("\n🚀 Running graph with streaming...")
        input_data = {
            "messages": [
                {"role": "human", "content": "Hola, necesito ayuda con baterías para mi casa"}
            ],
            "contact_id": config.test_contact_id,
            "conversation_id": config.test_conversation_id
        }
        
        print("Streaming updates...")
        events_received = []
        async for chunk in client.runs.stream(
            thread_id=thread_id,
            assistant_id=config.assistant_id,
            input=input_data,
            stream_mode=["updates", "messages", "events"]
        ):
            event_type = chunk.event
            events_received.append(event_type)
            print(f"  📨 Event: {event_type}")
            
            # Print relevant data
            if hasattr(chunk, 'data') and chunk.data:
                if event_type == "messages":
                    print(f"     Message: {chunk.data}")
                elif event_type == "updates":
                    print(f"     Update: {json.dumps(chunk.data, indent=2)[:200]}...")
        
        print(f"\n✅ Stream completed. Received {len(events_received)} events")
        
        # Test 5: Get thread state
        print("\n📊 Getting final thread state...")
        state = await client.threads.get_state(thread_id)
        print(f"✅ Thread state retrieved")
        print(f"   Values keys: {list(state.get('values', {}).keys())}")
        
        # Test 6: Test threadless run (stateless)
        print("\n🔄 Testing threadless run...")
        async for chunk in client.runs.stream(
            None,  # No thread - stateless run
            config.assistant_id,
            input={
                "messages": [
                    {"role": "human", "content": "¿Qué batería recomiendas para un apartamento?"}
                ],
                "contact_id": config.test_contact_id
            },
            stream_mode="updates"
        ):
            if chunk.event == "updates":
                print(f"  Update: {json.dumps(chunk.data, indent=2)[:200]}...")
        
        print("\n✅ All SDK tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ SDK test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_with_sync_sdk(config: DeploymentTestConfig):
    """Test deployment using the synchronous SDK"""
    print("\n=== Testing with LangGraph SDK (Sync) ===\n")
    
    try:
        # Initialize sync client
        client = get_sync_client(url=config.deployment_url, api_key=config.api_key)
        print(f"✅ Connected to deployment (sync): {config.deployment_url}")
        
        # Quick test with sync client
        print("\n🔄 Running sync test...")
        thread = client.threads.create()
        
        for chunk in client.runs.stream(
            thread["thread_id"],
            config.assistant_id,
            input={
                "messages": [
                    {"role": "human", "content": "¿Cuánto dura una batería EcoFlow Delta 2?"}
                ],
                "contact_id": config.test_contact_id
            },
            stream_mode="updates"
        ):
            if chunk.event == "updates":
                print(f"  Sync update: {json.dumps(chunk.data, indent=2)[:100]}...")
        
        print("\n✅ Sync SDK test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Sync SDK test failed: {str(e)}")
        return False


async def test_with_rest_api(config: DeploymentTestConfig):
    """Test deployment using direct REST API calls"""
    print("\n=== Testing with REST API ===\n")
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": config.api_key
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test 1: Create thread
            print("🧵 Creating thread via REST...")
            response = await client.post(
                f"{config.deployment_url}/threads",
                headers=headers,
                json={}
            )
            response.raise_for_status()
            thread = response.json()
            thread_id = thread["thread_id"]
            print(f"✅ Created thread: {thread_id}")
            
            # Test 2: Stream run
            print("\n🚀 Streaming run via REST...")
            stream_url = f"{config.deployment_url}/threads/{thread_id}/runs/stream"
            
            async with client.stream(
                "POST",
                stream_url,
                headers=headers,
                json={
                    "assistant_id": config.assistant_id,
                    "input": {
                        "messages": [
                            {"role": "human", "content": "Necesito baterías para 6 horas de respaldo"}
                        ],
                        "contact_id": config.test_contact_id
                    },
                    "stream_mode": ["updates", "messages"]
                }
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("event:"):
                        event_type = line[7:].strip()
                        print(f"  📨 Event: {event_type}")
                    elif line.startswith("data:"):
                        data = line[6:].strip()
                        if data and data != "[DONE]":
                            try:
                                parsed_data = json.loads(data)
                                print(f"     Data: {json.dumps(parsed_data, indent=2)[:100]}...")
                            except:
                                print(f"     Raw: {data[:100]}...")
            
            print("\n✅ REST API test passed!")
            return True
            
    except Exception as e:
        print(f"\n❌ REST API test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_error_scenarios(config: DeploymentTestConfig):
    """Test error handling scenarios"""
    print("\n=== Testing Error Scenarios ===\n")
    
    if not HAS_SDK:
        print("⚠️  Skipping error tests (SDK not installed)")
        return False
    
    client = get_client(url=config.deployment_url, api_key=config.api_key)
    
    # Test 1: Invalid assistant
    print("🧪 Testing invalid assistant...")
    try:
        async for chunk in client.runs.stream(
            None,
            "invalid-assistant-id",
            input={"messages": [{"role": "human", "content": "test"}]},
            stream_mode="updates"
        ):
            pass
    except Exception as e:
        print(f"✅ Correctly caught error: {str(e)[:100]}...")
    
    # Test 2: Invalid input
    print("\n🧪 Testing invalid input...")
    try:
        async for chunk in client.runs.stream(
            None,
            config.assistant_id,
            input={"invalid_field": "test"},
            stream_mode="updates"
        ):
            pass
    except Exception as e:
        print(f"✅ Correctly caught error: {str(e)[:100]}...")
    
    return True


async def run_all_tests():
    """Run all deployment tests"""
    print("""
    =====================================
    LangGraph Cloud Deployment Test Suite
    =====================================
    """)
    
    # Get configuration from environment or use defaults
    deployment_url = os.getenv(
        "DEPLOYMENT_URL", 
        "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
    )
    api_key = os.getenv("LANGSMITH_API_KEY", "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")
    
    config = DeploymentTestConfig(
        deployment_url=deployment_url,
        api_key=api_key
    )
    
    print(f"🔧 Configuration:")
    print(f"   Deployment URL: {config.deployment_url}")
    print(f"   Assistant ID: {config.assistant_id}")
    print(f"   API Key: {config.api_key[:20]}...")
    
    # Run tests
    results = []
    
    if HAS_SDK:
        # SDK tests
        results.append(("Async SDK", await test_with_sdk(config)))
        results.append(("Sync SDK", test_with_sync_sdk(config)))
    else:
        print("\n⚠️  SDK tests skipped (install langgraph-sdk first)")
    
    # REST API tests (always available)
    results.append(("REST API", await test_with_rest_api(config)))
    
    # Error scenario tests
    if HAS_SDK:
        results.append(("Error Handling", await test_error_scenarios(config)))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! Your deployment is working correctly.")
        print("\n📝 Next steps:")
        print("1. Update environment variables in LangSmith UI if needed")
        print("2. Configure webhooks to point to your deployment")
        print("3. Monitor logs in LangSmith for production usage")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")


def main():
    """Main entry point"""
    # Check for SDK installation
    if not HAS_SDK:
        print("\n📦 Installing LangGraph SDK...")
        import subprocess
        subprocess.check_call(["pip", "install", "langgraph-sdk"])
        print("✅ SDK installed. Please run the script again.")
        return
    
    # Run async tests
    asyncio.run(run_all_tests())


if __name__ == "__main__":
    main()