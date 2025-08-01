"""Custom FastAPI app with webhook routes for LangGraph server"""
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
import json
import structlog
from typing import Dict, Any
import os

from ghl_agent.config import settings
from ghl_agent.webhooks.handlers import WebhookHandler, WebhookValidator
from ghl_agent.models import GHLWebhookPayload, MetaLeadWebhook

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="GHL Webhook Handler",
    description="Custom webhook routes for GHL and Meta integration",
    version="2.0.0"
)

# Initialize webhook handler
webhook_handler = WebhookHandler()

# Import the LangGraph client to interact with our graph
from langgraph_sdk import get_client

def get_langgraph_client():
    """Get LangGraph client for the local server"""
    # When running with langgraph dev, the server is available at localhost:8123
    # When deployed, this would use the appropriate URL
    base_url = os.getenv("LANGGRAPH_API_URL", "http://localhost:8123")
    return get_client(url=base_url)

@app.get("/webhook/meta")
async def verify_meta_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    """Meta webhook verification endpoint"""
    if hub_mode == "subscribe" and webhook_handler.verify_meta_webhook(hub_verify_token):
        logger.info("Meta webhook verified successfully")
        return int(hub_challenge)
    else:
        logger.warning("Meta webhook verification failed", 
                      mode=hub_mode, 
                      token_valid=webhook_handler.verify_meta_webhook(hub_verify_token))
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook/meta")
async def handle_meta_webhook(request: Request):
    """Handle Meta lead generation webhooks"""
    try:
        # Get raw body for signature verification
        body = await request.body()
        signature = request.headers.get("X-Hub-Signature-256", "")
        
        # Verify signature
        if not webhook_handler.verify_meta_signature(body, signature):
            logger.warning("Invalid Meta webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse and validate payload
        data = json.loads(body)
        webhook_data = WebhookValidator.validate_meta_webhook(data)
        
        logger.info("Processing Meta webhook", object_type=webhook_data.object)
        
        # Process each lead through LangGraph
        client = get_langgraph_client()
        leads_processed = []
        
        for entry in webhook_data.entry:
            for change in entry.get("changes", []):
                if change.get("field") == "leadgen":
                    lead_data = change.get("value", {})
                    lead_id = lead_data.get("leadgen_id")
                    
                    # Create thread for this lead
                    thread = await client.threads.create(
                        metadata={
                            "source": "meta_lead",
                            "lead_id": lead_id
                        }
                    )
                    
                    # Run the agent
                    response = await client.runs.create(
                        thread_id=thread["thread_id"],
                        assistant_id="ghl_agent",
                        input={
                            "messages": [{"role": "human", "content": "Hola, vi su anuncio sobre sistemas de baterías y me interesa."}],
                            "contact_id": f"meta-{lead_id}",
                            "conversation_id": None,
                            "housing_type": None,
                            "equipment_list": None,
                            "total_consumption": None,
                            "battery_recommendation": None,
                            "interested_in_consultation": None,
                            "customer_name": None,
                            "customer_phone": None,
                            "customer_email": None,
                            "metadata": {
                                "source": "meta_lead",
                                "lead_id": lead_id
                            }
                        }
                    )
                    
                    # Wait for completion
                    result = await client.runs.wait(thread_id=thread["thread_id"], run_id=response["run_id"])
                    
                    leads_processed.append({
                        "lead_id": lead_id,
                        "thread_id": thread["thread_id"],
                        "run_id": response["run_id"],
                        "status": result["status"]
                    })
        
        return JSONResponse(content={
            "success": True,
            "leads_processed": leads_processed
        }, status_code=200)
        
    except Exception as e:
        logger.error("Error processing Meta webhook", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/webhook/ghl")
async def handle_ghl_webhook(request: Request):
    """Handle GoHighLevel message webhooks"""
    try:
        # Parse request body
        data = await request.json()
        
        # Validate webhook data
        webhook_data = WebhookValidator.validate_ghl_webhook(data)
        
        logger.info("Processing GHL webhook", 
                   contact_id=webhook_data.id,
                   contact_name=webhook_data.name)
        
        # Skip if no message content
        if not webhook_data.message:
            return {"success": True, "action": "skipped", "reason": "no message content"}
        
        # Process through LangGraph
        client = get_langgraph_client()
        
        # Use contact_id as thread_id for conversation continuity
        thread_id = f"ghl-{webhook_data.id}"
        
        # Check if thread exists, create if not
        try:
            thread = await client.threads.get(thread_id)
        except:
            thread = await client.threads.create(
                thread_id=thread_id,
                metadata={
                    "source": "ghl",
                    "contact_id": webhook_data.id,
                    "contact_name": webhook_data.name,
                    "contact_email": webhook_data.email,
                    "contact_phone": webhook_data.phone
                }
            )
        
        # Run the agent
        response = await client.runs.create(
            thread_id=thread_id,
            assistant_id="ghl_agent",
            input={
                "messages": [{"role": "human", "content": webhook_data.message}],
                "contact_id": webhook_data.id,
                "conversation_id": None,
                "customer_name": webhook_data.name,
                "customer_phone": webhook_data.phone,
                "customer_email": webhook_data.email
            }
        )
        
        # Wait for completion
        result = await client.runs.wait(thread_id=thread_id, run_id=response["run_id"])
        
        return JSONResponse(content={
            "success": True,
            "thread_id": thread_id,
            "run_id": response["run_id"],
            "status": result["status"]
        }, status_code=200)
        
    except Exception as e:
        logger.error("Error processing GHL webhook", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/webhooks/health")
async def webhook_health():
    """Health check for webhook endpoints"""
    return {
        "status": "healthy",
        "webhooks": {
            "meta": "ready",
            "ghl": "ready"
        },
        "langgraph_api": os.getenv("LANGGRAPH_API_URL", "http://localhost:8123")
    }

@app.post("/test/ghl-webhook")
async def test_ghl_webhook():
    """Test endpoint that simulates your GHL webhook format"""
    test_payload = {
        "id": "test-contact-123",
        "name": "Juan Pérez",
        "email": "juan@example.com",
        "phone": "787-555-1234",
        "message": "Hola, vi su anuncio sobre sistemas de baterías"
    }
    
    # Process through the same handler
    return await handle_ghl_webhook(Request(scope={"type": "http"}, receive=lambda: {"body": json.dumps(test_payload).encode()}, send=lambda x: None))

# Export the app
__all__ = ["app"]