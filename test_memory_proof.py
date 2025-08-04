#!/usr/bin/env python3
"""Prove the agent remembers previous conversation context"""

import asyncio
from langgraph_sdk import get_client
import json
from datetime import datetime

CLOUD_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
API_KEY = "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"
ASSISTANT_ID = "ghl_agent"
CONTACT_ID = "mVCISvZhpHehaDavn1ij"

async def test_memory():
    """Test if agent truly remembers context"""
    print("🧠 Testing Agent Memory/Context")
    print("=" * 60)
    
    client = get_client(url=CLOUD_URL, api_key=API_KEY)
    
    # Create TWO different threads to compare
    thread1 = await client.threads.create()
    thread2 = await client.threads.create()
    
    print(f"📌 Thread 1 (with context): {thread1['thread_id']}")
    print(f"📌 Thread 2 (no context): {thread2['thread_id']}")
    
    # THREAD 1: Build context step by step
    print("\n" + "="*60)
    print("THREAD 1: Building Context")
    print("="*60)
    
    # Message 1: Greeting
    print("\n1️⃣ Sending: 'Hola'")
    response1 = await client.runs.create(
        thread1['thread_id'],
        ASSISTANT_ID,
        input={
            "messages": [{"role": "human", "content": "Hola"}],
            "contact_id": CONTACT_ID
        }
    )
    await client.runs.join(thread1['thread_id'], response1['run_id'])
    state1 = await client.threads.get_state(thread1['thread_id'])
    
    # Extract agent's question
    for msg in reversed(state1['values']['messages']):
        if isinstance(msg, dict) and msg.get('type') == 'ai' and msg.get('tool_calls'):
            for tc in msg['tool_calls']:
                if tc['name'] == 'send_ghl_message':
                    print(f"   🤖 Agent asks: {tc['args']['message']}")
                    break
            break
    
    # Message 2: Answer house type
    print("\n2️⃣ Sending: 'Vivo en una casa'")
    response2 = await client.runs.create(
        thread1['thread_id'],
        ASSISTANT_ID,
        input={
            "messages": [{"role": "human", "content": "Vivo en una casa"}],
            "contact_id": CONTACT_ID
        }
    )
    await client.runs.join(thread1['thread_id'], response2['run_id'])
    state2 = await client.threads.get_state(thread1['thread_id'])
    
    # Extract agent's response
    for msg in reversed(state2['values']['messages']):
        if isinstance(msg, dict) and msg.get('type') == 'ai' and msg.get('tool_calls'):
            for tc in msg['tool_calls']:
                if tc['name'] == 'send_ghl_message':
                    print(f"   🤖 Agent responds: {tc['args']['message']}")
                    break
            break
    
    # Message 3: Test if agent remembers house type
    print("\n3️⃣ Sending: '¿Recuerdas dónde vivo?'")
    response3 = await client.runs.create(
        thread1['thread_id'],
        ASSISTANT_ID,
        input={
            "messages": [{"role": "human", "content": "¿Recuerdas dónde vivo?"}],
            "contact_id": CONTACT_ID
        }
    )
    await client.runs.join(thread1['thread_id'], response3['run_id'])
    state3 = await client.threads.get_state(thread1['thread_id'])
    
    # Extract agent's response
    thread1_response = None
    for msg in reversed(state3['values']['messages']):
        if isinstance(msg, dict) and msg.get('type') == 'ai' and msg.get('tool_calls'):
            for tc in msg['tool_calls']:
                if tc['name'] == 'send_ghl_message':
                    thread1_response = tc['args']['message']
                    print(f"   🤖 Agent answers: {thread1_response}")
                    break
            break
    
    # THREAD 2: Ask same question without context
    print("\n" + "="*60)
    print("THREAD 2: No Context")
    print("="*60)
    
    print("\n❓ Sending same question without context: '¿Recuerdas dónde vivo?'")
    response4 = await client.runs.create(
        thread2['thread_id'],
        ASSISTANT_ID,
        input={
            "messages": [{"role": "human", "content": "¿Recuerdas dónde vivo?"}],
            "contact_id": CONTACT_ID
        }
    )
    await client.runs.join(thread2['thread_id'], response4['run_id'])
    state4 = await client.threads.get_state(thread2['thread_id'])
    
    # Extract agent's response
    thread2_response = None
    for msg in reversed(state4['values']['messages']):
        if isinstance(msg, dict) and msg.get('type') == 'ai' and msg.get('tool_calls'):
            for tc in msg['tool_calls']:
                if tc['name'] == 'send_ghl_message':
                    thread2_response = tc['args']['message']
                    print(f"   🤖 Agent answers: {thread2_response}")
                    break
            break
    
    # ANALYSIS
    print("\n" + "="*60)
    print("🔍 MEMORY ANALYSIS")
    print("="*60)
    
    # Check state details
    print(f"\n📊 Thread 1 State:")
    print(f"   Total messages: {len(state3['values']['messages'])}")
    print(f"   Housing type in state: {state3['values'].get('housing_type', 'NOT SET')}")
    print(f"   Conversation stage: {state3['values'].get('conversation_stage', 'unknown')}")
    
    print(f"\n📊 Thread 2 State:")
    print(f"   Total messages: {len(state4['values']['messages'])}")
    print(f"   Housing type in state: {state4['values'].get('housing_type', 'NOT SET')}")
    print(f"   Conversation stage: {state4['values'].get('conversation_stage', 'unknown')}")
    
    # Compare responses
    print(f"\n🧪 RESULTS:")
    
    if thread1_response and thread2_response:
        if "casa" in thread1_response.lower() and "casa" not in thread2_response.lower():
            print("   ✅ MEMORY PROVEN: Thread 1 remembers 'casa', Thread 2 doesn't!")
        elif "casa" in thread1_response.lower():
            print("   ✅ Thread 1 mentions 'casa' in response")
        else:
            print("   ❓ Check responses manually to verify memory")
        
        print(f"\n   Thread 1 (with context): {thread1_response}")
        print(f"   Thread 2 (no context): {thread2_response}")
    
    # Additional test: Check message accumulation
    print(f"\n📚 Message History:")
    print(f"   Thread 1 has {len(state3['values']['messages'])} messages (built up over conversation)")
    print(f"   Thread 2 has {len(state4['values']['messages'])} messages (just one exchange)")
    
    if len(state3['values']['messages']) > len(state4['values']['messages']):
        print("   ✅ Thread 1 maintains full conversation history!")

if __name__ == "__main__":
    asyncio.run(test_memory())