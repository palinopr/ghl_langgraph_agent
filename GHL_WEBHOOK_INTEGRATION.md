# GHL Webhook Integration Guide

## Webhook Format

Your GHL webhook sends data in this format:
```json
{
  "id": "{{contact.id}}",
  "name": "{{contact.name}}",
  "email": "{{contact.email}}",
  "phone": "{{contact.phone}}",
  "message": "{{message.body}}"
}
```

## Updated System Components

### 1. Models (`ghl_agent/models.py`)
Updated `GHLWebhookPayload` to match your format:
```python
class GHLWebhookPayload(BaseModel):
    id: str  # contact.id
    name: Optional[str] = None  # contact.name
    email: Optional[str] = None  # contact.email
    phone: Optional[str] = None  # contact.phone
    message: str  # message.body
```

### 2. Webhook Handler (`ghl_agent/webhooks/handlers.py`)
- Updated to use `id` as the contact identifier
- Stores contact info (name, email, phone) in the response
- No longer expects `type`, `locationId`, or `conversationId`

### 3. Custom App (`ghl_agent/custom_app.py`)
- Updated to pass contact info to the agent state
- Creates threads using the contact ID
- Stores contact metadata in thread creation

## Setting Up in GoHighLevel

### 1. Create Webhook in GHL
1. Go to **Settings** → **Webhooks**
2. Click **Add Webhook**
3. Configure:
   - **Name**: Battery Consultation Bot
   - **URL**: `https://your-domain.com/webhook/ghl`
   - **Events**: Select "Message Received" or "SMS Received"

### 2. Set Webhook Payload
Use this exact template in GHL:
```json
{
  "id": "{{contact.id}}",
  "name": "{{contact.name}}",
  "email": "{{contact.email}}",
  "phone": "{{contact.phone}}",
  "message": "{{message.body}}"
}
```

### 3. Test the Integration

#### Local Testing
```bash
# Start the server
python -m ghl_agent.main

# Test with curl
curl -X POST http://localhost:8000/webhook/ghl \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test-contact-123",
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "787-555-1234",
    "message": "Hola, necesito información sobre baterías"
  }'
```

#### Test Endpoint
Visit: `POST http://localhost:8000/test/ghl-webhook`

This will simulate a GHL webhook with test data.

## Agent State Integration

The agent now receives contact information in the initial state:
- `contact_id`: From webhook `id`
- `customer_name`: From webhook `name`
- `customer_phone`: From webhook `phone`
- `customer_email`: From webhook `email`

This means the agent already has contact info when asking for consultation details!

## Benefits of New Format

1. **Simpler Integration**: Direct mapping of GHL contact fields
2. **Contact Info Available**: Agent has name/phone/email from the start
3. **Cleaner Payload**: Only essential fields, no nested objects
4. **Better for Battery Consultation**: Can skip asking for contact info if already provided

## Conversation Flow Update

Since contact info might already be available:

1. **If contact info exists**: Skip directly to scheduling
   ```
   "Hola Juan! Veo que estás interesado en nuestros sistemas de baterías. 
   ¿Te gustaría agendar una consulta gratuita?"
   ```

2. **If contact info missing**: Follow normal flow
   ```
   "Para agendar tu consulta, necesito tu nombre completo, teléfono y email."
   ```

## Troubleshooting

### Webhook Not Triggering
1. Check GHL webhook is active
2. Verify URL is correct and publicly accessible
3. Check webhook events are properly selected

### Missing Contact Info
- GHL might not always send all fields
- Agent handles missing fields gracefully
- Can still collect info during conversation

### Testing Production
```bash
# Monitor logs
tail -f logs/webhook.log

# Check webhook health
curl https://your-domain.com/webhooks/health
```

## Next Steps

1. Deploy the updated agent
2. Configure GHL webhook with your domain
3. Test with real messages
4. Monitor conversations in LangSmith