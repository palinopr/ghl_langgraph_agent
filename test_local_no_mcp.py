#!/usr/bin/env python3
"""
Test the agent locally without MCP
"""

import asyncio
from ghl_agent.agent.graph import process_ghl_message

async def test_local():
    """Test local agent without MCP"""
    print("Testing local agent (no MCP)...")
    
    try:
        response = await process_ghl_message(
            contact_id="test-local-123",
            conversation_id="conv-local-123",
            message="Hola, necesito ayuda con baterías"
        )
        
        print(f"✅ Success! Response: {response[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'mcp' in str(e).lower():
            print("⚠️  MCP reference found in error!")
        return False

if __name__ == "__main__":
    asyncio.run(test_local())