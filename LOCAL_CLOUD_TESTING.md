# Local Cloud Testing Guide

This guide explains how to test your LangGraph deployment locally with 1:1 parity to cloud deployment.

## 🚀 Quick Start

### 1. Start Local Server

```bash
# Basic start
./start_local_cloud.sh

# With tunnel for remote access
./start_local_cloud.sh --tunnel

# With debug logging
./start_local_cloud.sh --debug

# Custom port
./start_local_cloud.sh --port 3000
```

### 2. Run Tests

In another terminal:

```bash
# Run comprehensive test suite
python test_local_as_cloud.py

# Test specific deployment features
python test_langsmith_cloud.py  # Change URL to http://localhost:2024
```

## 📋 What Gets Tested

### 1. **Threadless Runs** (Stateless)
- Single message processing
- No state persistence between calls
- Same as cloud deployment threadless mode

### 2. **Thread Runs** (Stateful)
- Conversation state persistence
- Multiple messages in same thread
- State management across messages

### 3. **REST API Endpoints**
- `/health` - Server health check
- `/info` - Deployment information
- `/assistants` - List available assistants
- `/runs/stream` - Streaming runs
- `/threads` - Thread management

### 4. **Custom Webhooks**
- `/webhook/ghl` - GHL webhook handler
- `/webhook/meta` - Meta webhook handler
- Same routing as cloud deployment

## 🔧 Configuration

### Environment Variables

The local server uses the same `.env` file as cloud deployment:

```env
# Required
GHL_API_KEY=your_key
GHL_LOCATION_ID=your_location
GHL_CALENDAR_ID=your_calendar
OPENAI_API_KEY=your_key

# Optional
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=false  # Disable for local testing
```

### LangGraph Configuration

Same `langgraph.json` works locally and in cloud:

```json
{
  "python_version": "3.11",
  "dependencies": ["./"],
  "graphs": {
    "ghl_agent": {
      "path": "./ghl_agent/agent/graph.py:graph"
    }
  },
  "env": ".env",
  "http": {
    "app": "./ghl_agent/custom_app.py:app"
  },
  "crons": [...]
}
```

## 🎯 Testing Scenarios

### 1. Basic Conversation Flow

```python
# Test Spanish conversation
messages = [
    "Hola, necesito baterías",
    "Vivo en una casa",
    "Quiero nevera y luces"
]
```

### 2. Tool Execution

```python
# Test GHL tools
- send_ghl_message
- get_conversation_messages
- book_ghl_appointment
```

### 3. Memory Persistence

```python
# Test state management
- Customer preferences
- Conversation history
- Equipment calculations
```

### 4. Error Handling

```python
# Test resilience
- Invalid inputs
- Tool failures
- Retry logic
```

## 🔍 Debugging

### 1. Enable Debug Logging

```bash
export LANGGRAPH_LOG_LEVEL=debug
export LOG_COLOR=true
./start_local_cloud.sh --debug
```

### 2. Use LangGraph Studio

Open in browser:
```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

Features:
- Visual graph debugging
- Real-time state inspection
- Message flow visualization
- Tool execution tracking

### 3. Check Logs

```bash
# Server logs appear in terminal
# Look for:
- Incoming requests
- Tool executions
- State updates
- Error messages
```

## 🌐 Tunnel Testing

For testing webhooks from external services:

```bash
./start_local_cloud.sh --tunnel
```

This creates a public HTTPS URL like:
```
https://abc123.tunnels.langgraph.app
```

Use this URL for:
- GHL webhook configuration
- Meta webhook testing
- Mobile app testing
- Sharing with team

## 📊 Monitoring

### Local Metrics

The `/info` endpoint provides:
```json
{
  "version": "0.2.119",
  "assistants": true,
  "crons": true,
  "flags": {
    "langsmith": true
  }
}
```

### State Inspection

Check thread state:
```python
state = await client.threads.get_state(thread_id)
print(state['values'])  # Full state dump
```

## ✅ Pre-Deployment Checklist

Before deploying to cloud, ensure:

- [ ] All tests pass locally
- [ ] Conversation flow works end-to-end
- [ ] Tools execute correctly
- [ ] Error handling is robust
- [ ] Memory persistence works
- [ ] Webhooks respond correctly
- [ ] Performance is acceptable

## 🚀 Deploy to Cloud

Once local testing is complete:

```bash
# Deploy to LangGraph Cloud
langgraph deploy \
  --name "ghl-customer-agent" \
  --github-repo "yourusername/ghl_langgraph_agent" \
  --branch "main"
```

## 🔄 Local vs Cloud Comparison

| Feature | Local Dev | Cloud Deployment |
|---------|-----------|------------------|
| API Endpoints | ✅ Same | ✅ Same |
| Thread State | ✅ In-memory | ✅ Persistent |
| Webhooks | ✅ Available | ✅ Available |
| Cron Jobs | ❌ Not in dev | ✅ Scheduled |
| Scaling | ❌ Single instance | ✅ Auto-scale |
| Public URL | ✅ Via tunnel | ✅ Always |
| Monitoring | 🟡 Basic | ✅ Full |

## 🛠️ Troubleshooting

### Server Won't Start
- Check Python version (3.11+)
- Verify `langgraph-cli` is installed
- Check port availability

### Tests Fail
- Ensure server is running
- Check environment variables
- Verify assistant ID matches

### State Not Persisting
- Local uses in-memory store
- Restart clears all state
- Use threads for stateful testing

## 📚 Additional Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangSmith SDK](https://github.com/langchain-ai/langsmith-sdk)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Cloud Testing Guide](./CLOUD_TESTING_GUIDE.md)