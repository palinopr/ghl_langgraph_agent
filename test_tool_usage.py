"""Test if agent uses send_ghl_message tool"""
import asyncio
from ghl_agent.agent.graph import graph

async def test_tool_usage():
    print("Testing if agent uses send_ghl_message tool...")
    print("=" * 50)
    
    # Test with real contact ID
    initial_state = {
        "messages": [],
        "contact_id": "KTmWrFbAwVDVT0zMZAKb",  # Real GHL contact
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
    
    # Add first message
    from langchain_core.messages import HumanMessage
    initial_state["messages"].append(HumanMessage(content="Hola, necesito información sobre baterías"))
    
    # Run the graph
    result = await graph.ainvoke(initial_state)
    
    # Check if agent used tools
    print("\n[Messages in result]")
    for i, msg in enumerate(result["messages"]):
        print(f"\n{i+1}. Type: {type(msg).__name__}")
        if hasattr(msg, "content"):
            print(f"   Content: {msg.content[:100]}...")
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"   Tool calls: {len(msg.tool_calls)} tools called")
            for tool_call in msg.tool_calls:
                print(f"   - Tool: {tool_call['name']}")
                print(f"     Args: {tool_call['args']}")
    
    print("\n" + "=" * 50)
    print("Test complete!")

if __name__ == "__main__":
    asyncio.run(test_tool_usage())