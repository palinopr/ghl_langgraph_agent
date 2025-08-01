"""Test full conversation through webhook"""
import requests
import json
import time

base_url = "http://localhost:8002/webhook/ghl"
contact_id = "test-contact-456"

# Conversation flow
messages = [
    "Hola, necesito información sobre baterías",
    "Vivo en un apartamento",
    "Necesito energizar la nevera, dos abanicos y el televisor",
    "Sí, me interesa una consulta personalizada",
    "Mi nombre es María González, teléfono 787-555-9876, email maria@example.com"
]

print("Testing Battery Consultation Conversation Flow")
print("=" * 50)

for i, message in enumerate(messages, 1):
    print(f"\n[Message {i}]")
    print(f"Customer: {message}")
    
    # Send webhook
    payload = {
        "id": contact_id,
        "name": "María González" if i > 3 else None,
        "email": "maria@example.com" if i > 3 else None,
        "phone": "787-555-9876" if i > 3 else None,
        "message": message
    }
    
    try:
        response = requests.post(base_url, json=payload)
        result = response.json()
        
        if result.get("success"):
            agent_response = result.get("response", "No response")
            print(f"Agent: {agent_response}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Wait between messages
    time.sleep(1)

print("\n" + "=" * 50)
print("Conversation test complete!")
print("\nNote: Since we're not maintaining state between webhook calls,")
print("each message is treated as a new conversation.")
print("In production with LangGraph, the state would be maintained.")