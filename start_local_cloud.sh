#!/bin/bash
# Start LangGraph in local development mode that mimics cloud deployment

echo "🚀 Starting LangGraph Local Cloud Environment"
echo "============================================"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if langgraph CLI is installed
if ! command -v langgraph &> /dev/null; then
    echo "❌ langgraph CLI not found!"
    echo "Install with: pip install -U 'langgraph-cli[inmem]'"
    exit 1
fi

# Display configuration
echo ""
echo "📋 Configuration:"
echo "   - Port: 2024 (default)"
echo "   - API URL: http://localhost:2024"
echo "   - Studio URL: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024"
echo "   - Config: langgraph.json"
echo "   - Environment: .env"
echo ""

# Parse command line arguments
TUNNEL=false
DEBUG=false
PORT=2024

while [[ $# -gt 0 ]]; do
    case $1 in
        --tunnel)
            TUNNEL=true
            shift
            ;;
        --debug)
            DEBUG=true
            shift
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--tunnel] [--debug] [--port PORT]"
            exit 1
            ;;
    esac
done

# Build command
CMD="langgraph dev"

if [ "$PORT" != "2024" ]; then
    CMD="$CMD --port $PORT"
fi

if [ "$TUNNEL" = true ]; then
    echo "🌐 Enabling tunnel for remote access..."
    CMD="$CMD --tunnel"
fi

if [ "$DEBUG" = true ]; then
    echo "🐛 Enabling debug mode..."
    export LANGGRAPH_LOG_LEVEL=debug
    export LOG_COLOR=true
fi

echo "📝 Starting with command: $CMD"
echo ""
echo "🔗 Available endpoints:"
echo "   - Health: http://localhost:$PORT/health"
echo "   - Info: http://localhost:$PORT/info"
echo "   - Assistants: http://localhost:$PORT/assistants"
echo "   - Runs: http://localhost:$PORT/runs/stream"
echo "   - Threads: http://localhost:$PORT/threads"
echo "   - Webhooks: http://localhost:$PORT/webhook/ghl"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================"
echo ""

# Start the server
exec $CMD