"""Test sending real message to GHL contact"""
import asyncio
from ghl_agent.tools.ghl_tools import send_ghl_message

async def test_send():
    print("Testing direct message send to GHL...")
    print("Contact ID: KTmWrFbAwVDVT0zMZAKb")
    
    try:
        # Send test message directly using invoke
        result = await send_ghl_message.ainvoke({
            "contact_id": "KTmWrFbAwVDVT0zMZAKb",
            "message": "🔋 Prueba de sistema de baterías - ¡Hola! Este es un mensaje de prueba del agente de consulta de baterías.",
            "conversation_id": None
        })
        print(f"\nResult: {result}")
        
        # Send another message
        result2 = await send_ghl_message.ainvoke({
            "contact_id": "KTmWrFbAwVDVT0zMZAKb",
            "message": "¡Hola! ¿Vives en casa o apartamento? Estoy aquí para ayudarte a encontrar la solución de batería perfecta para tus necesidades.",
            "conversation_id": None
        })
        print(f"\nResult 2: {result2}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_send())