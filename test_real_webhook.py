"""Test webhook with real contact ID"""
import requests
import json

# Test with real contact
url = "http://localhost:8002/webhook/ghl"
payload = {
    "id": "KTmWrFbAwVDVT0zMZAKb",
    "name": "Test Customer",
    "email": "test@example.com", 
    "phone": "787-555-1234",
    "message": "Hola, necesito ayuda con baterías para mi casa"
}

print("Testing webhook with real contact ID...")
print(f"Contact ID: {payload['id']}")
print(f"Message: {payload['message']}")

try:
    response = requests.post(url, json=payload)
    print(f"\nStatus: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if result.get("success"):
        print("\n✅ Success! The agent processed the message.")
        print(f"Agent response: {result.get('response', 'No response')}")
    else:
        print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")