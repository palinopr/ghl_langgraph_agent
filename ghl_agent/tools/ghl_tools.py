import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from langchain_core.tools import tool
from pydantic import BaseModel, Field
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from ghl_agent.config import settings

logger = structlog.get_logger()


class GHLClient:
    """Client for GoHighLevel API operations"""
    
    def __init__(self):
        self.base_url = settings.ghl_api_base_url
        self.headers = {
            "Authorization": f"Bearer {settings.ghl_api_key}",
            "Content-Type": "application/json",
            "Version": "2021-07-28"
        }
        self.location_id = settings.ghl_location_id
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to GHL API with retry logic"""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
    
    async def send_message(self, contact_id: str, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Send message to contact via GHL"""
        payload = {
            "type": "WhatsApp",
            "contactId": contact_id,
            "message": message
        }
        
        if conversation_id:
            payload["conversationId"] = conversation_id
        
        logger.info("Sending GHL message", 
                   contact_id=contact_id,
                   message_preview=message[:50])
        
        return await self._make_request(
            "POST",
            f"/conversations/messages",
            json=payload
        )
    
    async def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact information from GHL"""
        return await self._make_request(
            "GET",
            f"/contacts/{contact_id}"
        )
    
    async def get_conversation_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation history from GHL"""
        response = await self._make_request(
            "GET",
            f"/conversations/{conversation_id}/messages"
        )
        return response.get("messages", [])
    
    async def update_contact(self, contact_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update contact information in GHL"""
        return await self._make_request(
            "PUT",
            f"/contacts/{contact_id}",
            json=data
        )
    
    async def get_calendar_slots(self, calendar_id: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get available calendar slots"""
        # Convert date strings to timestamps
        from datetime import datetime as dt
        start_timestamp = int(dt.fromisoformat(start_date).timestamp() * 1000)
        end_timestamp = int(dt.fromisoformat(end_date).timestamp() * 1000)
        
        params = {
            "startDate": start_timestamp,
            "endDate": end_timestamp,
            "timezone": "UTC"
        }
        
        response = await self._make_request(
            "GET",
            f"/calendars/{calendar_id}/free-slots",
            params=params
        )
        return response.get("slots", [])
    
    async def book_appointment(self, contact_id: str, calendar_id: str, 
                             slot_start: datetime, slot_end: datetime,
                             timezone: str = "UTC", title: Optional[str] = None,
                             notes: Optional[str] = None) -> Dict[str, Any]:
        """Book an appointment for a contact"""
        payload = {
            "calendarId": calendar_id,
            "contactId": contact_id,
            "startTime": slot_start.isoformat(),
            "endTime": slot_end.isoformat(),
            "timezone": timezone,
            "title": title or "Appointment",
            "appointmentStatus": "confirmed"
        }
        
        if notes:
            payload["notes"] = notes
        
        return await self._make_request(
            "POST",
            f"/calendars/{calendar_id}/appointments",
            json=payload
        )


# Initialize GHL client
ghl_client = GHLClient()




@tool
async def send_ghl_message(contact_id: str, message: str, conversation_id: Optional[str] = None) -> str:
    """Send a message to a customer via GoHighLevel"""
    try:
        result = await ghl_client.send_message(contact_id, message, conversation_id)
        return f"Message sent successfully. Message ID: {result.get('id', 'unknown')}"
    except Exception as e:
        logger.error("Failed to send GHL message", error=str(e))
        return f"Failed to send message: {str(e)}"


@tool
async def get_ghl_contact_info(contact_id: str) -> Dict[str, Any]:
    """Get contact information from GoHighLevel"""
    try:
        contact = await ghl_client.get_contact(contact_id)
        return {
            "success": True,
            "contact": {
                "id": contact.get("id"),
                "name": contact.get("name"),
                "email": contact.get("email"),
                "phone": contact.get("phone"),
                "tags": contact.get("tags", []),
                "customFields": contact.get("customFields", {})
            }
        }
    except Exception as e:
        logger.error("Failed to get contact info", error=str(e))
        return {"success": False, "error": str(e)}


@tool
async def update_ghl_contact(contact_id: str, updates: Dict[str, Any]) -> str:
    """Update contact information in GoHighLevel"""
    try:
        result = await ghl_client.update_contact(contact_id, updates)
        return f"Contact updated successfully"
    except Exception as e:
        logger.error("Failed to update contact", error=str(e))
        return f"Failed to update contact: {str(e)}"


@tool
async def get_available_calendar_slots(days_ahead: int = 7) -> List[Dict[str, Any]]:
    """Get available calendar slots for the next N days"""
    try:
        if not settings.ghl_calendar_id:
            return {"error": "Calendar ID not configured"}
            
        start_date = datetime.utcnow().date().isoformat()
        end_date = (datetime.utcnow().date() + timedelta(days=days_ahead)).isoformat()
        
        slots = await ghl_client.get_calendar_slots(settings.ghl_calendar_id, start_date, end_date)
        return [
            {
                "date": slot.get("date"),
                "time": slot.get("time"),
                "available": slot.get("available", True)
            }
            for slot in slots
        ]
    except Exception as e:
        logger.error("Failed to get calendar slots", error=str(e))
        return []


@tool
async def book_ghl_appointment(
    contact_id: str,
    appointment_datetime: str,
    duration_minutes: int = 30,
    title: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """Book an appointment in GoHighLevel"""
    try:
        if not settings.ghl_calendar_id:
            return "Failed to book appointment: Calendar ID not configured"
            
        start_time = datetime.fromisoformat(appointment_datetime)
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        result = await ghl_client.book_appointment(
            contact_id=contact_id,
            calendar_id=settings.ghl_calendar_id,
            slot_start=start_time,
            slot_end=end_time,
            title=title,
            notes=notes
        )
        return f"Appointment booked successfully. Appointment ID: {result.get('id', 'unknown')}"
    except Exception as e:
        logger.error("Failed to book appointment", error=str(e))
        return f"Failed to book appointment: {str(e)}"


# Export all tools
GHL_TOOLS = [
    send_ghl_message,
    get_ghl_contact_info,
    update_ghl_contact,
    get_available_calendar_slots,
    book_ghl_appointment
]