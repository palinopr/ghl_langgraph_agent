"""Agent Inbox UI integration for conversation monitoring and management"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import structlog
import json
from langgraph.store.base import BaseStore

logger = structlog.get_logger()

class AgentInbox:
    """Agent Inbox for monitoring and managing conversations"""
    
    def __init__(self, store: BaseStore):
        self.store = store
        
    async def get_active_conversations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get list of active conversations"""
        try:
            # Search for recent conversations
            namespace = ("conversation", "*")
            conversations = []
            
            # Get all conversation memories
            memories = self.store.search(namespace)
            
            for memory in memories[:limit]:
                conv_data = memory.value
                contact_id = memory.namespace[1]
                
                # Get latest insights if available
                insights_namespace = ("insights", contact_id)
                insights = self.store.search(insights_namespace)
                latest_insight = insights[0].value if insights else {}
                
                conversations.append({
                    "contact_id": contact_id,
                    "customer_name": conv_data.get("customer_name", "Unknown"),
                    "last_interaction": conv_data.get("last_interaction"),
                    "housing_type": conv_data.get("housing_type"),
                    "equipment_list": conv_data.get("equipment_list", []),
                    "stage": conv_data.get("conversation_stage", "unknown"),
                    "sentiment": latest_insight.get("sentiment", "neutral"),
                    "next_action": latest_insight.get("next_action", "Continue conversation"),
                    "appointment_scheduled": conv_data.get("appointment_scheduled", False)
                })
            
            # Sort by last interaction
            conversations.sort(
                key=lambda x: x.get("last_interaction", ""), 
                reverse=True
            )
            
            return conversations
            
        except Exception as e:
            logger.error("Failed to get active conversations", error=str(e))
            return []
    
    async def get_conversation_details(self, contact_id: str) -> Dict[str, Any]:
        """Get detailed view of a specific conversation"""
        try:
            # Get conversation memory
            conv_namespace = ("conversation", contact_id)
            conv_memories = self.store.search(conv_namespace)
            
            if not conv_memories:
                return {"error": "Conversation not found"}
            
            conv_data = conv_memories[0].value
            
            # Get insights
            insights_namespace = ("insights", contact_id)
            insights = self.store.search(insights_namespace)
            
            # Get preferences
            pref_namespace = ("preferences", contact_id)
            preferences = self.store.search(pref_namespace)
            
            return {
                "contact_id": contact_id,
                "conversation": conv_data,
                "insights": [i.value for i in insights],
                "preferences": preferences[0].value if preferences else {},
                "summary": self._generate_summary(conv_data, insights)
            }
            
        except Exception as e:
            logger.error("Failed to get conversation details", error=str(e))
            return {"error": str(e)}
    
    def _generate_summary(self, conv_data: Dict, insights: List) -> Dict[str, Any]:
        """Generate conversation summary"""
        latest_insight = insights[0].value if insights else {}
        
        return {
            "status": self._determine_status(conv_data),
            "progress": self._calculate_progress(conv_data),
            "key_points": latest_insight.get("key_topics", []),
            "pain_points": latest_insight.get("pain_points", []),
            "opportunities": latest_insight.get("opportunities", []),
            "recommended_actions": latest_insight.get("recommendations", [])
        }
    
    def _determine_status(self, conv_data: Dict) -> str:
        """Determine conversation status"""
        if conv_data.get("appointment_scheduled"):
            return "completed"
        elif conv_data.get("interested_in_consultation"):
            return "qualified"
        elif conv_data.get("housing_type"):
            return "in_progress"
        else:
            return "new"
    
    def _calculate_progress(self, conv_data: Dict) -> int:
        """Calculate conversation progress percentage"""
        progress = 0
        
        if conv_data.get("housing_type"):
            progress += 25
        if conv_data.get("equipment_list"):
            progress += 25
        if conv_data.get("interested_in_consultation"):
            progress += 25
        if conv_data.get("appointment_scheduled"):
            progress += 25
            
        return progress
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get inbox metrics and statistics"""
        try:
            conversations = await self.get_active_conversations(limit=100)
            
            total = len(conversations)
            completed = sum(1 for c in conversations if c.get("appointment_scheduled"))
            qualified = sum(1 for c in conversations if c.get("stage") == "qualification")
            
            sentiment_counts = {
                "positive": sum(1 for c in conversations if c.get("sentiment") == "positivo"),
                "neutral": sum(1 for c in conversations if c.get("sentiment") == "neutral"),
                "negative": sum(1 for c in conversations if c.get("sentiment") == "negativo")
            }
            
            return {
                "total_conversations": total,
                "completed_appointments": completed,
                "qualified_leads": qualified,
                "conversion_rate": (completed / total * 100) if total > 0 else 0,
                "sentiment_distribution": sentiment_counts,
                "active_conversations": total - completed
            }
            
        except Exception as e:
            logger.error("Failed to get metrics", error=str(e))
            return {}

# Export
__all__ = ["AgentInbox"]