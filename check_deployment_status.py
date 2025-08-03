#!/usr/bin/env python3
"""
Check LangGraph deployment status via LangSmith API
"""

import requests
import json
from datetime import datetime

LANGSMITH_API_KEY = "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"
DEPLOYMENT_ID = "03e9a719-ff0b-40bb-8e5c-548ff6ae0abf"

def check_langsmith_deployment():
    """Check deployment status via LangSmith API"""
    print("=== Checking LangSmith/LangGraph Deployment ===\n")
    
    # Common LangSmith API endpoints
    endpoints = [
        "https://api.smith.langchain.com/api/v1/deployments",
        f"https://api.smith.langchain.com/api/v1/deployments/{DEPLOYMENT_ID}",
        "https://api.langchain.com/v1/deployments",
        f"https://api.langchain.com/v1/deployments/{DEPLOYMENT_ID}",
    ]
    
    headers = {
        "X-API-Key": LANGSMITH_API_KEY,
        "Authorization": f"Bearer {LANGSMITH_API_KEY}",
        "Content-Type": "application/json"
    }
    
    for endpoint in endpoints:
        print(f"Trying: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)[:500]}...")
                return data
            elif response.status_code == 401:
                print("❌ Authentication failed - API key might be invalid")
            elif response.status_code == 404:
                print("❌ Not found - endpoint or deployment doesn't exist")
            else:
                print(f"Response: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print()
    
    return None

def check_deployment_instructions():
    """Print instructions for checking deployment"""
    print("\n=== Manual Deployment Check Instructions ===\n")
    print("1. Go to https://smith.langchain.com/")
    print("2. Sign in with your account")
    print("3. Navigate to 'Deployments' in the left sidebar")
    print(f"4. Look for deployment ID: {DEPLOYMENT_ID}")
    print("5. Check the deployment status and URL")
    print("\nThe deployment URL should be shown in the deployment details.")
    print("It might look like:")
    print("  - https://<deployment-name>-<hash>.langraph.app")
    print("  - https://api.langchain.com/deployments/<id>/invoke")
    print("  - A custom domain if configured")
    
def suggest_local_testing():
    """Suggest local testing approach"""
    print("\n=== Alternative: Test Locally ===\n")
    print("If the deployment isn't accessible, you can test locally:")
    print("\n1. Start the local server:")
    print("   cd /Users/jaimeortiz/N8N\\ WHAT/ghl_langgraph_agent")
    print("   python -m ghl_agent.main")
    print("\n2. Test with curl:")
    print("   curl -X POST http://localhost:8001/test/conversation \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"contact_id\": \"test-123\", \"message\": \"I need a website\"}'")
    print("\n3. Or use the local webhook endpoints:")
    print("   - POST http://localhost:8001/webhook/ghl")
    print("   - POST http://localhost:8001/webhook/meta")

def main():
    print(f"""
    ====================================
    LangGraph Deployment Status Check
    ====================================
    Deployment ID: {DEPLOYMENT_ID}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    ====================================
    """)
    
    # Check via API
    deployment_info = check_langsmith_deployment()
    
    if not deployment_info:
        print("\n❌ Could not retrieve deployment information via API")
        check_deployment_instructions()
        suggest_local_testing()
    else:
        print("\n✅ Deployment information retrieved!")
        print("Please check the response above for the deployment URL")

if __name__ == "__main__":
    main()