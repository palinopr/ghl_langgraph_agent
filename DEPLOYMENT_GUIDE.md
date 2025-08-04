# GHL Agent Deployment Guide

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Configuration](#configuration)
3. [Local Development](#local-development)
4. [Cloud Deployment](#cloud-deployment)
5. [Cron Jobs](#cron-jobs)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Tools
- Python 3.11+
- Git
- LangGraph CLI: `pip install -U langgraph-cli`
- LangSmith Plus account (for cloud deployment)

### Required API Keys
- **GHL_API_KEY**: GoHighLevel API key
- **GHL_LOCATION_ID**: Your GHL location ID
- **GHL_CALENDAR_ID**: Calendar ID for booking
- **LANGSMITH_API_KEY**: For tracing and deployment
- **OPENAI_API_KEY** or **ANTHROPIC_API_KEY**: For LLM

### Optional API Keys
- **META_VERIFY_TOKEN**: For Meta webhook verification
- **META_APP_SECRET**: For Meta lead ads
- **REDIS_URL**: For production memory store
- **POSTGRES_URI**: For production persistence

## ⚙️ Configuration

### 1. Environment Variables

Create a `.env` file:
```bash
# Required
GHL_API_KEY=your_ghl_api_key
GHL_LOCATION_ID=your_location_id
GHL_CALENDAR_ID=your_calendar_id
LANGSMITH_API_KEY=your_langsmith_key
OPENAI_API_KEY=your_openai_key

# Optional
META_VERIFY_TOKEN=your_meta_token
META_APP_SECRET=your_meta_secret
REDIS_URL=redis://localhost:6379
POSTGRES_URI=postgresql://user:pass@localhost/db
```

### 2. Agent Configuration

Edit `ghl_agent/config.yaml`:
```yaml
business:
  name: "Your Business Name"
  email: "your@email.com"
  phone: "+1234567890"
  timezone: "America/New_York"
  language: "es"

qualification:
  min_budget: 5000
  # ... other settings
```

### 3. Cron Schedule

Edit `langgraph.json` to customize cron jobs:
```json
"crons": [
  {
    "schedule": "*/15 * * * *",  // Every 15 minutes
    "graph_id": "ghl_agent",
    "input": {
      "task": "check_new_leads",
      "minutes_since": 20
    }
  }
]
```

## 🏠 Local Development

### Quick Start
```bash
# Install dependencies
pip install -e .

# Run local server
python scripts/deploy.py --mode local

# Or use langgraph directly
langgraph dev
```

### Test Local Deployment
```bash
# In another terminal
python test_deployment.py --local

# Or test specific conversation
curl -X POST http://localhost:2024/runs/stream \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "ghl_agent",
    "input": {
      "messages": [{"role": "human", "content": "Necesito baterías"}],
      "contact_id": "test-123"
    }
  }'
```

## ☁️ Cloud Deployment

### Method 1: Using Deploy Script
```bash
# Deploy to LangGraph Cloud
python scripts/deploy.py --mode cloud \
  --name "ghl-customer-agent" \
  --github-repo "yourusername/ghl_langgraph_agent" \
  --branch "main"
```

### Method 2: Using LangGraph CLI
```bash
# Authenticate first
langgraph auth

# Deploy from GitHub
langgraph deploy \
  --name "ghl-customer-agent" \
  --github-repo "yourusername/ghl_langgraph_agent" \
  --branch "main"
```

### Method 3: Via LangSmith UI
1. Go to [LangSmith Deployments](https://smith.langchain.com/deployments)
2. Click "New Deployment"
3. Connect your GitHub repository
4. Configure environment variables
5. Deploy

### Post-Deployment Setup

1. **Get Deployment URL**
   ```bash
   # From deployment output or LangSmith UI
   https://your-deployment.us.langgraph.app
   ```

2. **Configure Webhooks**
   - GHL Webhook: `https://your-deployment.us.langgraph.app/webhook/ghl`
   - Meta Webhook: `https://your-deployment.us.langgraph.app/webhook/meta`

3. **Test Deployment**
   ```bash
   python test_deployment.py \
     --url "https://your-deployment.us.langgraph.app"
   ```

## ⏰ Cron Jobs

### Automatic Setup (Cloud)
Cron jobs are automatically configured from `langgraph.json` during deployment.

### Manual Testing
```bash
# Test cron job locally
python scripts/setup_cron.py --test \
  --url "https://your-deployment.us.langgraph.app"
```

### Available Cron Tasks

1. **Lead Checking** (Every 15 minutes)
   - Checks for new leads from various sources
   - Applies triage rules
   - Auto-responds to qualified leads

2. **Daily Summary** (9 AM daily)
   - Sends summary of leads processed
   - Reports conversion metrics
   - Highlights issues needing attention

## 📊 Monitoring

### LangSmith Tracing
1. All conversations are automatically traced
2. View traces at [smith.langchain.com](https://smith.langchain.com)
3. Filter by deployment name

### Metrics to Track
- Response time per conversation
- Lead qualification rate
- Appointment booking success
- Error rates by type
- Cron job execution status

### Alerts
Configure alerts in LangSmith for:
- High error rates
- Failed cron jobs
- Slow response times
- Budget threshold breaches

## 🔧 Troubleshooting

### Common Issues

#### 1. "Configuration validation failed"
- Check all required environment variables
- Verify `config.yaml` syntax
- Ensure file paths are correct

#### 2. "Failed to send GHL message"
- Verify GHL API key permissions
- Check contact_id exists in GHL
- Review API rate limits

#### 3. "Webhook not receiving data"
- Verify webhook URL is correct
- Check webhook signatures
- Review server logs

#### 4. "Cron job not running"
- Check cron schedule syntax
- Verify deployment is active
- Review cron logs in LangSmith

### Debug Mode

Enable debug logging:
```yaml
# In config.yaml
logging:
  level: "DEBUG"
```

### View Logs

**Local:**
```bash
# Real-time logs
langgraph dev --verbose
```

**Cloud:**
```bash
# Via LangSmith UI or API
curl https://your-deployment.us.langgraph.app/logs
```

## 🚀 Production Checklist

- [ ] All environment variables configured
- [ ] Memory store configured (Redis/Postgres)
- [ ] Webhooks tested and verified
- [ ] Cron jobs scheduled and tested
- [ ] Error alerts configured
- [ ] Backup deployment ready
- [ ] Rate limits configured
- [ ] SSL certificates valid
- [ ] Monitoring dashboards set up
- [ ] Runbook documented

## 📝 Maintenance

### Update Deployment
```bash
# Push changes to GitHub
git add .
git commit -m "Update agent logic"
git push

# Deployment auto-updates or manually trigger
langgraph deploy --name "ghl-customer-agent"
```

### Backup Configuration
```bash
# Backup important files
cp .env .env.backup
cp ghl_agent/config.yaml config.yaml.backup
```

### Scale Deployment
- Adjust worker count in LangSmith UI
- Configure auto-scaling rules
- Monitor resource usage

## 🆘 Support

- **LangChain Discord**: For LangGraph questions
- **GitHub Issues**: For bug reports
- **LangSmith Support**: For deployment issues