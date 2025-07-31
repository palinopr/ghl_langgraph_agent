#!/bin/bash

# LangGraph Cloud Deployment Script

echo "🚀 Deploying GHL LangGraph Agent to LangGraph Cloud"
echo "=================================================="

# Check if LANGSMITH_API_KEY is set
if [ -z "$LANGSMITH_API_KEY" ]; then
    echo "❌ Error: LANGSMITH_API_KEY environment variable is not set"
    echo "Please set it with: export LANGSMITH_API_KEY=your_key_here"
    exit 1
fi

# Install LangGraph CLI if not installed
if ! command -v langgraph &> /dev/null; then
    echo "📦 Installing LangGraph CLI..."
    pip install -U langgraph-cli
fi

echo "📋 Using configuration:"
echo "  - Repository: palinopr/ghl_langgraph_agent"
echo "  - Branch: main"
echo "  - Project Name: ghl-customer-agent"

# Deploy from GitHub
echo "🏗️ Starting deployment..."
langgraph deploy \
    --name "ghl-customer-agent" \
    --github-repo "palinopr/ghl_langgraph_agent" \
    --branch "main" \
    --api-key "$LANGSMITH_API_KEY"

echo "✅ Deployment initiated!"
echo ""
echo "📝 Next steps:"
echo "1. Go to https://smith.langchain.com to view your deployment"
echo "2. Set environment variables in the LangSmith UI:"
echo "   - OPENAI_API_KEY"
echo "   - GHL_API_KEY"
echo "   - GHL_LOCATION_ID"
echo "   - GHL_CALENDAR_ID"
echo "3. Configure webhooks with your deployment URL"
echo ""
echo "🔍 To check deployment status:"
echo "   langgraph status --name 'ghl-customer-agent'"