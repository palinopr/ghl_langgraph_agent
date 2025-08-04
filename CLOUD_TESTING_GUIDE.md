# LangGraph Cloud Testing Guide

## Quick Start

### 1. Install SDK (Recommended)
```bash
pip install langgraph-sdk
```

### 2. Test with Python SDK

```python
from langgraph_sdk import get_client

# Your deployment details
deployment_url = "https://ghl-customer-agent-6938642b2e79555cbe304569cd0f8a05.us.langgraph.app"
api_key = "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"

# Initialize client
client = get_client(url=deployment_url, api_key=api_key)

# Run threadless (stateless) test
async for chunk in client.runs.stream(
    None,  # No thread ID = threadless run
    "ghl_agent",  # Assistant ID from langgraph.json
    input={
        "messages": [
            {"role": "human", "content": "Hola, necesito baterías"}
        ],
        "contact_id": "test-123",
        "conversation_id": "conv-123"
    },
    stream_mode="updates"
):
    print(f"Event: {chunk.event}")
    print(f"Data: {chunk.data}")
```

### 3. Test with REST API (No SDK)

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

## Test Scripts

### Basic Test
```bash
python test_langsmith_cloud.py
```

### Comprehensive Test
```bash
python test_cloud_deployment.py
```

## Common Operations

### 1. List Assistants
```python
assistants = await client.assistants.search()
for assistant in assistants:
    print(f"{assistant['name']} - {assistant['assistant_id']}")
```

### 2. Create Thread
```python
thread = await client.threads.create(
    metadata={"user_id": "123"}
)
thread_id = thread["thread_id"]
```

### 3. Run with Thread (Stateful)
```python
async for chunk in client.runs.stream(
    thread_id,
    "ghl_agent",
    input={"messages": [{"role": "human", "content": "Hello"}]},
    stream_mode=["values", "updates", "messages"]
):
    print(chunk)
```

### 4. Get Thread State
```python
state = await client.threads.get_state(thread_id)
print(state)
```

## Deployment Management

### Check Deployment Status
1. Go to: https://smith.langchain.com/
2. Navigate to Deployments
3. Find deployment ID: 03e9a719-ff0b-40bb-8e5c-548ff6ae0abf
4. Check status and logs

### Update Environment Variables
1. In LangSmith UI, go to your deployment
2. Click "Environment Variables"
3. Add/Update:
   ```
   GHL_API_KEY=your-ghl-api-key
   GHL_LOCATION_ID=your-location-id
   GHL_CALENDAR_ID=your-calendar-id
   OPENAI_API_KEY=your-openai-key
   ```

### View Logs
1. In deployment details, click "Logs"
2. Filter by time range or search
3. Check for errors or warnings

## Troubleshooting

### Common Issues

1. **"Invalid assistant: 'agent'"**
   - Use `assistant_id: "ghl_agent"` not "agent"

2. **"Failed to send message via MCP"**
   - MCP code has been removed
   - Messages are sent via direct GHL API

3. **Connection timeouts**
   - Increase timeout in client configuration
   - Check deployment is running in LangSmith UI

4. **Authentication errors**
   - Verify API key is correct
   - Check key permissions in LangSmith

### Debug Tips

1. **Enable verbose logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check raw responses**:
   ```python
   # Use httpx directly for debugging
   import httpx
   response = await client.get(url, headers=headers)
   print(response.status_code, response.text)
   ```

3. **Monitor in LangSmith**:
   - Go to deployment → Monitoring
   - Check traces for each run
   - View detailed error messages

## Best Practices

1. **Use threadless runs for testing** - Simpler and stateless
2. **Start with small tests** - Basic message → Complex flows
3. **Check logs frequently** - LangSmith UI shows detailed logs
4. **Test error scenarios** - Invalid inputs, missing fields
5. **Monitor performance** - Check response times in traces

## Next Steps

1. **Production Setup**:
   - Configure production environment variables
   - Set up monitoring alerts
   - Implement error handling

2. **Webhook Integration**:
   - Update GHL webhooks to point to deployment URL
   - Test with real GHL messages
   - Monitor webhook delivery

3. **Scaling**:
   - Monitor usage in LangSmith
   - Adjust instance configuration if needed
   - Set up autoscaling rules