import uvicorn
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
import structlog
import json

from .config import settings, validate_config
from .webhooks.handlers import WebhookHandler, WebhookValidator
from .agent.graph import process_ghl_message

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

# Validate configuration at startup
if not validate_config():
    logger.error("Configuration validation failed. Exiting.")
    exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="GHL LangGraph Agent",
    description="AI Agent for Meta to GHL customer messaging",
    version="1.0.0"
)

# Initialize webhook handler
webhook_handler = WebhookHandler()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GHL LangGraph Agent",
        "version": "1.0.0"
    }


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
        
        # Process the webhook
        result = await webhook_handler.handle_meta_lead(webhook_data)
        
        return JSONResponse(content=result, status_code=200)
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON in Meta webhook")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValueError as e:
        logger.error("Invalid Meta webhook data", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
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
                   webhook_type=webhook_data.type,
                   contact_id=webhook_data.contact_id)
        
        # Process the webhook
        result = await webhook_handler.handle_ghl_message(webhook_data)
        
        return JSONResponse(content=result, status_code=200)
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON in GHL webhook")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValueError as e:
        logger.error("Invalid GHL webhook data", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Error processing GHL webhook", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/test/conversation")
async def test_conversation(request: Request):
    """Test endpoint for conversation processing"""
    from .models import LeadInfo
    
    try:
        data = await request.json()
        contact_id = data.get("contact_id")
        message = data.get("message")
        
        if not contact_id or not message:
            raise HTTPException(status_code=400, detail="contact_id and message are required")
        
        # Process message through agent
        response = await process_ghl_message(
            contact_id=contact_id,
            conversation_id=None,
            message=message
        )
        
        return {
            "success": True,
            "response": response,
            "contact_id": contact_id
        }
    except Exception as e:
        logger.error("Error in test conversation", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    logger.info("Starting GHL LangGraph Agent", 
               host=settings.server_host, 
               port=settings.server_port)
    
    uvicorn.run(
        "src.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )