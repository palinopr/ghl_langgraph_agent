import hashlib
import hmac
import json
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
import structlog

from ghl_agent.config import settings
from ghl_agent.models import GHLWebhookPayload, MetaLeadWebhook, LeadInfo
from ghl_agent.agent.graph import process_ghl_message

logger = structlog.get_logger()


class WebhookHandler:
    """Unified webhook handler for both local and LangGraph Cloud deployment"""
    
    def verify_meta_webhook(self, token: str) -> bool:
        """Verify Meta webhook verification token"""
        return token == settings.meta_verify_token
    
    def verify_meta_signature(self, payload: bytes, signature: str) -> bool:
        """Verify Meta webhook signature"""
        if not settings.meta_app_secret:
            logger.warning("Meta app secret not configured")
            return True  # Skip verification in development
        
        expected_signature = hmac.new(
            settings.meta_app_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return f"sha256={expected_signature}" == signature
    
    async def handle_meta_lead(self, webhook_data: MetaLeadWebhook) -> Dict[str, Any]:
        """Process Meta lead generation webhook"""
        try:
            leads_processed = []
            
            for entry in webhook_data.entry:
                for change in entry.get("changes", []):
                    if change.get("field") == "leadgen":
                        lead_data = change.get("value", {})
                        
                        # Extract lead information
                        lead_id = lead_data.get("leadgen_id")
                        
                        # Process initial greeting
                        response = await process_ghl_message(
                            contact_id=f"meta-{lead_id}",
                            conversation_id=None,
                            message="Hi, I just saw your ad and I'm interested in your services."
                        )
                        
                        leads_processed.append({
                            "lead_id": lead_id,
                            "contact_id": f"meta-{lead_id}",
                            "status": "processed",
                            "initial_response": response
                        })
            
            return {
                "success": True,
                "leads_processed": leads_processed
            }
            
        except Exception as e:
            logger.error("Error processing Meta lead webhook", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
    
    async def handle_ghl_message(self, webhook_data: GHLWebhookPayload) -> Dict[str, Any]:
        """Process GHL message webhook"""
        try:
            # Skip if no message content
            if not webhook_data.message:
                return {"success": True, "action": "skipped", "reason": "no message content"}
            
            # Process message through agent
            response = await process_ghl_message(
                contact_id=webhook_data.contact_id,
                conversation_id=webhook_data.conversation_id,
                message=webhook_data.message
            )
            
            return {
                "success": True,
                "response": response,
                "contact_id": webhook_data.contact_id,
                "conversation_id": webhook_data.conversation_id
            }
            
        except Exception as e:
            logger.error("Error processing GHL message webhook", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))


class WebhookValidator:
    """Validator for webhook payloads"""
    
    @staticmethod
    def validate_ghl_webhook(data: Dict[str, Any]) -> GHLWebhookPayload:
        """Validate and parse GHL webhook data"""
        required_fields = ["type", "locationId", "contactId"]
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        return GHLWebhookPayload(
            type=data["type"],
            location_id=data["locationId"],
            contact_id=data["contactId"],
            conversation_id=data.get("conversationId"),
            message=data.get("message", {}).get("body"),
            attachments=data.get("message", {}).get("attachments", []),
            metadata=data.get("metadata", {})
        )
    
    @staticmethod
    def validate_meta_webhook(data: Dict[str, Any]) -> MetaLeadWebhook:
        """Validate and parse Meta webhook data"""
        if "entry" not in data or "object" not in data:
            raise ValueError("Invalid Meta webhook format")
        
        return MetaLeadWebhook(
            entry=data["entry"],
            object=data["object"]
        )