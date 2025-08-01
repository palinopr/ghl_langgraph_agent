"""Run the app locally for testing"""
import uvicorn
from ghl_agent.custom_app import app

if __name__ == "__main__":
    print("Starting local server...")
    print("Webhook endpoint: http://localhost:8002/webhook/ghl")
    print("Health check: http://localhost:8002/health")
    print("\nPress Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)