#!/usr/bin/env python3
"""Debug conversation context issues"""

import asyncio
from langgraph_sdk import get_client
import json

# Configuration
CLOUD_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
API_KEY = "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"
ASSISTANT_ID = "ghl_agent"
CONTACT_ID = "mVCISvZhpHehaDavn1ij"

async def debug_context():
    """Debug why context is not maintained"""
    print("🔍 Debugging Context Issues")
    print("=" * 60)
    
    client = get_client(url=CLOUD_URL, api_key=API_KEY)
    
    # Create a thread
    thread = await client.threads.create()
    print(f"📌 Thread ID: {thread['thread_id']}")
    
    # First message
    print("\n1️⃣ First Message: 'Hola, necesito baterías'")
    
    response1 = await client.runs.create(
        thread['thread_id'],
        ASSISTANT_ID,
        input={
            "messages": [{"role": "human", "content": "Hola, necesito baterías"}],
            "contact_id": CONTACT_ID,
            "conversation_id": f"debug-{thread['thread_id']}"
        }
    )
    
    await client.runs.join(thread['thread_id'], response1['run_id'])
    state1 = await client.threads.get_state(thread['thread_id'])
    
    print("\n📊 State after message 1:")
    print(f"   Messages count: {len(state1['values'].get('messages', []))}")
    
    # Print all messages
    for i, msg in enumerate(state1['values'].get('messages', [])):
        if isinstance(msg, dict):
            print(f"\n   Message {i+1}:")
            print(f"      Type: {msg.get('type', 'unknown')}")
            print(f"      Content: {msg.get('content', '')[:100]}...")
            if msg.get('tool_calls'):
                print(f"      Tool calls: {len(msg['tool_calls'])}")
        else:
            print(f"\n   Message {i+1}: {str(msg)[:100]}...")
    
    # Second message
    print("\n\n2️⃣ Second Message: 'Vivo en una casa'")
    
    response2 = await client.runs.create(
        thread['thread_id'],
        ASSISTANT_ID,
        input={
            "messages": [{"role": "human", "content": "Vivo en una casa"}],
            "contact_id": CONTACT_ID,
            "conversation_id": f"debug-{thread['thread_id']}"
        }
    )
    
    await client.runs.join(thread['thread_id'], response2['run_id'])
    state2 = await client.threads.get_state(thread['thread_id'])
    
    print("\n📊 State after message 2:")
    print(f"   Messages count: {len(state2['values'].get('messages', []))}")
    print(f"   Housing type: {state2['values'].get('housing_type', 'NOT SET')}")
    print(f"   Conversation stage: {state2['values'].get('conversation_stage', 'NOT SET')}")
    
    # Check if messages are accumulating
    if len(state2['values'].get('messages', [])) > len(state1['values'].get('messages', [])):
        print("   ✅ Messages are accumulating (context maintained)")
    else:
        print("   ❌ Messages NOT accumulating (context lost)")
    
    # Print last AI message
    messages = state2['values'].get('messages', [])
    for msg in reversed(messages):
        if isinstance(msg, dict) and msg.get('type') == 'ai':
            print(f"\n   Last AI response: {msg.get('content', 'EMPTY')[:200]}...")
            break
    
    # Check store
    print(f"\n   Store content: {state2['values'].get('store', {})}")

if __name__ == "__main__":
    asyncio.run(debug_context())