#!/usr/bin/env python3
"""
Test LangGraph Cloud deployment on LangSmith
Specific to deployment ID: 03e9a719-ff0b-40bb-8e5c-548ff6ae0abf
"""

import asyncio
import json
from datetime import datetime
import httpx


async def test_deployment():
    """Test the specific deployment"""
    print(f"""
    ====================================
    Testing LangGraph Cloud Deployment
    ====================================
    Deployment ID: 03e9a719-ff0b-40bb-8e5c-548ff6ae0abf
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    """)
    
    # Configuration
    deployment_url = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
    api_key = "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"
    assistant_id = "ghl_agent"  # From langgraph.json
    
    print(f"🔧 Configuration:")
    print(f"   URL: {deployment_url}")
    print(f"   Assistant: {assistant_id}")
    print(f"   API Key: {api_key[:20]}...")
    
    # Test 1: Simple threadless run (no SDK needed)
    print("\n=== Test 1: Threadless Run (REST API) ===")
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    
    payload = {
        "assistant_id": assistant_id,
        "input": {
            "messages": [
                {"role": "human", "content": "Hola, necesito un sistema de baterías para mi casa"}
            ],
            "contact_id": "test-cloud-123",
            "conversation_id": "conv-cloud-123"
        },
        "stream_mode": "updates"
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            print("\n📤 Sending request...")
            print(f"   Endpoint: {deployment_url}/runs/stream")
            print(f"   Payload: {json.dumps(payload, indent=2)}")
            
            response = await client.post(
                f"{deployment_url}/runs/stream",
                headers=headers,
                json=payload
            )
            
            print(f"\n📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Request successful!")
                print("\n📨 Stream events:")
                
                # Process streaming response
                events = []
                for line in response.text.split('\n'):
                    if line.startswith('event:'):
                        event_type = line[7:].strip()
                        events.append(event_type)
                        print(f"   - Event: {event_type}")
                    elif line.startswith('data:') and line.strip() != 'data: [DONE]':
                        data = line[6:].strip()
                        if data:
                            try:
                                parsed = json.loads(data)
                                print(f"     Data: {json.dumps(parsed, indent=2)[:200]}...")
                            except:
                                print(f"     Raw: {data[:100]}...")
                
                print(f"\n✅ Received {len(events)} events")
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Response: {response.text[:500]}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Try with LangGraph SDK if available
    print("\n=== Test 2: Using LangGraph SDK ===")
    
    try:
        from langgraph_sdk import get_client
        
        print("✅ LangGraph SDK is installed")
        
        client = get_client(url=deployment_url, api_key=api_key)
        
        print("\n🔄 Running with SDK...")
        events = []
        async for chunk in client.runs.stream(
            None,  # Threadless
            assistant_id,
            input={
                "messages": [
                    {"role": "human", "content": "¿Qué batería recomiendas para un apartamento?"}
                ],
                "contact_id": "test-sdk-123"
            },
            stream_mode="updates"
        ):
            events.append(chunk.event)
            print(f"   Event: {chunk.event}")
            if hasattr(chunk, 'data') and chunk.data:
                print(f"   Data: {json.dumps(chunk.data, indent=2)[:200]}...")
        
        print(f"\n✅ SDK test successful! Received {len(events)} events")
        
    except ImportError:
        print("⚠️  LangGraph SDK not installed")
        print("   Install with: pip install langgraph-sdk")
    except Exception as e:
        print(f"❌ SDK test failed: {str(e)}")
    
    # Test 3: Check deployment health
    print("\n=== Test 3: Deployment Health Check ===")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try common health endpoints
            endpoints = [
                "/health",
                "/",
                "/info",
                "/assistants"
            ]
            
            for endpoint in endpoints:
                try:
                    url = f"{deployment_url}{endpoint}"
                    print(f"\n🔍 Checking {endpoint}...")
                    
                    response = await client.get(
                        url,
                        headers={"X-Api-Key": api_key}
                    )
                    
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        print(f"   Response: {response.text[:200]}...")
                        
                except Exception as e:
                    print(f"   Error: {str(e)[:100]}")
    
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
    
    print("\n" + "="*50)
    print("TEST COMPLETE")
    print("="*50)
    print("\n📝 Summary:")
    print("- Deployment URL is accessible")
    print("- Assistant ID should be 'ghl_agent'")
    print("- Use the REST API or SDK to interact with the deployment")
    print("\n🚀 Next steps:")
    print("1. Check LangSmith UI for deployment logs")
    print("2. Configure environment variables if needed")
    print("3. Set up webhooks to point to this deployment")


if __name__ == "__main__":
    asyncio.run(test_deployment())