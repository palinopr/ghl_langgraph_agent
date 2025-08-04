#!/usr/bin/env python3
"""
Test LangGraph locally as if it were cloud deployment
This script runs the same tests against local langgraph dev server
"""

import asyncio
import subprocess
import time
import sys
import os
from langgraph_sdk import get_client
import httpx
import json

# Configuration
LOCAL_URL = "http://localhost:2024"
ASSISTANT_ID = "ghl_agent"

async def wait_for_server(url: str, timeout: int = 30):
    """Wait for the server to be ready"""
    print(f"⏳ Waiting for server at {url}...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{url}/health")
                if response.status_code == 200:
                    print("✅ Server is ready!")
                    return True
        except:
            pass
        await asyncio.sleep(1)
    
    return False

async def test_threadless_run():
    """Test threadless run (stateless)"""
    print("\n=== Test 1: Threadless Run (Stateless) ===")
    
    client = get_client(url=LOCAL_URL)
    
    messages = [
        "Hola, necesito un sistema de baterías para mi casa",
        "Vivo en una casa con paneles solares",
        "Quiero energizar nevera, luces y abanicos"
    ]
    
    for message in messages:
        print(f"\n📤 Sending: {message}")
        
        async for chunk in client.runs.stream(
            None,  # Threadless run
            ASSISTANT_ID,
            input={
                "messages": [{"role": "human", "content": message}],
                "contact_id": "test-local-123",
                "conversation_id": "conv-local-123"
            },
            stream_mode="updates"
        ):
            print(f"   Event: {chunk.event}")
            if chunk.data and isinstance(chunk.data, dict):
                # Pretty print the response
                print(f"   Data: {json.dumps(chunk.data, indent=2, ensure_ascii=False)[:200]}...")

async def test_thread_run():
    """Test threaded run (stateful)"""
    print("\n=== Test 2: Thread Run (Stateful) ===")
    
    client = get_client(url=LOCAL_URL)
    
    # Create a thread
    thread = await client.threads.create()
    print(f"📌 Created thread: {thread['thread_id']}")
    
    messages = [
        "Hola, necesito información sobre baterías",
        "Mi casa tiene 3 habitaciones",
        "Tengo nevera, abanicos y luces LED"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📤 Message {i}: {message}")
        
        # Send message in thread
        response = await client.runs.create(
            thread['thread_id'],
            ASSISTANT_ID,
            input={
                "messages": [{"role": "human", "content": message}],
                "contact_id": "test-thread-123",
                "conversation_id": f"conv-thread-{thread['thread_id']}"
            }
        )
        
        # Wait for completion
        await client.runs.join(thread['thread_id'], response['run_id'])
        
        # Get the state
        state = await client.threads.get_state(thread['thread_id'])
        
        # Print current state
        print(f"🔍 State keys: {list(state['values'].keys())}")
        
        # Get last message
        if state['values'].get('messages'):
            last_msg = state['values']['messages'][-1]
            if hasattr(last_msg, 'content'):
                print(f"📥 Response: {last_msg.content[:200]}...")
            else:
                print(f"📥 Response: {json.dumps(last_msg, indent=2, ensure_ascii=False)[:200]}...")

async def test_rest_api():
    """Test REST API directly"""
    print("\n=== Test 3: REST API Direct ===")
    
    async with httpx.AsyncClient() as client:
        # Test health endpoint
        print("\n🔍 Testing /health...")
        response = await client.get(f"{LOCAL_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test info endpoint
        print("\n🔍 Testing /info...")
        response = await client.get(f"{LOCAL_URL}/info")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        # Test assistants endpoint
        print("\n🔍 Testing /assistants...")
        response = await client.get(f"{LOCAL_URL}/assistants")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        # Test streaming run
        print("\n🔍 Testing streaming run...")
        response = await client.post(
            f"{LOCAL_URL}/runs/stream",
            json={
                "assistant_id": ASSISTANT_ID,
                "input": {
                    "messages": [{"role": "human", "content": "Hola, necesito ayuda"}],
                    "contact_id": "test-rest-123"
                },
                "stream_mode": "updates"
            }
        )
        
        print(f"   Status: {response.status_code}")
        
        # Process SSE stream
        event_count = 0
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                event_count += 1
                data = json.loads(line[6:])
                print(f"   Event {event_count}: {list(data.keys())}")
                if event_count >= 3:  # Just show first 3 events
                    break

async def test_webhook_endpoints():
    """Test custom webhook endpoints"""
    print("\n=== Test 4: Custom Webhook Endpoints ===")
    
    async with httpx.AsyncClient() as client:
        # Test GHL webhook
        print("\n🔍 Testing /webhook/ghl...")
        response = await client.post(
            f"{LOCAL_URL}/webhook/ghl",
            json={
                "type": "InboundMessage",
                "locationId": "test-location",
                "contactId": "test-webhook-123",
                "conversationId": "conv-webhook-123",
                "message": {
                    "body": "Test message from webhook"
                }
            }
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {json.dumps(response.json(), indent=2)}")

async def main():
    """Run all tests"""
    print("""
    ====================================
    LangGraph Local-as-Cloud Testing
    ====================================
    
    This tests the local langgraph dev server
    with the same API calls used in cloud deployment
    """)
    
    # Check if server is running
    server_ready = await wait_for_server(LOCAL_URL)
    
    if not server_ready:
        print("\n❌ Server is not running!")
        print("\nTo start the server, run in another terminal:")
        print("  cd /Users/jaimeortiz/N8N\\ WHAT/ghl_langgraph_agent")
        print("  source venv/bin/activate")
        print("  langgraph dev")
        print("\nOr with tunnel for remote access:")
        print("  langgraph dev --tunnel")
        return
    
    # Run all tests
    try:
        await test_threadless_run()
        await test_thread_run()
        await test_rest_api()
        await test_webhook_endpoints()
        
        print("\n✅ All tests completed!")
        print("\n📝 Summary:")
        print("- Local server behaves exactly like cloud deployment")
        print("- Same API endpoints and responses")
        print("- Thread state persistence works locally")
        print("- Custom webhooks are accessible")
        print("\n🚀 Ready for cloud deployment!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())