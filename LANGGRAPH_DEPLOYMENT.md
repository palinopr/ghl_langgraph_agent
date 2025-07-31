# LangGraph Cloud Deployment Guide

This guide will help you deploy the GHL agent to LangGraph Cloud.

## Prerequisites

1. **LangSmith Account** with LangGraph Cloud access
2. **LangGraph CLI** installed:
   ```bash
   pip install -U langgraph-cli
   ```
3. **API Keys** ready:
   - OpenAI API key
   - GoHighLevel API key
   - LangSmith API key

## Deployment Steps

### 1. Login to LangGraph Cloud

```bash
langgraph auth login
```

### 2. Deploy the Agent

From the project root directory:

```bash
langgraph deploy --name "ghl-customer-agent"
```

This will:
- Package your agent
- Upload to LangGraph Cloud
- Return your deployment URL

### 3. Configure Environment Variables

After deployment, set your environment variables:

```bash
langgraph env set GHL_API_KEY "your-ghl-api-key"
langgraph env set GHL_LOCATION_ID "your-location-id"
langgraph env set GHL_CALENDAR_ID "your-calendar-id"
langgraph env set OPENAI_API_KEY "your-openai-key"
```

### 4. Test the Deployment

```bash
# Test with curl
curl -X POST https://your-deployment-id.langgraph.app/runs/invoke \
  -H "X-API-Key: your-langsmith-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [{"role": "human", "content": "I need a website"}],
      "contact_id": "test-123",
      "conversation_id": null
    }
  }'
```

## Webhook Integration

### Option 1: Direct Webhook to LangGraph Cloud

Configure your GHL webhook to:
```
https://your-deployment-id.langgraph.app/webhooks/ghl
```

Add headers:
- `X-API-Key: your-langsmith-api-key`

### Option 2: Webhook Proxy (Recommended)

Deploy a lightweight webhook handler (like AWS Lambda) that:
1. Receives webhooks from GHL/Meta
2. Transforms the payload
3. Forwards to LangGraph Cloud

Example using Vercel:

```javascript
// api/webhook/ghl.js
export default async function handler(req, res) {
  const { contactId, conversationId, message } = req.body;
  
  const response = await fetch('https://your-deployment.langgraph.app/runs/invoke', {
    method: 'POST',
    headers: {
      'X-API-Key': process.env.LANGSMITH_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      input: {
        messages: [{ role: 'human', content: message.body }],
        contact_id: contactId,
        conversation_id: conversationId
      }
    })
  });
  
  const result = await response.json();
  res.json(result);
}
```

## Monitoring

### View Runs in LangSmith

1. Go to https://smith.langchain.com
2. Navigate to your project
3. View all conversation runs
4. Debug and trace execution

### Check Logs

```bash
langgraph logs --deployment-id your-deployment-id
```

### Update Deployment

After making changes:

```bash
langgraph deploy --update --deployment-id your-deployment-id
```

## Production Considerations

### 1. Scaling
- LangGraph Cloud auto-scales based on load
- Consider rate limits from GHL API
- Monitor token usage

### 2. Error Handling
- Set up alerts in LangSmith
- Implement webhook retry logic
- Add fallback responses

### 3. Security
- Use environment variables for all secrets
- Implement webhook signature verification
- Enable CORS if needed

### 4. Cost Optimization
- Monitor LLM token usage
- Use streaming for long responses
- Cache common queries

## Troubleshooting

### Common Issues

1. **Deployment fails**
   - Check langgraph.json syntax
   - Ensure all imports are correct
   - Verify Python version compatibility

2. **Webhooks not working**
   - Check API key in headers
   - Verify webhook URL format
   - Look at LangSmith traces

3. **Agent not responding correctly**
   - Check environment variables
   - Verify GHL API connection
   - Review system prompts

### Debug Commands

```bash
# Check deployment status
langgraph status --deployment-id your-deployment-id

# View environment variables
langgraph env list --deployment-id your-deployment-id

# Test specific thread
langgraph test --thread-id "ghl-contact-123"
```

## Next Steps

1. **Set up production webhooks** in GHL
2. **Configure Meta webhooks** for lead capture
3. **Monitor performance** in LangSmith
4. **Optimize prompts** based on real conversations
5. **Add custom tools** as needed

## Support

- LangGraph Docs: https://python.langchain.com/docs/langgraph
- LangSmith Support: support@langchain.com
- Community: https://github.com/langchain-ai/langgraph