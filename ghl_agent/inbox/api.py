"""FastAPI routes for Agent Inbox UI"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from langgraph.store.base import BaseStore
from ghl_agent.agent.graph import get_checkpointer_with_store
from .inbox_ui import AgentInbox
import structlog

logger = structlog.get_logger()

def get_inbox_store() -> BaseStore:
    """Get store instance for inbox"""
    _, store = get_checkpointer_with_store()
    return store

def create_inbox_router() -> APIRouter:
    """Create FastAPI router for inbox endpoints"""
    router = APIRouter(prefix="/inbox", tags=["inbox"])
    
    @router.get("/conversations")
    async def list_conversations(
        limit: int = 20,
        status: Optional[str] = None,
        store: BaseStore = Depends(get_inbox_store)
    ) -> List[Dict[str, Any]]:
        """List active conversations with filtering"""
        try:
            inbox = AgentInbox(store)
            conversations = await inbox.get_active_conversations(limit)
            
            # Filter by status if provided
            if status:
                status_map = {
                    "new": lambda c: c.get("stage") == "greeting",
                    "in_progress": lambda c: c.get("stage") in ["discovery", "qualification"],
                    "qualified": lambda c: c.get("stage") == "scheduling",
                    "completed": lambda c: c.get("appointment_scheduled", False)
                }
                
                if status in status_map:
                    conversations = [c for c in conversations if status_map[status](c)]
            
            return conversations
            
        except Exception as e:
            logger.error("Failed to list conversations", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/conversations/{contact_id}")
    async def get_conversation(
        contact_id: str,
        store: BaseStore = Depends(get_inbox_store)
    ) -> Dict[str, Any]:
        """Get detailed conversation view"""
        try:
            inbox = AgentInbox(store)
            details = await inbox.get_conversation_details(contact_id)
            
            if "error" in details:
                raise HTTPException(status_code=404, detail=details["error"])
            
            return details
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Failed to get conversation", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/metrics")
    async def get_metrics(
        store: BaseStore = Depends(get_inbox_store)
    ) -> Dict[str, Any]:
        """Get inbox metrics and statistics"""
        try:
            inbox = AgentInbox(store)
            metrics = await inbox.get_metrics()
            return metrics
            
        except Exception as e:
            logger.error("Failed to get metrics", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.post("/conversations/{contact_id}/flag")
    async def flag_conversation(
        contact_id: str,
        reason: str,
        store: BaseStore = Depends(get_inbox_store)
    ) -> Dict[str, str]:
        """Flag a conversation for review"""
        try:
            # Store flag in preferences
            namespace = ("flags", contact_id)
            flag_data = {
                "flagged": True,
                "reason": reason,
                "flagged_at": datetime.now().isoformat()
            }
            store.put(namespace, str(uuid.uuid4()), flag_data)
            
            logger.info("Conversation flagged", contact_id=contact_id, reason=reason)
            return {"status": "flagged", "contact_id": contact_id}
            
        except Exception as e:
            logger.error("Failed to flag conversation", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/search")
    async def search_conversations(
        query: str,
        store: BaseStore = Depends(get_inbox_store)
    ) -> List[Dict[str, Any]]:
        """Search conversations by customer name or content"""
        try:
            inbox = AgentInbox(store)
            all_conversations = await inbox.get_active_conversations(limit=100)
            
            # Simple search implementation
            query_lower = query.lower()
            results = []
            
            for conv in all_conversations:
                if (query_lower in conv.get("customer_name", "").lower() or
                    query_lower in str(conv.get("equipment_list", [])).lower() or
                    query_lower in conv.get("housing_type", "").lower()):
                    results.append(conv)
            
            return results[:20]  # Limit results
            
        except Exception as e:
            logger.error("Failed to search conversations", error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
    
    return router

# Missing imports
from datetime import datetime
import uuid