from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class LeadInfo(BaseModel):
    contact_id: str
    conversation_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    meta_lead_id: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    requirements: Optional[Dict[str, Any]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)




class GHLWebhookPayload(BaseModel):
    """GoHighLevel webhook payload structure"""
    id: str  # contact.id
    name: Optional[str] = None  # contact.name
    email: Optional[str] = None  # contact.email
    phone: Optional[str] = None  # contact.phone
    message: str  # message.body


class MetaLeadWebhook(BaseModel):
    """Meta lead generation webhook payload"""
    entry: List[Dict[str, Any]]
    object: str


