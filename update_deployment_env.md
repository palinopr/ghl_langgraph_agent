# Update Deployment Environment Variables

## Quick Fix: Disable MCP Tools

Since GoHighLevel doesn't have an MCP server endpoint, you need to disable MCP and use the direct API tools instead.

### Steps to Update Your Deployment:

1. **Go to your LangSmith deployment page:**
   https://smith.langchain.com/o/d46348af-8871-4fc1-bb27-5d17f0589bd5/host/deployments/03e9a719-ff0b-40bb-8e5c-548ff6ae0abf

2. **Add/Update these environment variables:**

```env
# Disable MCP tools - use direct API instead
GHL_USE_MCP=false

# GoHighLevel Configuration
GHL_API_KEY=pit-7d1ae9f4-8373-49c1-bc6b-b67cb35bb7ca
GHL_LOCATION_ID=EJ92ICNR9AmnbKq7Z2VQ
GHL_CALENDAR_ID=eIHCWiTQjE1lTzjdz4xi

# OpenAI Configuration  
OPENAI_API_KEY=your-openai-api-key-here

# Optional - for better logging
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=outlet-media-bot

# Timezone
TIMEZONE=America/New_York
```

3. **Save and redeploy** (the deployment should restart automatically)

## What This Does:

- Sets `GHL_USE_MCP=false` which makes the agent use the direct API tools in `ghl_tools.py` instead of the MCP tools
- The direct API tools connect to the real GoHighLevel API endpoints
- This should fix the "Failed to send message via MCP" errors

## Test After Update:

Once the environment variables are updated and the deployment restarts, run this test:

```bash
curl -X POST https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app/runs/stream \
  -H 'Content-Type: application/json' \
  -H 'X-Api-Key: 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' \
  -d '{
    "assistant_id": "ghl_agent",
    "input": {
      "messages": [
        {"role": "human", "content": "Hola, necesito un sistema de baterías"}
      ],
      "contact_id": "test-123",
      "conversation_id": "conv-123"
    },
    "stream_mode": "updates"
  }'
```

## Alternative: If You Want to Keep MCP

If you want to use MCP properly, you would need to:

1. Set up an MCP server that wraps the GoHighLevel API
2. Deploy that MCP server somewhere accessible from LangGraph Cloud
3. Update the MCP client URL in your code

But for now, using the direct API tools is the simpler and more reliable approach.