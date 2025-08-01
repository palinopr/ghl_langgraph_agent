"""Test complete flow with tool invocation"""
import asyncio
from ghl_agent.agent.graph import graph
from langchain_core.messages import HumanMessage, SystemMessage
from ghl_agent.tools.ghl_tools import send_ghl_message

async def test_flow():
    print("Testing complete battery consultation flow...")
    print("=" * 50)
    
    # Test 1: Direct message send
    print("\n1. Testing direct WhatsApp send...")
    try:
        result = await send_ghl_message.ainvoke({
            "contact_id": "KTmWrFbAwVDVT0zMZAKb",
            "message": "🔋 Sistema de Baterías - Mensaje de prueba directo",
            "conversation_id": None
        })
        print(f"✅ Direct send result: {result}")
    except Exception as e:
        print(f"❌ Direct send error: {e}")
    
    # Test 2: Agent with forced tool use
    print("\n2. Testing agent flow...")
    state = {
        "messages": [HumanMessage(content="Hola, necesito información sobre baterías")],
        "contact_id": "KTmWrFbAwVDVT0zMZAKb",
        "conversation_id": None,
        "housing_type": None,
        "equipment_list": None,
        "total_consumption": None,
        "battery_recommendation": None,
        "interested_in_consultation": None,
        "customer_name": None,
        "customer_phone": None,
        "customer_email": None
    }
    
    try:
        # Run the agent
        result = await graph.ainvoke(state)
        
        # Check if agent sent message
        print("\n[Agent Results]")
        sent_message = False
        for msg in result["messages"]:
            print(f"- {type(msg).__name__}: {str(msg)[:100]}...")
            if hasattr(msg, "name") and msg.name == "send_ghl_message":
                sent_message = True
                
        if sent_message:
            print("✅ Agent used send_ghl_message tool")
        else:
            print("❌ Agent did NOT use send_ghl_message tool")
            
            # Force send the last AI message
            for msg in reversed(result["messages"]):
                if hasattr(msg, "content") and msg.content and not hasattr(msg, "tool_calls"):
                    print(f"\nForcing send of: {msg.content[:50]}...")
                    try:
                        force_result = await send_ghl_message.ainvoke({
                            "contact_id": "KTmWrFbAwVDVT0zMZAKb",
                            "message": msg.content,
                            "conversation_id": None
                        })
                        print(f"✅ Forced send result: {force_result}")
                    except Exception as e:
                        print(f"❌ Forced send error: {e}")
                    break
                    
    except Exception as e:
        print(f"❌ Agent error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    asyncio.run(test_flow())