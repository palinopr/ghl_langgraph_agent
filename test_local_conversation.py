#!/usr/bin/env python3
"""
Test the local GHL agent conversation flow
"""

import requests
import json
from datetime import datetime
import time

BASE_URL = "http://localhost:8002"

def test_webhook_conversation():
    """Test conversation through GHL webhook"""
    print("\n=== Testing GHL Webhook Conversation ===")
    
    contact_id = f"test-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    conversation_id = f"conv-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Test messages
    messages = [
        "Hello, I need help with a battery system",
        "I need it for my home solar system",
        "My budget is around $3000",
        "Actually, I can go up to $8000 if needed"
    ]
    
    for i, message in enumerate(messages):
        print(f"\n--- Message {i+1} ---")
        print(f"Sending: {message}")
        
        payload = {
            "type": "InboundMessage",
            "locationId": "test-location",
            "contactId": contact_id,
            "conversationId": conversation_id,
            "message": {
                "body": message,
                "direction": "inbound"
            }
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/webhook/ghl",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            else:
                print(f"Error: {response.text}")
                
            # Wait a bit between messages
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_direct_conversation():
    """Test direct conversation endpoint"""
    print("\n=== Testing Direct Conversation ===")
    
    contact_id = f"direct-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    try:
        response = requests.post(
            f"{BASE_URL}/test/conversation",
            json={
                "contact_id": contact_id,
                "message": "I'm interested in battery storage for my business"
            },
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def check_health():
    """Check server health"""
    print("\n=== Server Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print(f"""
    ====================================
    Local GHL Agent Test
    ====================================
    Server: {BASE_URL}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    """)
    
    # Check health first
    if not check_health():
        print("\n❌ Server is not healthy. Exiting.")
        return
    
    # Run tests
    test_webhook_conversation()
    test_direct_conversation()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()