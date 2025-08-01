"""Custom webhook app for LangGraph deployment"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import structlog
import os
from typing import Dict, Any
import httpx
import asyncio

# Configure logging
logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="Battery Consultation Webhooks",
    description="Webhook endpoints for GHL integration",
    version="2.0.0"
)

# Get the LangGraph API URL - in deployment this is available locally
LANGGRAPH_API_URL = os.getenv("LANGGRAPH_API_URL", "http://localhost:8123")

async def invoke_agent(contact_id: str, message: str, contact_info: Dict[str, Any]) -> Dict[str, Any]:
    """Invoke the LangGraph agent with the message"""
    try:
        # In LangGraph Cloud, we use the local API to create runs
        async with httpx.AsyncClient() as client:
            # Create a thread for this conversation
            thread_response = await client.post(
                f"{LANGGRAPH_API_URL}/threads",
                json={
                    "metadata": {
                        "contact_id": contact_id,
                        "contact_name": contact_info.get("name"),
                        "contact_email": contact_info.get("email"),
                        "contact_phone": contact_info.get("phone")
                    }
                }
            )
            thread = thread_response.json()
            thread_id = thread["thread_id"]
            
            # Create a run with the message
            run_response = await client.post(
                f"{LANGGRAPH_API_URL}/threads/{thread_id}/runs",
                json={
                    "assistant_id": "ghl_agent",
                    "input": {
                        "messages": [{"role": "human", "content": message}],
                        "contact_id": contact_id,
                        "conversation_id": None,
                        "customer_name": contact_info.get("name"),
                        "customer_phone": contact_info.get("phone"),
                        "customer_email": contact_info.get("email")
                    }
                }
            )
            run = run_response.json()
            
            # Wait for completion (with timeout)
            for _ in range(30):  # 30 seconds timeout
                await asyncio.sleep(1)
                status_response = await client.get(
                    f"{LANGGRAPH_API_URL}/threads/{thread_id}/runs/{run['run_id']}"
                )
                status = status_response.json()
                if status["status"] in ["success", "error"]:
                    return {
                        "thread_id": thread_id,
                        "run_id": run["run_id"],
                        "status": status["status"]
                    }
            
            return {
                "thread_id": thread_id,
                "run_id": run["run_id"],
                "status": "timeout"
            }
            
    except Exception as e:
        logger.error(f"Error invoking agent: {str(e)}")
        return {"error": str(e)}

@app.post("/webhook/ghl")
async def handle_ghl_webhook(request: Request):
    """Handle GoHighLevel webhook and invoke agent"""
    try:
        data = await request.json()
        
        # Log the webhook receipt
        logger.info("GHL webhook received", 
                   contact_id=data.get("id"),
                   has_message=bool(data.get("message")))
        
        # Basic validation
        if not data.get("id") or not data.get("message"):
            return {"success": False, "error": "Missing required fields"}
        
        # Extract contact info
        contact_info = {
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone")
        }
        
        # Invoke the agent
        result = await invoke_agent(
            contact_id=data["id"],
            message=data["message"],
            contact_info=contact_info
        )
        
        # Return success with agent invocation details
        return JSONResponse(content={
            "success": True,
            "message": "Agent invoked",
            "contact_id": data.get("id"),
            "agent_result": result
        }, status_code=200)
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "battery-consultation",
        "webhooks": "ready",
        "langgraph_api": LANGGRAPH_API_URL
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Battery Consultation Agent",
        "version": "2.0.0",
        "endpoints": [
            "/webhook/ghl",
            "/health"
        ]
    }

# Export the app
__all__ = ["app"]