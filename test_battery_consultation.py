"""Test script for battery consultation flow"""
import asyncio
from ghl_agent.agent.graph import process_ghl_message
from ghl_agent.tools.battery_tools import calculate_battery_runtime, recommend_battery_system

async def test_battery_consultation():
    """Test the complete battery consultation flow"""
    print("🔋 Testing Battery Consultation Flow\n")
    
    # Test conversation flow
    conversations = [
        {
            "message": "Hola, necesito ayuda con un sistema de batería",
            "expected": "greeting"
        },
        {
            "message": "Vivo en un apartamento",
            "expected": "housing_type_response"
        },
        {
            "message": "Quiero energizar la nevera, dos abanicos, el TV y cargar celulares",
            "expected": "equipment_list_response"
        },
        {
            "message": "Sí, me interesa recibir orientación personalizada",
            "expected": "consultation_interest"
        },
        {
            "message": "Mi nombre es Juan Pérez, teléfono 787-555-1234, email juan@example.com",
            "expected": "contact_info_collected"
        }
    ]
    
    state = None
    contact_id = "test-battery-001"
    
    for conv in conversations:
        print(f"\n👤 Cliente: {conv['message']}")
        
        # Process message
        response = await process_ghl_message(
            contact_id=contact_id,
            conversation_id="test-conv-001",
            message=conv['message'],
            existing_state=state
        )
        
        print(f"🤖 Agente: {response}")
        
        # Simulate state updates (in real implementation, this would be handled by the graph)
        if not state:
            state = {
                "messages": [],
                "contact_id": contact_id,
                "conversation_id": "test-conv-001"
            }
    
    print("\n" + "="*60)
    print("📊 Testing Battery Calculation Tools\n")
    
    # Test battery runtime calculation
    equipment = ["nevera", "tv", "abanico", "abanico", "celulares"]
    battery_capacity = 2000  # 2000Wh battery
    
    result = await calculate_battery_runtime.ainvoke({
        "equipment_list": equipment,
        "battery_capacity_wh": battery_capacity
    })
    
    print(f"Equipment: {', '.join(equipment)}")
    print(f"Total consumption: {result['total_consumption_watts']}W")
    print(f"Battery capacity: {battery_capacity}Wh")
    print(f"Runtime: {result['runtime_detailed']}")
    
    print("\n" + "="*60)
    print("🔌 Testing Battery Recommendations\n")
    
    # Test battery recommendations
    recommendations = await recommend_battery_system.ainvoke({
        "housing_type": "apartamento",
        "total_consumption_watts": result['total_consumption_watts']
    })
    
    print(f"Housing type: Apartamento")
    print(f"Total consumption: {result['total_consumption_watts']}W")
    print(f"\nRecommended batteries:")
    
    for i, battery in enumerate(recommendations['recommendations'], 1):
        print(f"\n{i}. {battery['model']}")
        print(f"   Capacity: {battery['capacity_wh']}Wh")
        print(f"   Runtime: {battery['runtime_hours']} hours")
        print(f"   Price: {battery['price_range']}")
        print(f"   Features: {', '.join(battery['features'][:2])}")


if __name__ == "__main__":
    asyncio.run(test_battery_consultation())