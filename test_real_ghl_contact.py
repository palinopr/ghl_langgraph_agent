#!/usr/bin/env python3
"""Test with real GHL contact"""

import asyncio
from langgraph_sdk import get_client
import json
import httpx

# Real GHL contact from the URL
CONTACT_ID = "mVCISvZhpHehaDavn1ij"
LOCATION_ID = "EJ92ICNR9AmnbKq7Z2VQ"

# Deployment configuration
CLOUD_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
API_KEY = "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"
ASSISTANT_ID = "ghl_agent"

async def test_with_sdk():
    """Test using LangGraph SDK with real contact"""
    print("🧪 Testing with Real GHL Contact using SDK")
    print("=" * 60)
    print(f"Contact ID: {CONTACT_ID}")
    print(f"Location ID: {LOCATION_ID}")
    print("=" * 60)
    
    client = get_client(url=CLOUD_URL, api_key=API_KEY)
    
    # Create a thread for stateful conversation
    thread = await client.threads.create()
    print(f"\n📌 Created thread: {thread['thread_id']}")
    
    # Test messages
    messages = [
        "Hola, necesito información sobre sistemas de baterías para mi casa",
        "Vivo en una casa con 3 habitaciones",
        "Quiero energizar nevera, abanicos y luces durante apagones"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n{'='*60}")
        print(f"📤 Message {i}: {message}")
        
        try:
            # Send message
            response = await client.runs.create(
                thread['thread_id'],
                ASSISTANT_ID,
                input={
                    "messages": [{"role": "human", "content": message}],
                    "contact_id": CONTACT_ID,
                    "conversation_id": f"test-conversation-{thread['thread_id']}"
                }
            )
            
            print(f"🔄 Run ID: {response['run_id']}")
            
            # Wait for completion
            await client.runs.join(thread['thread_id'], response['run_id'])
            
            # Get the state
            state = await client.threads.get_state(thread['thread_id'])
            
            # Print state info
            print(f"\n📊 State after message {i}:")
            print(f"   Keys: {list(state['values'].keys())}")
            
            # Get tool calls if any
            if 'tool_calls' in state['values'] and state['values']['tool_calls']:
                print(f"\n🔧 Tool calls made:")
                for tc in state['values']['tool_calls']:
                    print(f"   - {tc['name']}: {json.dumps(tc['args'], ensure_ascii=False)[:100]}...")
            
            # Get response
            if 'messages' in state['values'] and state['values']['messages']:
                last_msg = state['values']['messages'][-1]
                if hasattr(last_msg, 'content'):
                    print(f"\n📥 Agent response: {last_msg.content}")
                elif isinstance(last_msg, dict) and 'content' in last_msg:
                    print(f"\n📥 Agent response: {last_msg['content']}")
            
            # Check if any errors
            if 'error' in state['values']:
                print(f"\n❌ Error: {state['values']['error']}")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Small delay between messages
        await asyncio.sleep(2)
    
    print(f"\n{'='*60}")
    print("✅ Test complete!")

async def test_with_rest():
    """Test using REST API with real contact"""
    print("\n🧪 Testing with Real GHL Contact using REST API")
    print("=" * 60)
    print(f"Contact ID: {CONTACT_ID}")
    print("=" * 60)
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY
    }
    
    payload = {
        "assistant_id": ASSISTANT_ID,
        "input": {
            "messages": [{"role": "human", "content": "Hola, necesito ayuda con baterías solares"}],
            "contact_id": CONTACT_ID,
            "conversation_id": "test-rest-conversation"
        },
        "stream_mode": "updates"
    }
    
    print(f"\n📤 Sending: {payload['input']['messages'][0]['content']}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{CLOUD_URL}/runs/stream",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                # Process stream
                events = []
                for line in response.text.split('\n'):
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            events.append(data)
                            print(f"\n📨 Event: {list(data.keys())}")
                            
                            # Check for tool calls
                            if 'agent' in data and data['agent'] and 'tool_calls' in data['agent']:
                                for tc in data['agent']['tool_calls']:
                                    print(f"   🔧 Tool: {tc['name']}")
                                    print(f"      Args: {json.dumps(tc['args'], ensure_ascii=False)[:100]}...")
                            
                            # Check for response
                            if 'agent' in data and data['agent'] and 'response' in data['agent']:
                                print(f"   📥 Response: {data['agent']['response']}")
                                
                        except json.JSONDecodeError:
                            pass
                
                print(f"\n✅ Received {len(events)} events total")
            else:
                print(f"❌ Error response: {response.text}")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

async def test_webhook_simulation():
    """Simulate a GHL webhook call"""
    print("\n🔗 Simulating GHL Webhook")
    print("=" * 60)
    
    webhook_data = {
        "type": "InboundMessage",
        "locationId": LOCATION_ID,
        "contactId": CONTACT_ID,
        "conversationId": "webhook-test-conversation",
        "message": {
            "body": "Hola, vi su anuncio sobre baterías solares"
        }
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Test against cloud webhook endpoint
            response = await client.post(
                f"{CLOUD_URL}/webhook/ghl",
                json=webhook_data,
                timeout=30
            )
            
            print(f"✅ Webhook Status: {response.status_code}")
            if response.status_code == 200:
                print(f"📊 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            else:
                print(f"❌ Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

async def main():
    """Run all tests with real contact"""
    print("""
    ====================================
    Testing with Real GHL Contact
    ====================================
    
    Contact: mVCISvZhpHehaDavn1ij
    Location: EJ92ICNR9AmnbKq7Z2VQ
    
    This will test:
    1. SDK conversation flow
    2. REST API calls
    3. Webhook simulation
    ====================================
    """)
    
    # Run tests
    await test_with_sdk()
    await test_with_rest()
    await test_webhook_simulation()
    
    print("\n✅ All tests completed!")
    print("\n📝 Notes:")
    print("- Check LangSmith for traces")
    print("- Check GHL contact for actual messages sent")
    print("- Monitor for any GHL API errors")

if __name__ == "__main__":
    asyncio.run(main())