"""Test simple agent without message history issues"""
import asyncio
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from ghl_agent.tools.ghl_tools import send_ghl_message

async def test_simple():
    print("Testing simple agent with tools...")
    
    # Simple prompt that forces tool use
    system_prompt = """Eres un asistente de baterías en Puerto Rico.
    
REGLA CRÍTICA: SIEMPRE usa la función send_ghl_message para enviar tu respuesta.
Contact ID: KTmWrFbAwVDVT0zMZAKb

Responde en español y mantén las respuestas cortas."""

    # Create model with tools
    model = ChatOpenAI(model="gpt-4-0125-preview", temperature=0.3)
    model_with_tools = model.bind_tools([send_ghl_message])
    
    # Test message
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Hola, necesito información sobre baterías")
    ]
    
    try:
        # Get response
        response = await model_with_tools.ainvoke(messages)
        print(f"\nModel response: {response}")
        
        # Check if model wants to use tools
        if response.tool_calls:
            print(f"\n✅ Model wants to use {len(response.tool_calls)} tool(s)")
            
            # Execute tool calls
            for tool_call in response.tool_calls:
                print(f"\nTool: {tool_call['name']}")
                print(f"Args: {tool_call['args']}")
                
                if tool_call['name'] == 'send_ghl_message':
                    result = await send_ghl_message.ainvoke(tool_call['args'])
                    print(f"Result: {result}")
        else:
            print("\n❌ Model did not use tools")
            print(f"Content: {response.content}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple())