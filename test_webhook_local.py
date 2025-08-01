"""Test webhook locally"""
import asyncio
import httpx

async def test_webhook():
    """Test the webhook endpoint locally"""
    # Test data matching GHL format
    test_payload = {
        "id": "test-contact-123",
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "phone": "787-555-1234",
        "message": "Hola, necesito información sobre baterías para mi casa"
    }
    
    # Test local webhook
    async with httpx.AsyncClient() as client:
        try:
            # First check health
            health = await client.get("http://localhost:8002/health")
            print(f"Health check: {health.json()}")
            
            # Then test webhook
            response = await client.post(
                "http://localhost:8002/webhook/ghl",
                json=test_payload
            )
            print(f"\nWebhook response status: {response.status_code}")
            print(f"Webhook response: {response.json()}")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure the server is running locally!")

if __name__ == "__main__":
    asyncio.run(test_webhook())