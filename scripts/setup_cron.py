#!/usr/bin/env python3
"""Setup cron job for periodic lead checking"""

import asyncio
import argparse
import os
from typing import Optional
from langgraph_sdk import get_client
import structlog

logger = structlog.get_logger()

async def create_cron_job(
    deployment_url: str,
    api_key: Optional[str] = None,
    schedule: str = "*/15 * * * *",  # Every 15 minutes
    assistant_id: str = "ghl_agent"
):
    """Create a cron job for periodic lead checking
    
    Args:
        deployment_url: LangGraph deployment URL
        api_key: API key for authentication
        schedule: Cron schedule expression
        assistant_id: Assistant ID to use
    """
    try:
        # Initialize client
        client = get_client(url=deployment_url, api_key=api_key)
        
        # Define the cron job payload
        cron_payload = {
            "schedule": schedule,
            "input": {
                "task": "check_new_leads",
                "minutes_since": 20,  # Check leads from last 20 minutes
                "process_all": False,  # Only process new leads
            }
        }
        
        # Create the cron job
        logger.info(f"Creating cron job with schedule: {schedule}")
        
        # For LangGraph Cloud, we need to use the runs API with a cron schedule
        # This is a placeholder - actual implementation depends on LangGraph Cloud API
        
        # Note: LangGraph Cloud cron job creation is done through the UI or deployment config
        # This script shows what the cron job would do when triggered
        
        print(f"""
Cron Job Configuration
=====================

To set up automatic lead checking, add this to your langgraph.json:

"crons": [
  {{
    "schedule": "{schedule}",
    "input": {{
      "task": "check_new_leads",
      "minutes_since": 20,
      "process_all": false
    }}
  }}
]

Or configure through LangSmith UI:
1. Go to your deployment
2. Click on "Crons" tab
3. Add new cron with:
   - Schedule: {schedule}
   - Input: {{"task": "check_new_leads", "minutes_since": 20}}

The cron job will:
- Run every 15 minutes
- Check for new leads in the last 20 minutes
- Process only unprocessed leads
- Send automated responses based on triage rules
""")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to create cron job: {e}")
        return False

async def test_cron_execution(
    deployment_url: str,
    api_key: Optional[str] = None,
    assistant_id: str = "ghl_agent"
):
    """Test what the cron job would do"""
    try:
        client = get_client(url=deployment_url, api_key=api_key)
        
        # Simulate cron job execution
        thread = await client.threads.create()
        
        run = await client.runs.create(
            thread["thread_id"],
            assistant_id,
            input={
                "task": "check_new_leads",
                "minutes_since": 20,
                "process_all": False
            }
        )
        
        # Stream results
        print("\nTesting cron job execution...")
        async for chunk in client.runs.stream(
            thread["thread_id"],
            run["run_id"],
            stream_mode="updates"
        ):
            if chunk.event == "updates":
                print(f"Update: {chunk.data}")
        
        print("\nCron job test completed successfully!")
        
    except Exception as e:
        logger.error(f"Cron job test failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Setup cron job for lead checking")
    parser.add_argument("--url", required=True, help="LangGraph deployment URL")
    parser.add_argument("--api-key", help="API key (or set LANGSMITH_API_KEY)")
    parser.add_argument("--schedule", default="*/15 * * * *", help="Cron schedule (default: every 15 min)")
    parser.add_argument("--test", action="store_true", help="Test cron execution")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        print("Error: API key required. Set LANGSMITH_API_KEY or use --api-key")
        return
    
    if args.test:
        asyncio.run(test_cron_execution(args.url, api_key))
    else:
        asyncio.run(create_cron_job(args.url, api_key, args.schedule))

if __name__ == "__main__":
    main()