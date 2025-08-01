"""Simple webhook test without SDK"""
import requests
import json

# Test webhook endpoint
url = "http://localhost:8002/webhook/ghl"

# Test data
test_data = {
    "id": "test-contact-123",
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "787-555-1234",
    "message": "Hola, necesito información sobre baterías"
}

print("Testing webhook endpoint...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_data, indent=2)}")

try:
    # First check if server is running
    health = requests.get("http://localhost:8002/health")
    print(f"\nHealth check: {health.json()}")
    
    # Send webhook
    response = requests.post(url, json=test_data)
    print(f"\nResponse status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
except requests.exceptions.ConnectionError:
    print("\nError: Server is not running!")
    print("Please run 'python3 run_local.py' first")
except Exception as e:
    print(f"\nError: {e}")