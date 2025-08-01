# LangGraph Dev Server Guide

This guide explains how to use the LangGraph dev server for local development of the GHL agent.

## What's New

We've enhanced the project with:
1. **LangGraph CLI** - For easy local development and testing
2. **Enhanced Agent** - With memory, state tracking, and conversation stages
3. **Custom Webhook Routes** - Integrated with LangGraph server
4. **Dual Graph Support** - Both basic and enhanced versions

## Quick Start

### 1. Start the LangGraph Dev Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start the dev server
langgraph dev
```

The server will start at `http://localhost:8123` with:
- Full API endpoints (`/runs`, `/threads`, `/assistants`)
- Built-in PostgreSQL for state persistence
- Hot reload for development
- Custom webhook routes at `/webhook/ghl` and `/webhook/meta`

### 2. Test the Enhanced Agent

```bash
# Run the test script
python test_langgraph_dev.py
```

This will:
- Create a thread
- Send a test message
- Show the agent's response with state tracking

### 3. Test Webhooks

```bash
# Test GHL webhook
curl -X POST http://localhost:8123/webhook/ghl \
  -H "Content-Type: application/json" \
  -d '{
    "type": "InboundMessage",
    "locationId": "test-location",
    "contactId": "test-contact-123",
    "conversationId": "test-conversation",
    "message": {"body": "I need a website for my business"}
  }'

# Check webhook health
curl http://localhost:8123/webhooks/health
```

## Enhanced Features

### 1. Conversation Stages

The enhanced agent tracks conversation progress through stages:
- **greeting** - Welcome and initial contact
- **discovery** - Learn about project needs
- **qualification** - Check budget requirements ($5k minimum)
- **scheduling** - Book appointments for qualified leads
- **completed** - Wrap up the conversation

### 2. State Management

The agent now tracks:
```python
{
    "contact_id": "...",
    "conversation_stage": "qualification",
    "is_qualified": false,
    "budget": 3000,
    "project_type": "website",
    "appointment_scheduled": false
}
```

### 3. Memory & Persistence

- Conversations are saved per contact
- State persists between messages
- Thread-based conversation history

### 4. Intelligent Routing

The agent automatically:
- Extracts budget from messages
- Determines qualification status
- Routes to appropriate conversation stage
- Books appointments when qualified

## API Endpoints

### Core LangGraph Endpoints

- `GET /` - API documentation
- `GET /ok` - Health check
- `GET /info` - Server information
- `POST /runs` - Create a new run
- `GET /threads/{thread_id}` - Get thread state
- `POST /threads` - Create a new thread

### Custom Webhook Endpoints

- `GET /webhook/meta` - Meta webhook verification
- `POST /webhook/meta` - Process Meta leads
- `POST /webhook/ghl` - Process GHL messages
- `GET /webhooks/health` - Webhook health status

## Development Workflow

### 1. Modify the Agent

Edit `ghl_agent/agent/enhanced_graph.py` to:
- Adjust conversation flow
- Add new tools
- Change qualification criteria
- Enhance state tracking

### 2. Test Changes

The dev server auto-reloads, so just:
```bash
# Send a test message
curl -X POST http://localhost:8123/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "ghl_agent",
    "input": {
      "messages": [{"role": "human", "content": "Your test message"}],
      "contact_id": "test-123"
    }
  }'
```

### 3. View Threads

```bash
# List all threads
curl http://localhost:8123/threads

# Get specific thread state
curl http://localhost:8123/threads/ghl-test-123
```

## Switching Between Agents

We have two agents available:
- `ghl_agent` - Enhanced version with memory and stages
- `basic_agent` - Original simple version

Use different agents:
```json
{
  "assistant_id": "basic_agent",  // or "ghl_agent"
  "input": {...}
}
```

## Configuration

### Environment Variables

Create a `.env` file:
```env
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...

GHL_API_KEY=your-ghl-key
GHL_LOCATION_ID=your-location
GHL_CALENDAR_ID=your-calendar

# Optional
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_TRACING_V2=true
```

### LangGraph Configuration

The `langgraph.json` file configures:
- Available graphs
- Environment variables
- Custom HTTP routes
- Python version

## Debugging

### 1. Enable Debug Logging

```bash
# Start with debug logging
LANGGRAPH_LOG_LEVEL=debug langgraph dev
```

### 2. View LangSmith Traces

If you have LangSmith configured:
1. Go to https://smith.langchain.com
2. Find your project
3. View detailed traces of each run

### 3. Inspect State

```python
# In your code, print state
print(f"Current state: {json.dumps(state, indent=2)}")
```

## Production Deployment

When ready for production:

```bash
# Build Docker image
langgraph build -t ghl-agent:latest

# Deploy to LangGraph Cloud
langgraph deploy --name "ghl-customer-agent"
```

## Troubleshooting

### Port Already in Use

If port 8123 is busy:
```bash
langgraph dev --port 8124
```

### Database Issues

The dev server manages its own PostgreSQL. If issues:
```bash
# Stop all containers
docker ps -q | xargs docker stop

# Restart
langgraph dev
```

### Import Errors

Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. **Test the enhanced agent** with various scenarios
2. **Customize the conversation flow** for your needs
3. **Add more tools** as required
4. **Deploy to production** when ready

The LangGraph dev server provides a complete development environment with persistence, debugging, and easy testing - making it much easier to build and iterate on your agent!