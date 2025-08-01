"""Test GHL API directly"""
import asyncio
import httpx
from ghl_agent.config import settings

async def test_ghl_api():
    print("Testing GHL API...")
    print(f"API Key: {settings.ghl_api_key[:10]}...")
    print(f"Location ID: {settings.ghl_location_id}")
    print(f"Contact ID: KTmWrFbAwVDVT0zMZAKb")
    
    headers = {
        "Authorization": f"Bearer {settings.ghl_api_key}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }
    
    # Test 1: Get contact info
    print("\n1. Testing GET contact info...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.ghl_api_base_url}/contacts/KTmWrFbAwVDVT0zMZAKb",
                headers=headers
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                contact = response.json()
                print(f"Contact Name: {contact.get('name', 'N/A')}")
                print(f"Contact Phone: {contact.get('phone', 'N/A')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 2: Send message
    print("\n2. Testing SEND message...")
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "type": "WhatsApp",
                "contactId": "KTmWrFbAwVDVT0zMZAKb",
                "message": "Prueba desde Python - Sistema de Baterías 🔋"
            }
            
            response = await client.post(
                f"{settings.ghl_api_base_url}/conversations/messages",
                headers=headers,
                json=payload
            )
            print(f"Status: {response.status_code}")
            if response.status_code in [200, 201]:
                print("Message sent successfully!")
                print(f"Response: {response.json()}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ghl_api())