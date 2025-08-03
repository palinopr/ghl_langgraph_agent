#!/usr/bin/env python3
"""
Corrected test script for LangGraph Cloud deployment
Using the proper message format expected by the graph
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
    """Test basic conversation flow with correct message format"""
    print("\n" + "="*60)
    print("TEST 1: Basic Conversation (Battery Consultation)")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    # Correct input format based on the State definition
    test_input = {
        "messages": [
            {
                "role": "human",
                "content": "Hola, necesito ayuda con un sistema de baterías para mi hogar"
            }
        ],
        "contact_id": f"test-basic-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-basic-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
    
    print(f"Contact ID: {test_input['contact_id']}")
    print(f"Message: {test_input['messages'][0]['content']}")
    print("\nStreaming response...")
    
    try:
        response_count = 0
        last_messages = []
        
        async for chunk in client.runs.stream(
            None,  # Threadless run
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            response_count += 1
            print(f"\n📥 Event {response_count}: {chunk.event}")
            
            if hasattr(chunk, 'data') and chunk.data:
                if isinstance(chunk.data, dict):
                    # Check for messages in the response
                    if 'messages' in chunk.data:
                        last_messages = chunk.data['messages']
                        print(f"Messages updated: {len(last_messages)} total messages")
                        # Show the last AI message if available
                        for msg in last_messages:
                            if isinstance(msg, dict) and msg.get('type') == 'ai':
                                print(f"AI Response: {msg.get('content', '')[:200]}...")
                    
                    # Show other state updates
                    for key, value in chunk.data.items():
                        if key != 'messages' and value is not None:
                            print(f"{key}: {value}")
        
        print(f"\n✅ Test completed!")
        print(f"Total events: {response_count}")
        
        return response_count > 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def test_housing_type_flow():
    """Test the housing type conversation flow"""
    print("\n" + "="*60)
    print("TEST 2: Housing Type Flow (Casa vs Apartamento)")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    # Start with greeting and then specify housing type
    test_input = {
        "messages": [
            {
                "role": "human",
                "content": "Hola, necesito un sistema de baterías"
            },
            {
                "role": "ai",
                "content": "¡Hola! Me alegra poder ayudarte con tu sistema de baterías. Para ofrecerte la mejor solución, ¿vives en una casa o en un apartamento?"
            },
            {
                "role": "human",
                "content": "Vivo en una casa"
            }
        ],
        "contact_id": f"test-casa-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-casa-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "housing_type": "casa"
    }
    
    print(f"Testing housing type: casa")
    print("Last message: 'Vivo en una casa'")
    
    try:
        response_count = 0
        
        async for chunk in client.runs.stream(
            None,
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            response_count += 1
            
            if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                if 'housing_type' in chunk.data:
                    print(f"Housing type confirmed: {chunk.data['housing_type']}")
                
                if 'messages' in chunk.data:
                    for msg in chunk.data['messages']:
                        if isinstance(msg, dict) and msg.get('type') == 'ai':
                            print(f"AI Response: {msg.get('content', '')[:200]}...")
        
        print(f"\n✅ Housing type test completed!")
        return response_count > 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def test_equipment_list_flow():
    """Test equipment listing and calculation flow"""
    print("\n" + "="*60)
    print("TEST 3: Equipment List and Calculation")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    # Simulate a conversation that has progressed to equipment listing
    test_input = {
        "messages": [
            {
                "role": "human",
                "content": "Tengo una nevera, estufa eléctrica, 3 abanicos y un televisor"
            }
        ],
        "contact_id": f"test-equip-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-equip-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "housing_type": "casa",
        "equipment_list": ["nevera", "estufa eléctrica", "3 abanicos", "televisor"]
    }
    
    print("Testing equipment list calculation")
    print(f"Equipment: {test_input['equipment_list']}")
    
    try:
        response_count = 0
        battery_recommendation = None
        
        async for chunk in client.runs.stream(
            None,
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            response_count += 1
            
            if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                if 'total_consumption' in chunk.data:
                    print(f"Total consumption calculated: {chunk.data['total_consumption']} watts")
                
                if 'battery_recommendation' in chunk.data:
                    battery_recommendation = chunk.data['battery_recommendation']
                    print(f"Battery recommendation: {battery_recommendation}")
                
                if 'messages' in chunk.data:
                    for msg in chunk.data['messages']:
                        if isinstance(msg, dict) and msg.get('type') == 'ai':
                            content = msg.get('content', '')
                            if 'EG4' in content or 'Growatt' in content:
                                print(f"Product recommendation found: {content[:300]}...")
        
        print(f"\n✅ Equipment calculation test completed!")
        return response_count > 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def test_consultation_booking():
    """Test consultation booking flow"""
    print("\n" + "="*60)
    print("TEST 4: Consultation Booking")
    print("="*60)
    
    client = get_client(url=DEPLOYMENT_URL, api_key=LANGSMITH_API_KEY)
    
    # Simulate interest in consultation
    test_input = {
        "messages": [
            {
                "role": "human",
                "content": "Sí, me gustaría agendar una consulta. Mi nombre es Juan Pérez"
            }
        ],
        "contact_id": f"test-consult-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "conversation_id": f"conv-consult-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "interested_in_consultation": True,
        "customer_name": "Juan Pérez",
        "battery_recommendation": "EG4 LifePower 48V"
    }
    
    print("Testing consultation booking flow")
    print(f"Customer: {test_input['customer_name']}")
    
    try:
        response_count = 0
        
        async for chunk in client.runs.stream(
            None,
            ASSISTANT_ID,
            input=test_input,
            stream_mode="updates",
        ):
            response_count += 1
            
            if hasattr(chunk, 'data') and chunk.data and isinstance(chunk.data, dict):
                if 'customer_phone' in chunk.data:
                    print(f"Phone collected: {chunk.data['customer_phone']}")
                
                if 'customer_email' in chunk.data:
                    print(f"Email collected: {chunk.data['customer_email']}")
                
                # Check for tool calls (booking appointment)
                if 'tool_calls' in chunk.data:
                    for tool_call in chunk.data['tool_calls']:
                        print(f"Tool called: {tool_call}")
        
        print(f"\n✅ Consultation booking test completed!")
        return response_count > 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


async def main():
    print(f"""
    ====================================
    LangGraph Battery Consultation Test
    ====================================
    Deployment URL: {DEPLOYMENT_URL}
    Assistant ID: {ASSISTANT_ID}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Language: Spanish (PR market)
    ====================================
    """)
    
    # Run all tests
    tests = [
        ("Basic Conversation", test_basic_conversation),
        ("Housing Type Flow", test_housing_type_flow),
        ("Equipment Calculation", test_equipment_list_flow),
        ("Consultation Booking", test_consultation_booking)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🚀 Starting: {test_name}")
            success = await test_func()
            results.append((test_name, success))
            await asyncio.sleep(2)  # Pause between tests
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Show quick test commands
    print("\n" + "="*60)
    print("QUICK TEST COMMANDS")
    print("="*60)
    print("\nTest with curl:")
    print(f"""
curl -X POST {DEPLOYMENT_URL}/runs/stream \\
  -H 'Content-Type: application/json' \\
  -H 'X-Api-Key: {LANGSMITH_API_KEY}' \\
  -d '{{
    "assistant_id": "{ASSISTANT_ID}",
    "input": {{
      "messages": [
        {{"role": "human", "content": "Hola, necesito un sistema de baterías"}}
      ],
      "contact_id": "test-curl-123",
      "conversation_id": "conv-curl-123"
    }},
    "stream_mode": "updates"
  }}'
""")


if __name__ == "__main__":
    asyncio.run(main())