"""Task for checking and processing new leads"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import structlog
from ghl_agent.tools.ghl_tools import get_ghl_contact_info
from ghl_agent.config_loader import get_config

logger = structlog.get_logger()

class LeadChecker:
    """Check and process new leads from various sources"""
    
    def __init__(self):
        self.config = get_config()
        self.processed_leads = set()  # Track processed lead IDs
    
    async def check_new_leads(
        self, 
        minutes_since: int = 20,
        process_all: bool = False,
        sources: List[str] = ["meta", "ghl_form", "manual"]
    ) -> Dict[str, Any]:
        """Check for new leads from various sources
        
        Args:
            minutes_since: Check leads from last N minutes
            process_all: Process all leads, even if already processed
            sources: List of lead sources to check
            
        Returns:
            Summary of processed leads
        """
        since_time = datetime.now() - timedelta(minutes=minutes_since)
        logger.info(f"Checking leads since {since_time}")
        
        results = {
            "checked": 0,
            "new": 0,
            "processed": 0,
            "triaged": {
                "auto_respond": 0,
                "notify_human": 0,
                "ignored": 0
            }
        }
        
        # Check each source
        for source in sources:
            if source == "meta":
                leads = await self._check_meta_leads(since_time)
            elif source == "ghl_form":
                leads = await self._check_ghl_forms(since_time)
            elif source == "manual":
                leads = await self._check_manual_entries(since_time)
            else:
                continue
            
            results["checked"] += len(leads)
            
            # Process each lead
            for lead in leads:
                if not process_all and lead["id"] in self.processed_leads:
                    continue
                
                results["new"] += 1
                
                # Triage the lead
                triage_result = await self._triage_lead(lead)
                results["triaged"][triage_result["action"]] += 1
                
                # Process based on triage
                if triage_result["action"] == "auto_respond":
                    await self._process_lead(lead, triage_result)
                    results["processed"] += 1
                elif triage_result["action"] == "notify_human":
                    await self._notify_human(lead, triage_result)
                
                # Mark as processed
                self.processed_leads.add(lead["id"])
        
        logger.info(f"Lead check complete: {results}")
        return results
    
    async def _check_meta_leads(self, since_time: datetime) -> List[Dict[str, Any]]:
        """Check for leads from Meta (Facebook/Instagram)"""
        # This would integrate with Meta Lead Ads API
        # For now, return empty list
        return []
    
    async def _check_ghl_forms(self, since_time: datetime) -> List[Dict[str, Any]]:
        """Check for leads from GHL forms"""
        # This would check GHL for new form submissions
        # For now, return empty list
        return []
    
    async def _check_manual_entries(self, since_time: datetime) -> List[Dict[str, Any]]:
        """Check for manually entered leads"""
        # This would check a database or file for manual entries
        # For now, return empty list
        return []
    
    async def _triage_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Triage a lead based on configuration rules
        
        Returns:
            Dict with 'action' and 'reason'
        """
        message = lead.get("message", "").lower()
        
        # Check ignore patterns
        for pattern in self.config.triage.get("ignore", []):
            if pattern.lower() in message:
                return {
                    "action": "ignored",
                    "reason": f"Contains ignore pattern: {pattern}"
                }
        
        # Check notify patterns
        for pattern in self.config.triage.get("notify_human", []):
            if pattern.lower() in message:
                return {
                    "action": "notify_human",
                    "reason": f"Contains notify pattern: {pattern}"
                }
        
        # Check auto-respond patterns
        for pattern in self.config.triage.get("auto_respond", []):
            if pattern.lower() in message:
                return {
                    "action": "auto_respond",
                    "reason": f"Contains auto-respond pattern: {pattern}"
                }
        
        # Default to auto-respond for battery-related queries
        battery_keywords = ["batería", "battery", "solar", "apagón", "luz", "energía"]
        if any(keyword in message for keyword in battery_keywords):
            return {
                "action": "auto_respond",
                "reason": "Battery-related query"
            }
        
        # Default action
        return {
            "action": "notify_human",
            "reason": "No matching patterns"
        }
    
    async def _process_lead(self, lead: Dict[str, Any], triage_result: Dict[str, Any]):
        """Process a lead by starting a conversation"""
        logger.info(f"Processing lead {lead['id']}: {triage_result['reason']}")
        
        # This would trigger the main agent to start a conversation
        # For now, just log
        logger.info(f"Would start conversation for lead {lead['id']}")
    
    async def _notify_human(self, lead: Dict[str, Any], triage_result: Dict[str, Any]):
        """Notify human about a lead that needs attention"""
        logger.info(f"Notifying human about lead {lead['id']}: {triage_result['reason']}")
        
        # This could send an email, SMS, or Slack message
        # For now, just log
        logger.info(f"Would notify human about lead {lead['id']}")

# Function to be called by cron job
async def check_leads_task(
    task: str = "check_new_leads",
    minutes_since: int = 20,
    process_all: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """Task entry point for cron job"""
    if task != "check_new_leads":
        return {"error": f"Unknown task: {task}"}
    
    checker = LeadChecker()
    return await checker.check_new_leads(
        minutes_since=minutes_since,
        process_all=process_all
    )