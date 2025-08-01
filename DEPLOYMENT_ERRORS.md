# Deployment Error Handling Guide

## Common Deployment Issues

### 1. RetryError in WhatsApp Messages

**Symptom**: `Failed to send message: RetryError[<Future at 0x... state=finished raised HTTPStatusError>]`

**Cause**: Network timeouts or slower response times in deployment environment vs local.

**Solutions**:

1. **Environment Variables** (set in deployment):
   ```env
   GHL_TIMEOUT_SECONDS=60      # Increase timeout (default: 30 local, 60 deployment)
   GHL_RETRY_ATTEMPTS=5        # Increase retry attempts (default: 3)
   ```

2. **Monitor Logs**: The improved error handling will now show:
   - Actual HTTP status codes
   - Response body for failed requests
   - Which retry attempt failed

### 2. Duplicate Traces in LangSmith

**This is normal behavior!** You see two traces because:
1. First trace: Agent deciding to use the tool
2. Second trace: Tool execution

This shows the complete flow: Agent → Tool Decision → Tool Execution

### 3. Deployment vs Local Differences

| Aspect | Local | Deployment |
|--------|-------|------------|
| Network | Fast, reliable | May have latency |
| Timeout | 30 seconds | 60 seconds (configurable) |
| Retries | 3 attempts | 3 attempts (configurable) |
| Error visibility | Console logs | LangSmith traces + logs |

### 4. Debugging Tips

1. **Check deployment logs**:
   ```bash
   langgraph logs --name "your-deployment-name"
   ```

2. **Test API directly** from deployment environment:
   ```python
   # Create a test endpoint in custom_app.py
   @app.get("/test/ghl-api")
   async def test_ghl_api():
       # Test GHL API connectivity
   ```

3. **Use environment-specific configuration**:
   - Local: Fast timeouts, fewer retries
   - Deployment: Longer timeouts, more retries

### 5. Best Practices

1. **Always log contact IDs** in errors for debugging
2. **Use structured logging** (already implemented)
3. **Return user-friendly messages** when retries fail
4. **Monitor rate limits** in GHL API responses
5. **Set appropriate timeouts** based on your network conditions

## Configuration Reference

```env
# Required
GHL_API_KEY=your-api-key
GHL_LOCATION_ID=your-location-id

# Optional (with defaults)
GHL_TIMEOUT_SECONDS=60     # API timeout in seconds
GHL_RETRY_ATTEMPTS=3       # Number of retry attempts
```