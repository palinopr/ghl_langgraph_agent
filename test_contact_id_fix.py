#!/usr/bin/env python3
"""Test that contact ID is properly passed to tools"""

import asyncio
import httpx
import json
from datetime import datetime

# Configuration
CLOUD_URL = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
LOCAL_URL = "http://localhost:2024"
API_KEY = "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"
REAL_CONTACT_ID = "mVCISvZhpHehaDavn1ij"

async def test_contact_id(name: str, url: str, use_api_key: bool = False):
    """Test that contact_id is properly passed to tools"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing {name}")
    print(f"   URL: {url}")
    print(f"   Contact ID: {REAL_CONTACT_ID}")
    print(f"{'='*60}")
    
    headers = {"Content-Type": "application/json"}
    if use_api_key:
        headers["X-Api-Key"] = API_KEY
    
    payload = {
        "assistant_id": "ghl_agent",
        "input": {
            "messages": [{"role": "human", "content": "Hola, necesito información sobre baterías"}],
            "contact_id": REAL_CONTACT_ID,
            "conversation_id": f"test-{name.lower()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        },
        "stream_mode": "updates"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{url}/runs/stream",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                # Look for send_ghl_message tool calls
                tool_calls_found = 0
                correct_contact_id = 0
                
                for line in response.text.split('\n'):
                    if line.startswith('data: ') and 'send_ghl_message' in line:
                        try:
                            data = json.loads(line[6:])
                            if 'agent' in data and data['agent'] and 'tool_calls' in data['agent']:
                                for tc in data['agent']['tool_calls']:
                                    if tc['name'] == 'send_ghl_message':
                                        tool_calls_found += 1
                                        actual_contact_id = tc['args'].get('contact_id', 'NOT_FOUND')
                                        
                                        print(f"\n🔧 Tool call #{tool_calls_found}:")
                                        print(f"   contact_id: {actual_contact_id}")
                                        print(f"   message: {tc['args'].get('message', '')[:50]}...")
                                        
                                        if actual_contact_id == REAL_CONTACT_ID:
                                            correct_contact_id += 1
                                            print(f"   ✅ Contact ID is CORRECT!")
                                        else:
                                            print(f"   ❌ Contact ID is WRONG (expected: {REAL_CONTACT_ID})")
                        except:
                            pass
                
                print(f"\n📊 Results:")
                print(f"   Total send_ghl_message calls: {tool_calls_found}")
                print(f"   Calls with correct contact_id: {correct_contact_id}")
                
                if tool_calls_found > 0:
                    success_rate = (correct_contact_id / tool_calls_found) * 100
                    print(f"   Success rate: {success_rate:.0f}%")
                    
                    if success_rate == 100:
                        print(f"\n✅ PASS: All tool calls used the correct contact ID!")
                        return True
                    else:
                        print(f"\n❌ FAIL: Some tool calls used incorrect contact ID")
                        return False
                else:
                    print(f"\n⚠️  No send_ghl_message tool calls found")
                    return False
            else:
                print(f"❌ Error response: {response.text[:200]}...")
                return False
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

async def main():
    """Run contact ID tests"""
    print("""
    ====================================
    Contact ID Fix Verification
    ====================================
    
    This test verifies that the contact_id
    is properly passed to tools, not as a
    literal string "contact_id"
    ====================================
    """)
    
    # Test local if available
    try:
        async with httpx.AsyncClient() as client:
            local_response = await client.get(f"{LOCAL_URL}/health", timeout=2)
            if local_response.status_code == 200:
                local_result = await test_contact_id("LOCAL", LOCAL_URL, False)
            else:
                print("\n⏭️  Skipping local test (server not running)")
                local_result = None
    except:
        print("\n⏭️  Skipping local test (server not running)")
        local_result = None
    
    # Test cloud
    cloud_result = await test_contact_id("CLOUD", CLOUD_URL, True)
    
    # Summary
    print(f"\n{'='*60}")
    print("📝 SUMMARY")
    print(f"{'='*60}")
    
    if local_result is not None:
        print(f"Local test: {'✅ PASSED' if local_result else '❌ FAILED'}")
    print(f"Cloud test: {'✅ PASSED' if cloud_result else '❌ FAILED'}")
    
    if cloud_result:
        print("\n🎉 The contact ID fix is working in production!")
    else:
        print("\n⏳ The fix may not be deployed yet. Wait for auto-deployment or trigger manually.")

if __name__ == "__main__":
    asyncio.run(main())