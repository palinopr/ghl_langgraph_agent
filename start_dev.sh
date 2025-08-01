#!/bin/bash

echo "🚀 Starting GHL LangGraph Agent Development Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! pip show langgraph-cli > /dev/null 2>&1; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    pip install -U langgraph-cli
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  WARNING: No .env file found!"
    echo "Please create a .env file with your API keys:"
    echo ""
    echo "OPENAI_API_KEY=sk-..."
    echo "GHL_API_KEY=your-ghl-key"
    echo "GHL_LOCATION_ID=your-location-id"
    echo "GHL_CALENDAR_ID=your-calendar-id"
    echo ""
    echo "Press Enter to continue anyway or Ctrl+C to exit..."
    read
fi

# Start the dev server
echo ""
echo "🌟 Starting LangGraph dev server..."
echo "📍 Server will be available at: http://localhost:8123"
echo "📚 API docs: http://localhost:8123/docs"
echo ""
echo "Webhooks:"
echo "  - GHL: http://localhost:8123/webhook/ghl"
echo "  - Meta: http://localhost:8123/webhook/meta"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

langgraph dev