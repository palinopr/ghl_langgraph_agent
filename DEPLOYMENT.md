# LangGraph Cloud Deployment Guide

This guide will help you deploy the GHL LangGraph Agent to LangGraph Cloud (Smith).

## Prerequisites

1. **LangSmith Account**: Sign up at [smith.langchain.com](https://smith.langchain.com)
2. **LangGraph CLI**: Install the deployment CLI
3. **GitHub Repository**: Your code should be in the GitHub repo
4. **API Keys Ready**: Have all your API keys ready for configuration

## Step 1: Install LangGraph CLI

```bash
pip install -U langgraph-cli
```

## Step 2: Authenticate with LangSmith

```bash
langgraph auth
```

This will open a browser window for authentication. Log in with your LangSmith account.

## Step 3: Prepare Your Repository

1. **Push your code to GitHub**:
```bash
git add .
git commit -m "Initial commit for LangGraph deployment"
git push origin main
```

2. **Verify langgraph.json**: The file is already configured with:
   - Python version 3.11
   - Required dependencies
   - Graph location: `src/agent/graph.py:graph`
   - Environment variables configuration

## Step 4: Deploy to LangGraph Cloud

### Option A: Deploy from GitHub (Recommended)

```bash
langgraph deploy --name "ghl-customer-agent" \
  --github-repo "palinopr/ghl_langgraph_agent" \
  --branch "main"
```

### Option B: Deploy from Local Directory

```bash
langgraph deploy --name "ghl-customer-agent"
```

## Step 5: Configure Environment Variables

After deployment, you'll need to set your environment variables in LangGraph Cloud:

1. Go to your deployment in the LangSmith UI
2. Navigate to the "Environment" tab
3. Set the following variables:

**Required Variables**:
- `OPENAI_API_KEY`: Your OpenAI API key
- `GHL_API_KEY`: Your GoHighLevel API key
- `GHL_LOCATION_ID`: Your GHL location ID
- `GHL_CALENDAR_ID`: Your GHL calendar ID

**Optional Variables**:
- `GHL_API_BASE_URL`: Default is `https://services.leadconnectorhq.com`
- `META_VERIFY_TOKEN`: For Meta webhook verification
- `META_APP_SECRET`: For Meta webhook signature verification
- `TIMEZONE`: Default is `America/New_York`

## Step 6: Set Up Webhooks

Once deployed, you'll get a LangGraph Cloud endpoint URL. Use this to configure your webhooks:

### GHL Webhook Configuration

1. In GoHighLevel, go to Settings → Webhooks
2. Create a new webhook with:
   - **URL**: `https://your-deployment.langraph.app/webhooks/ghl`
   - **Events**: 
     - Inbound Message
     - Conversation Started

### Meta Webhook Configuration

1. In Meta Business Manager, go to your app settings
2. Add webhook with:
   - **URL**: `https://your-deployment.langraph.app/webhooks/meta`
   - **Verify Token**: Use the value you set in `META_VERIFY_TOKEN`
   - **Subscribe to**: `leadgen` field

## Step 7: Test Your Deployment

### Test the Agent Directly

```bash
curl -X POST https://your-deployment.langraph.app/invoke \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_LANGSMITH_API_KEY" \
  -d '{
    "input": {
      "messages": [{"role": "human", "content": "I need a website"}],
      "contact_id": "test-123",
      "conversation_id": null
    }
  }'
```

### Monitor in LangSmith

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Navigate to your project
3. View traces and logs for debugging

## Deployment Commands Reference

### View Deployment Status
```bash
langgraph status --name "ghl-customer-agent"
```

### View Logs
```bash
langgraph logs --name "ghl-customer-agent"
```

### Update Deployment
```bash
langgraph update --name "ghl-customer-agent"
```

### Delete Deployment
```bash
langgraph delete --name "ghl-customer-agent"
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are in `requirements.txt`
2. **Environment Variables**: Double-check all required variables are set
3. **Webhook Verification**: Check logs for webhook signature validation errors
4. **API Rate Limits**: Monitor your API usage in both OpenAI and GHL

### Debug Mode

Enable debug logging by setting:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ghl-langgraph-agent-debug
```

## Production Considerations

1. **Scaling**: LangGraph Cloud automatically scales your deployment
2. **Monitoring**: Set up alerts in LangSmith for errors
3. **Backup**: Keep your environment variables backed up securely
4. **Updates**: Use GitHub Actions for automated deployments (see below)

## GitHub Actions Deployment (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to LangGraph Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install LangGraph CLI
        run: pip install -U langgraph-cli
      
      - name: Deploy
        env:
          LANGSMITH_API_KEY: ${{ secrets.LANGSMITH_API_KEY }}
        run: |
          langgraph deploy --name "ghl-customer-agent" \
            --api-key $LANGSMITH_API_KEY
```

## Support

For issues specific to:
- **LangGraph Cloud**: Contact LangChain support
- **GHL Integration**: Check GHL API documentation
- **Agent Logic**: Review the code in `src/agent/graph.py`

## Next Steps

1. Test your webhook integrations thoroughly
2. Monitor agent conversations in LangSmith
3. Adjust the agent prompts based on performance
4. Set up error alerting for production