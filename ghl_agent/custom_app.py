"""Custom webhook app for LangGraph deployment"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import structlog
import os
from typing import Dict, Any

# Configure logging
logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="Battery Consultation Webhooks",
    description="Webhook endpoints for GHL integration",
    version="2.0.0"
)

# Check if we're in deployment or local mode
IS_DEPLOYMENT = os.getenv("LANGGRAPH_API_URL") is not None

# Import based on environment
if IS_DEPLOYMENT:
    try:
        from langgraph_sdk import get_client
        client = None
    except ImportError:
        logger.warning("LangGraph SDK not available in deployment")
        client = None
else:
    # For local testing, use the agent directly
    from ghl_agent.agent.graph import process_ghl_message
    client = "local"

@app.on_event("startup")
async def startup_event():
    """Initialize based on environment"""
    global client
    
    if IS_DEPLOYMENT and client is None:
        try:
            from langgraph_sdk import get_client
            # In deployment, connect to local API
            client = get_client(url="http://localhost:8123")
            logger.info("LangGraph client initialized for deployment")
        except Exception as e:
            logger.error(f"Failed to initialize LangGraph client: {e}")
            client = None
    else:
        logger.info("Running in local mode - using direct agent invocation")

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
        
        # Process based on environment
        if IS_DEPLOYMENT and client and client != "local":
            # Deployment mode - use SDK
            try:
                thread_id = f"ghl-{data['id']}"
                
                # Try to get existing thread
                try:
                    thread = await client.threads.get(thread_id)
                    logger.info(f"Found existing thread: {thread_id}")
                except:
                    # Create new thread if it doesn't exist
                    thread = await client.threads.create(
                        thread_id=thread_id,
                        metadata={
                            "contact_id": data["id"],
                            "contact_name": data.get("name"),
                            "contact_email": data.get("email"),
                            "contact_phone": data.get("phone")
                        }
                    )
                    logger.info(f"Created new thread: {thread_id}")
                
                # Create a run with the message
                run = await client.runs.create(
                    thread_id=thread_id,
                    assistant_id="ghl_agent",  # This must match the name in langgraph.json
                    input={
                        "messages": [{"role": "human", "content": data["message"]}],
                        "contact_id": data["id"],
                        "conversation_id": None,
                        "customer_name": data.get("name"),
                        "customer_phone": data.get("phone"),
                        "customer_email": data.get("email")
                    }
                )
                
                logger.info(f"Created run: {run['run_id']} for thread: {thread_id}")
                
                return JSONResponse(content={
                    "success": True,
                    "message": "Agent invoked successfully",
                    "contact_id": data["id"],
                    "thread_id": thread_id,
                    "run_id": run["run_id"],
                    "mode": "deployment"
                }, status_code=200)
                
            except Exception as e:
                logger.error(f"Error in deployment mode: {str(e)}")
                return JSONResponse(content={
                    "success": False,
                    "error": f"Failed to invoke agent: {str(e)}"
                }, status_code=500)
        
        else:
            # Local mode - use direct invocation
            try:
                response = await process_ghl_message(
                    contact_id=data["id"],
                    conversation_id=None,
                    message=data["message"]
                )
                
                logger.info(f"Agent response: {response[:100]}...")
                
                return JSONResponse(content={
                    "success": True,
                    "message": "Agent processed locally",
                    "contact_id": data["id"],
                    "response": response,
                    "mode": "local"
                }, status_code=200)
                
            except Exception as e:
                logger.error(f"Error in local mode: {str(e)}")
                return JSONResponse(content={
                    "success": False,
                    "error": f"Failed to process message: {str(e)}"
                }, status_code=500)
        
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
        "mode": "deployment" if IS_DEPLOYMENT else "local",
        "client_initialized": client is not None
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
        ],
        "mode": "deployment" if IS_DEPLOYMENT else "local"
    }

# Export the app
__all__ = ["app"]