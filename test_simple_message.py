#!/usr/bin/env python3
"""Test a simple message to see raw response"""

import httpx
import json
import asyncio

CLOUD_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
API_KEY = "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"
CONTACT_ID = "mVCISvZhpHehaDavn1ij"

async def test_simple():
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY
    }
    
    payload = {
        "assistant_id": "ghl_agent",
        "input": {
            "messages": [{"role": "human", "content": "Hola"}],
            "contact_id": CONTACT_ID
        },
        "stream_mode": "updates"
    }
    
    print("📤 Sending simple message: 'Hola'")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CLOUD_URL}/runs/stream",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"Status: {response.status_code}\n")
        
        # Parse each event
        for line in response.text.split('\n'):
            if line.startswith('data: '):
                try:
                    data = json.loads(line[6:])
                    print(f"\n🔵 Event: {line[:50]}...")
                    
                    if 'agent' in data and data['agent']:
                        agent_data = data['agent']
                        
                        # Show response content
                        if 'response' in agent_data:
                            print(f"   Response: '{agent_data['response']}'")
                        
                        # Show tool calls
                        if 'tool_calls' in agent_data and agent_data['tool_calls']:
                            for tc in agent_data['tool_calls']:
                                print(f"   Tool: {tc['name']}")
                                print(f"   Args: {json.dumps(tc['args'], ensure_ascii=False)}")
                        
                        # Show content if any
                        if 'content' in agent_data:
                            print(f"   Content: '{agent_data['content']}'")
                    
                    if 'tools' in data:
                        print(f"   Tools result: {data['tools']}")
                        
                except json.JSONDecodeError:
                    pass

if __name__ == "__main__":
    asyncio.run(test_simple())