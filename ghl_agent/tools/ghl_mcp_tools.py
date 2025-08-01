"""GoHighLevel MCP (Model Context Protocol) tools for LangGraph"""
import httpx
from typing import Dict, List, Optional, Any
from langchain_core.tools import tool
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
import os

from ghl_agent.config import settings

logger = structlog.get_logger()


class GHLMCPClient:
    """Client for GoHighLevel MCP Server operations"""
    
    def __init__(self):
        self.base_url = "https://services.leadconnectorhq.com/mcp/"
        self.headers = {
            "Authorization": f"Bearer {settings.ghl_api_key}",
            "locationId": settings.ghl_location_id,
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"  # MCP requires both
        }
    
    @retry(
        stop=stop_after_attempt(int(os.getenv("GHL_RETRY_ATTEMPTS", "3"))),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def call_tool(self, tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool with retry logic"""
        # Use longer timeout in deployment environment
        is_deployment = bool(os.getenv("LANGGRAPH_AUTH_TYPE"))
        timeout_seconds = float(os.getenv("GHL_TIMEOUT_SECONDS", "60" if is_deployment else "30"))
        
        payload = {
            "tool": tool_name,
            "input": input_data
        }
        
        logger.info(f"Calling MCP tool: {tool_name}", input_preview=str(input_data)[:100])
        
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            # Log the response for debugging
            if response.status_code >= 400:
                logger.warning(f"MCP API error: {response.status_code} - {response.text[:200]}")
            
            response.raise_for_status()
            return response.json()


# Initialize MCP client
mcp_client = GHLMCPClient()


@tool
async def send_mcp_message(contact_id: str, message: str, conversation_id: Optional[str] = None) -> str:
    """Send a message via GoHighLevel MCP Server"""
    try:
        logger.info(f"Attempting to send WhatsApp message via MCP to contact: {contact_id}")
        
        # MCP expects different parameter names
        input_data = {
            "conversationId": conversation_id,  # MCP might need conversation ID
            "type": "WhatsApp",
            "message": message
        }
        
        # If we don't have conversation_id, we might need to search for it first
        if not conversation_id:
            # Try to find existing conversation
            try:
                search_result = await mcp_client.call_tool(
                    "conversations_search-conversation",
                    {"contactId": contact_id, "limit": 1}
                )
                
                if search_result.get("conversations"):
                    conversation_id = search_result["conversations"][0]["id"]
                    input_data["conversationId"] = conversation_id
                    logger.info(f"Found existing conversation: {conversation_id}")
            except Exception as e:
                logger.warning(f"Could not search for conversation: {e}")
        
        # Send the message
        result = await mcp_client.call_tool(
            "conversations_send-a-new-message",
            input_data
        )
        
        message_id = result.get('messageId', result.get('id', 'unknown'))
        logger.info(f"WhatsApp message sent successfully via MCP. ID: {message_id}")
        return f"Message sent successfully via MCP. Message ID: {message_id}"
        
    except RetryError as e:
        logger.error(f"All MCP retry attempts failed for contact {contact_id}")
        
        # Try to extract the actual error from the last attempt
        last_error_msg = "Unknown error"
        if hasattr(e, 'last_attempt') and e.last_attempt:
            last_exception = e.last_attempt.exception()
            if isinstance(last_exception, httpx.HTTPStatusError):
                last_error_msg = f"HTTP {last_exception.response.status_code}"
                logger.error(f"Last HTTP error: {last_exception.response.status_code} - {last_exception.response.text[:200]}")
            else:
                last_error_msg = str(last_exception)
        
        return f"Unable to send message via MCP due to connection issues. (Error: {last_error_msg})"
        
    except httpx.HTTPStatusError as e:
        logger.error(f"MCP HTTP Error: {e.response.status_code}", 
                    contact_id=contact_id,
                    error_body=e.response.text)
        return f"Failed to send message via MCP: HTTP {e.response.status_code}"
        
    except Exception as e:
        logger.error("Failed to send message via MCP", 
                    contact_id=contact_id,
                    error=str(e),
                    error_type=type(e).__name__)
        return f"Failed to send message via MCP: {str(e)}"


@tool
async def get_mcp_contact(contact_id: str) -> Dict[str, Any]:
    """Get contact information via GoHighLevel MCP Server"""
    try:
        result = await mcp_client.call_tool(
            "contacts_get-contact",
            {"contactId": contact_id}
        )
        
        return {
            "success": True,
            "contact": result.get("contact", result)
        }
    except Exception as e:
        logger.error("Failed to get contact via MCP", error=str(e))
        return {"success": False, "error": str(e)}


@tool
async def update_mcp_contact(contact_id: str, updates: Dict[str, Any]) -> str:
    """Update contact information via GoHighLevel MCP Server"""
    try:
        input_data = {"contactId": contact_id}
        input_data.update(updates)
        
        result = await mcp_client.call_tool(
            "contacts_update-contact",
            input_data
        )
        return "Contact updated successfully via MCP"
    except Exception as e:
        logger.error("Failed to update contact via MCP", error=str(e))
        return f"Failed to update contact via MCP: {str(e)}"


@tool
async def get_mcp_calendar_events(calendar_id: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get calendar events via GoHighLevel MCP Server"""
    try:
        input_data = {}
        if calendar_id:
            input_data["calendarId"] = calendar_id
        elif user_id:
            input_data["userId"] = user_id
        else:
            input_data["locationId"] = settings.ghl_location_id
            
        result = await mcp_client.call_tool(
            "calendars_get-calendar-events",
            input_data
        )
        return result.get("events", [])
    except Exception as e:
        logger.error("Failed to get calendar events via MCP", error=str(e))
        return []


# Export MCP tools
GHL_MCP_TOOLS = [
    send_mcp_message,
    get_mcp_contact,
    update_mcp_contact,
    get_mcp_calendar_events
]