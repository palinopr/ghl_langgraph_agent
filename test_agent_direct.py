"""Test the agent directly without webhooks"""
import asyncio
from ghl_agent.agent.graph import process_ghl_message

async def test_agent():
    """Test the agent with different messages"""
    test_cases = [
        {
            "contact_id": "test-123",
            "message": "Hola, necesito información sobre baterías"
        },
        {
            "contact_id": "test-123", 
            "message": "Vivo en un apartamento"
        },
        {
            "contact_id": "test-123",
            "message": "Necesito la nevera y dos abanicos"
        }
    ]
    
    print("Testing Battery Consultation Agent\n" + "="*40)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Contact: {test['contact_id']}")
        print(f"Message: {test['message']}")
        
        try:
            response = await process_ghl_message(
                contact_id=test['contact_id'],
                conversation_id=None,
                message=test['message']
            )
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_agent())