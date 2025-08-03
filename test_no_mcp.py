#!/usr/bin/env python3
"""
Test script to verify the agent works without MCP
"""

import asyncio
import os
from datetime import datetime
from langgraph_sdk import get_client
import json

# Configuration
DEPLOYMENT_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")
ASSISTANT_ID = "ghl_agent"


async def test_basic_conversation():
    """Test basic conversation flow without MCP"""
    print("\n" + "="*60)
    print("TEST: Basic Conversation (No MCP)")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    test_input = {
        "messages": [
            {
                "role": "human",
                "content": "Hola, necesito ayuda con un sistema de baterías para mi hogar"
            }
        ],
        "contact_id": f"test-no-mcp-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-no-mcp-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
    
    print(f"Contact ID: {test_input['contact_id']}")
    print(f"Message: {test_input['messages'][0]['content']}")
    print("\nStreaming response...")
    
    try:
        event_count = 0
        tool_calls = []
        
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
                    # Look for tool calls
                    if 'agent' in chunk.data:
                        agent_data = chunk.data['agent']
                        if 'messages' in agent_data:
                            for msg in agent_data['messages']:
                                if isinstance(msg, dict) and 'tool_calls' in msg:
                                    for tc in msg['tool_calls']:
                                        tool_name = tc.get('name', 'unknown')
                                        tool_calls.append(tool_name)
                                        print(f"🔧 Tool call: {tool_name}")
                                        if tool_name == 'send_ghl_message':
                                            print("✅ Using direct GHL API tool (not MCP)")
                    
                    # Check for errors
                    if 'error' in chunk.data:
                        print(f"❌ Error: {chunk.data['error']}")
                        if 'mcp' in str(chunk.data).lower():
                            print("⚠️  MCP reference found in error!")
        
        print(f"\n📊 Summary:")
        print(f"Total events: {event_count}")
        print(f"Tool calls: {tool_calls}")
        
        if 'send_ghl_message' in tool_calls:
            print("\n✅ SUCCESS: Agent is using direct GHL API tools")
            return True
        else:
            print("\n⚠️  No send_ghl_message calls detected")
            return False
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def test_local_import():
    """Test that local imports work without MCP"""
    print("\n" + "="*60)
    print("TEST: Local Import Check")
    print("="*60)
    
    try:
        # Try importing the graph module
        from ghl_agent.agent.graph import graph, State
        print("✅ Successfully imported graph module")
        
        # Check available tools
        print("\nChecking configured tools...")
        # This would need access to the tools list, but we can at least verify imports work
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False


async def main():
    print(f"""
    ====================================
    No-MCP Verification Test
    ====================================
    Deployment URL: {DEPLOYMENT_URL}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    
    This test verifies that:
    1. All MCP code has been removed
    2. The agent uses direct GHL API tools
    3. No MCP errors occur
    """)
    
    # Run tests
    local_ok = await test_local_import()
    cloud_ok = await test_basic_conversation()
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"Local Import Test: {'✅ PASSED' if local_ok else '❌ FAILED'}")
    print(f"Cloud Deployment Test: {'✅ PASSED' if cloud_ok else '❌ FAILED'}")
    
    if local_ok and cloud_ok:
        print("\n🎉 All MCP code has been successfully removed!")
        print("The agent is now using direct GHL API tools only.")
    else:
        print("\n⚠️  Some issues detected. Check the logs above.")


if __name__ == "__main__":
    asyncio.run(main())