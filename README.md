# GHL LangGraph Agent

AI-powered customer service agent that integrates Meta leads with GoHighLevel using LangGraph. Automatically qualifies leads and schedules appointments.

## Features

- **Meta Lead Integration**: Automatically captures and processes leads from Meta (Facebook/Instagram) lead ads
- **Intelligent Conversations**: Uses LangGraph to create context-aware conversations
- **Lead Qualification**: Automatically qualifies leads based on budget and requirements
- **Appointment Scheduling**: Books appointments directly in GHL for qualified leads
- **GHL Conversation History**: Fetches conversation context directly from GoHighLevel
- **Error Recovery**: Built-in retry logic and graceful error handling

## Architecture

```
Webhook → LangGraph Agent → GHL API → Customer
  ↓            ↓              ↓
Meta/GHL   AI Processing   Message/Booking
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required configurations:
- **GHL_API_KEY**: Your GoHighLevel API key
- **GHL_LOCATION_ID**: Your GHL location ID
- **META_VERIFY_TOKEN**: Token for Meta webhook verification
- **META_APP_SECRET**: Secret for Meta webhook signature verification
- **ANTHROPIC_API_KEY** or **OPENAI_API_KEY**: LLM provider credentials
- **LANGCHAIN_API_KEY**: For LangSmith tracing (optional but recommended)

### 3. Run the Server

```bash
python -m src.main
```

The server will start on `http://localhost:8000`

## Webhook Configuration

### Meta Webhook

1. In your Meta App settings, add the webhook URL:
   ```
   https://your-domain.com/webhook/meta
   ```

2. Subscribe to the `leadgen` field

3. Use the verify token from your `.env` file

### GHL Webhook

1. In GHL, create a webhook for incoming messages:
   ```
   https://your-domain.com/webhook/ghl
   ```

2. Set trigger events:
   - Inbound Message
   - Conversation Started

## API Endpoints

### Health Check
```
GET /
```

### Meta Webhook
```
GET /webhook/meta  # Verification
POST /webhook/meta # Lead events
```

### GHL Webhook
```
POST /webhook/ghl  # Message events
```

### Test Endpoint
```
POST /test/conversation
{
  "contact_id": "test-123",
  "message": "I need help with a website"
}
```

## Conversation Flow

1. **Greeting Stage**: Welcome new leads
2. **Discovery Stage**: Understand project needs
3. **Qualification Stage**: Check budget (min $5,000) and timeline
4. **Scheduling Stage**: Book appointments for qualified leads
5. **Completion**: Confirm appointment or provide alternatives

## Tools Available

- `send_ghl_message`: Send messages via GHL
- `get_ghl_contact_info`: Retrieve contact details
- `update_ghl_contact`: Update contact information
- `get_available_calendar_slots`: Check calendar availability
- `book_ghl_appointment`: Schedule appointments

## Customization

### Modify Conversation Flow

Edit `src/agent/prompts.py` to customize:
- System prompts
- Stage-specific guidance
- Qualification criteria
- Error messages

### Add New Tools

Create new tools in `src/tools/` and add them to the `GHL_TOOLS` list.

### Extend Agent Logic

Modify `src/agent/graph.py` to:
- Add new conversation stages
- Implement custom routing logic
- Enhance data extraction
- Add new node types

## Monitoring

Enable LangSmith tracing by setting:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=ghl-langgraph-agent
```

View traces at: https://smith.langchain.com

## Production Deployment

### Option 1: LangGraph Cloud (Recommended)

Deploy to LangGraph Cloud for managed, scalable hosting:

```bash
# Install CLI
pip install -U langgraph-cli

# Deploy
langgraph deploy --name "ghl-customer-agent"
```

See [LANGGRAPH_DEPLOYMENT.md](./LANGGRAPH_DEPLOYMENT.md) for detailed instructions.

### Option 2: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
CMD ["python", "-m", "src.main"]
```

### Environment Variables

Set all required environment variables in your deployment platform.

### SSL/TLS

Ensure your webhook endpoints use HTTPS in production.

## Troubleshooting

### Common Issues

1. **Webhook Verification Failing**
   - Check verify token matches
   - Ensure endpoint returns challenge parameter

2. **Messages Not Sending**
   - Verify GHL API key and permissions
   - Check contact_id is valid
   - Review logs for API errors

3. **Agent Not Responding**
   - Check LLM API keys are valid
   - Verify LangGraph is properly initialized
   - Review conversation state in logs

### Debug Mode

Set logging level in code:
```python
structlog.configure(
    processors=[...],
    level="DEBUG"
)
```

## License

MIT