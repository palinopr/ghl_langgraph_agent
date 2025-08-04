#!/usr/bin/env python3
"""Test state extraction functionality"""

import asyncio
from langgraph_sdk import get_client
import json

# Configuration
LOCAL_URL = "http://localhost:2024"
CLOUD_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
API_KEY = "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"
CONTACT_ID = "mVCISvZhpHehaDavn1ij"

async def test_state_extraction(url: str, use_api_key: bool = False):
    """Test if state extraction is working"""
    print(f"🧪 Testing State Extraction")
    print(f"   URL: {url}")
    print("=" * 60)
    
    client_config = {"url": url}
    if use_api_key:
        client_config["api_key"] = API_KEY
        
    client = get_client(**client_config)
    
    # Create a thread
    thread = await client.threads.create()
    print(f"📌 Thread: {thread['thread_id']}\n")
    
    # Test 1: Send housing type
    print("1️⃣ Sending: 'Hola, vivo en una casa'")
    response1 = await client.runs.create(
        thread['thread_id'],
        "ghl_agent",
        input={
            "messages": [{"role": "human", "content": "Hola, vivo en una casa"}],
            "contact_id": CONTACT_ID
        }
    )
    await client.runs.join(thread['thread_id'], response1['run_id'])
    state1 = await client.threads.get_state(thread['thread_id'])
    
    print("\n📊 State after message 1:")
    print(f"   housing_type: {state1['values'].get('housing_type', 'NOT SET')}")
    
    # Check tool calls
    for msg in reversed(state1['values']['messages']):
        if isinstance(msg, dict) and msg.get('type') == 'ai' and msg.get('tool_calls'):
            for tc in msg['tool_calls']:
                if tc['name'] == 'update_conversation_state':
                    print(f"   ✅ Called update_conversation_state with: {tc['args']}")
                elif tc['name'] == 'send_ghl_message':
                    print(f"   📱 Sent message: {tc['args']['message'][:100]}...")
            break
    
    # Test 2: Send equipment list
    print("\n2️⃣ Sending: 'Quiero energizar nevera, dos abanicos y luces'")
    response2 = await client.runs.create(
        thread['thread_id'],
        "ghl_agent",
        input={
            "messages": [{"role": "human", "content": "Quiero energizar nevera, dos abanicos y luces"}],
            "contact_id": CONTACT_ID
        }
    )
    await client.runs.join(thread['thread_id'], response2['run_id'])
    state2 = await client.threads.get_state(thread['thread_id'])
    
    print("\n📊 State after message 2:")
    print(f"   housing_type: {state2['values'].get('housing_type', 'NOT SET')}")
    print(f"   equipment_list: {state2['values'].get('equipment_list', 'NOT SET')}")
    
    # Check tool calls
    for msg in reversed(state2['values']['messages']):
        if isinstance(msg, dict) and msg.get('type') == 'ai' and msg.get('tool_calls'):
            for tc in msg['tool_calls']:
                if tc['name'] == 'update_conversation_state':
                    print(f"   ✅ Called update_conversation_state with: {tc['args']}")
            break
    
    # Test 3: Ask if agent remembers
    print("\n3️⃣ Sending: '¿Qué tipo de vivienda tengo?'")
    response3 = await client.runs.create(
        thread['thread_id'],
        "ghl_agent",
        input={
            "messages": [{"role": "human", "content": "¿Qué tipo de vivienda tengo?"}],
            "contact_id": CONTACT_ID
        }
    )
    await client.runs.join(thread['thread_id'], response3['run_id'])
    state3 = await client.threads.get_state(thread['thread_id'])
    
    print("\n📊 Final State:")
    print(f"   housing_type: {state3['values'].get('housing_type', 'NOT SET')}")
    print(f"   equipment_list: {state3['values'].get('equipment_list', 'NOT SET')}")
    print(f"   conversation_stage: {state3['values'].get('conversation_stage', 'unknown')}")
    
    # Get agent's response
    for msg in reversed(state3['values']['messages']):
        if isinstance(msg, dict) and msg.get('type') == 'ai' and msg.get('tool_calls'):
            for tc in msg['tool_calls']:
                if tc['name'] == 'send_ghl_message':
                    print(f"\n🤖 Agent responds: {tc['args']['message']}")
                    break
            break
    
    # Analysis
    print("\n" + "="*60)
    print("🔍 ANALYSIS:")
    if state3['values'].get('housing_type') == 'casa':
        print("   ✅ State extraction WORKING! Agent saved housing_type = 'casa'")
    else:
        print("   ❌ State extraction NOT working - housing_type not saved")
        
    if state3['values'].get('equipment_list'):
        print(f"   ✅ Equipment list saved: {state3['values']['equipment_list']}")
    else:
        print("   ❌ Equipment list not saved")

async def main():
    # Test local if available
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LOCAL_URL}/health", timeout=2)
            if response.status_code == 200:
                print("\n🏠 LOCAL TEST")
                print("="*60)
                await test_state_extraction(LOCAL_URL, False)
    except:
        print("⏭️  Skipping local test (server not running)")
    
    # Test cloud
    print("\n\n☁️  CLOUD TEST")
    print("="*60)
    await test_state_extraction(CLOUD_URL, True)

if __name__ == "__main__":
    asyncio.run(main())