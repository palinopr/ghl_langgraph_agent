"""Simplified webhook app for LangGraph deployment"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import structlog
import os

# Configure logging
logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="Battery Consultation Webhooks",
    description="Webhook endpoints for GHL integration",
    version="2.0.0"
)

@app.post("/webhook/ghl")
async def handle_ghl_webhook(request: Request):
    """Handle GoHighLevel webhook - simplified version"""
    try:
        data = await request.json()
        
        # Log the webhook receipt
        logger.info("GHL webhook received", 
                   contact_id=data.get("id"),
                   has_message=bool(data.get("message")))
        
        # Basic validation
        if not data.get("id") or not data.get("message"):
            return {"success": False, "error": "Missing required fields"}
        
        # Return success - the agent processes messages through the graph
        return JSONResponse(content={
            "success": True,
            "message": "Webhook received",
            "contact_id": data.get("id")
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
        "webhooks": "ready"
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