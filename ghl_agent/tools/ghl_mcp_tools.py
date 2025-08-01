"""GoHighLevel MCP (Model Context Protocol) tools for LangGraph"""
import httpx
import json
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
        
        # MCP uses JSON-RPC format
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": input_data
            },
            "id": 1
        }
        
        logger.info(f"Calling MCP tool: {tool_name}", input_preview=str(input_data)[:100])
        
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            # Log the response for debugging
            logger.debug(f"MCP Response: {response.status_code} - Headers: {dict(response.headers)}")
            
            if response.status_code >= 400:
                logger.warning(f"MCP API error: {response.status_code} - {response.text[:500]}")
                response.raise_for_status()
            
            # MCP returns Server-Sent Events format
            response_text = response.text
            
            # Log raw response for debugging
            logger.debug(f"MCP Raw Response: {response_text[:500]}")
            
            # Parse SSE response
            if response_text.startswith("event:"):
                lines = response_text.strip().split('\n')
                for line in lines:
                    if line.startswith("data: "):
                        data_json = line[6:]  # Remove "data: " prefix
                        parsed = json.loads(data_json)
                        
                        # Check for errors
                        if "error" in parsed:
                            error = parsed["error"]
                            raise Exception(f"MCP Error: {error.get('message', 'Unknown error')}")
                        
                        # Extract result
                        if "result" in parsed:
                            result = parsed["result"]
                            # Parse nested JSON if needed
                            if isinstance(result, dict) and "content" in result:
                                content = result["content"]
                                if isinstance(content, list) and content:
                                    text_content = content[0].get("text", "")
                                    try:
                                        return json.loads(text_content)
                                    except:
                                        return {"raw_response": text_content}
                            return result
            
            # Fallback to raw response
            return {"raw_response": response_text}


# Initialize MCP client
mcp_client = GHLMCPClient()


@tool
async def send_mcp_message(contact_id: str, message: str, conversation_id: Optional[str] = None) -> str:
    """Send a message via GoHighLevel MCP Server"""
    try:
        logger.info(f"Attempting to send WhatsApp message via MCP to contact: {contact_id}")
        
        # First, we need to get or create a conversation
        if not conversation_id:
            # Search for existing conversation with this contact
            try:
                search_result = await mcp_client.call_tool(
                    "conversations_search-conversation",
                    {
                        "query": contact_id,  # Try searching by contact ID
                        "limit": 1
                    }
                )
                
                # Parse the MCP response correctly
                if isinstance(search_result, dict) and "content" in search_result:
                    content = search_result["content"]
                    if isinstance(content, list) and content:
                        text_content = content[0].get("text", "")
                        try:
                            parsed_result = json.loads(text_content)
                            if parsed_result.get("success") and "data" in parsed_result:
                                conversations = parsed_result["data"].get("conversations", [])
                                if conversations:
                                    conversation_id = conversations[0].get("id")
                                    logger.info(f"Found existing conversation: {conversation_id}")
                                else:
                                    logger.warning("No conversations found in search")
                            else:
                                logger.warning(f"Search failed: {parsed_result}")
                        except json.JSONDecodeError:
                            logger.warning(f"Could not parse search result: {text_content[:100]}")
                else:
                    conversations = search_result.get("conversations", [])
                    if conversations:
                        conversation_id = conversations[0].get("id")
                        logger.info(f"Found existing conversation: {conversation_id}")
                    else:
                        logger.warning("No conversation found for contact")
            except Exception as e:
                logger.warning(f"Could not search for conversation: {e}")
        
        # According to MCP schema, parameters need body_ prefix
        input_data = {
            "body_type": "WhatsApp",
            "body_contactId": contact_id,
            "body_message": message
        }
        
        # Add conversation ID if available (as threadId)
        if conversation_id:
            input_data["body_threadId"] = conversation_id
        
        # Send the message using the correct tool name
        result = await mcp_client.call_tool(
            "conversations_send-a-new-message",
            input_data
        )
        
        # Parse the MCP response for message sending
        if isinstance(result, dict) and "content" in result:
            content = result["content"]
            if isinstance(content, list) and content:
                text_content = content[0].get("text", "")
                try:
                    parsed_result = json.loads(text_content)
                    if parsed_result.get("success"):
                        message_data = parsed_result.get("data", {})
                        message_id = message_data.get('messageId', message_data.get('id', 'sent'))
                        logger.info(f"WhatsApp message sent successfully via MCP. ID: {message_id}")
                        return f"Message sent successfully via MCP. Message ID: {message_id}"
                    else:
                        error_msg = parsed_result.get("data", {}).get("message", "Unknown error")
                        logger.error(f"MCP send failed: {error_msg}")
                        return f"Failed to send message via MCP: {error_msg}"
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse send result: {text_content[:100]}")
        
        # Fallback handling
        message_id = result.get('messageId', result.get('id', 'unknown'))
        logger.info(f"WhatsApp message sent (parsed fallback). ID: {message_id}")
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