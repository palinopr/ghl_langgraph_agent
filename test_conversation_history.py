#!/usr/bin/env python3
"""Test conversation history functionality"""

import asyncio
from langgraph_sdk import get_client
import json

async def test_conversation_history():
    """Test that the agent maintains conversation context"""
    
    # Your deployment configuration
    deployment_url = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
    api_key = "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"
    assistant_id = "ghl_agent"
    
    print("🧪 Testing Conversation History")
    print("=" * 50)
    
    client = get_client(url=deployment_url, api_key=api_key)
    
    # Create a thread
    thread = await client.threads.create()
    print(f"📌 Created thread: {thread['thread_id']}")
    
    # Test conversation flow
    messages = [
        "Hola, necesito un sistema de baterías",
        "Vivo en una casa",
        "Quiero energizar nevera, luces y abanicos"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📤 Message {i}: {message}")
        
        # Send message
        response = await client.runs.create(
            thread['thread_id'],
            assistant_id,
            input={
                "messages": [{"role": "human", "content": message}],
                "contact_id": "test-history-123",
                "conversation_id": "conv-history-123"
            }
        )
        
        # Wait for completion
        await client.runs.join(thread['thread_id'], response['run_id'])
        
        # Get the state to see the response
        state = await client.threads.get_state(thread['thread_id'])
        
        # Print the last assistant message
        if state['values'].get('messages'):
            last_message = state['values']['messages'][-1]
            print(f"📥 Response: {json.dumps(last_message, indent=2, ensure_ascii=False)}")
        
        # Check if agent is maintaining context
        print(f"🔍 Current state keys: {list(state['values'].keys())}")
        
        # Small delay between messages
        await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ Test complete - check if agent maintained context throughout conversation")

if __name__ == "__main__":
    asyncio.run(test_conversation_history())