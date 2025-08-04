# Agent Inbox Guide

## Overview

The Agent Inbox provides a web-based UI for monitoring and managing conversations handled by the GHL Battery Consultation Agent. It offers real-time metrics, conversation tracking, and insights from the reflection system.

## Features

### 1. **Conversation Monitoring**
- View all active conversations in real-time
- See customer details, housing type, and equipment lists
- Track conversation progress and stages
- Monitor sentiment analysis from reflection graphs

### 2. **Metrics Dashboard**
- Total conversations count
- Completed appointments
- Qualified leads
- Conversion rate percentage

### 3. **Reflection Insights**
- Automatic sentiment analysis (positive/neutral/negative)
- Key topics extraction
- Pain points identification
- Opportunity detection
- Recommended next actions

## Accessing the Inbox

### Local Development
```bash
# Start the local server
python -m langgraph dev

# Access the inbox at:
http://localhost:2024/inbox
```

### Cloud Deployment
```
https://your-deployment-url.langgraph.app/inbox
```

## API Endpoints

### Get Conversations
```http
GET /inbox/conversations?limit=20&status=new
```

Parameters:
- `limit`: Number of conversations to return (default: 20)
- `status`: Filter by status (all, new, in_progress, qualified, completed)

### Get Conversation Details
```http
GET /inbox/conversations/{contact_id}
```

Returns detailed information including:
- Full conversation history
- All reflection insights
- Customer preferences
- Progress tracking

### Get Metrics
```http
GET /inbox/metrics
```

Returns:
- Total conversations
- Completed appointments
- Qualified leads count
- Conversion rate
- Sentiment distribution
- Active conversations

### Search Conversations
```http
GET /inbox/search?query=casa
```

Search by:
- Customer name
- Housing type
- Equipment mentioned

### Flag Conversation
```http
POST /inbox/conversations/{contact_id}/flag
{
    "reason": "Needs human review"
}
```

## Reflection Graph Integration

The inbox automatically runs reflection analysis on conversations:

1. **Periodic Analysis**: Every 5 messages
2. **Stage-based Analysis**: At qualification and completion stages
3. **Insights Generated**:
   - Customer sentiment
   - Key discussion topics
   - Pain points
   - Sales opportunities
   - Recommended actions

## UI Features

### Conversation List
- Real-time updates every 30 seconds
- Sentiment indicators (colored dots)
- Status badges (New, In Progress, Qualified, Completed)
- Quick search functionality
- Filter by status tabs

### Conversation Details
- Progress bar showing completion percentage
- Full state information
- Reflection insights timeline
- Action recommendations
- Customer information summary

## Implementation Details

### Memory Storage
The inbox uses the same memory store as the agent:
- In-memory store for development
- PostgreSQL/Redis for production
- Namespaced storage for organization

### State Tracking
Conversations maintain:
- `housing_type`: casa/apartamento
- `equipment_list`: Array of equipment
- `customer_name`, `customer_phone`, `customer_email`
- `conversation_stage`: greeting/discovery/qualification/scheduling/completed
- `interested_in_consultation`: Boolean
- `appointment_scheduled`: Boolean

### Reflection Insights Storage
Insights are stored with:
- Timestamp of analysis
- Sentiment score
- Extracted topics and patterns
- Recommendations
- Next best action

## Troubleshooting

### No Conversations Showing
1. Check if the memory store is properly initialized
2. Verify conversations have been processed
3. Check browser console for API errors

### Metrics Not Loading
1. Ensure the `/inbox/metrics` endpoint is accessible
2. Check for CORS issues in deployment
3. Verify memory store connectivity

### UI Not Loading
1. Check if the app includes the inbox router
2. Verify the HTML template is being served
3. Check for JavaScript errors in console

## Future Enhancements

1. **Export Functionality**: Download conversation data as CSV
2. **Advanced Filtering**: Date ranges, sentiment filters
3. **Bulk Actions**: Process multiple conversations
4. **Real-time Updates**: WebSocket integration
5. **Analytics Dashboard**: Trend analysis and reporting
6. **Human Handoff**: Direct integration with support tools

## Security Considerations

1. **Authentication**: Add auth middleware for production
2. **Rate Limiting**: Implement API rate limits
3. **Data Privacy**: Ensure PII is properly handled
4. **Access Control**: Role-based permissions

---

The Agent Inbox provides comprehensive visibility into your battery consultation conversations, helping you monitor performance, identify opportunities, and ensure customer satisfaction.