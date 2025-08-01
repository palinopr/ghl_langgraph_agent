"""Test if the setup is working correctly"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing Battery Consultation Agent Setup")
print("=" * 50)

# Check environment variables
env_vars = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    "GHL_API_KEY": os.getenv("GHL_API_KEY"),
    "GHL_LOCATION_ID": os.getenv("GHL_LOCATION_ID"),
    "LANGCHAIN_API_KEY": os.getenv("LANGCHAIN_API_KEY")
}

print("\n1. Environment Variables:")
for var, value in env_vars.items():
    status = "✓ Set" if value else "✗ Not set"
    print(f"   {var}: {status}")

# Check imports
print("\n2. Testing imports:")
try:
    from ghl_agent.agent.graph import graph, process_ghl_message
    print("   ✓ Agent graph imported successfully")
except Exception as e:
    print(f"   ✗ Error importing agent: {e}")

try:
    from ghl_agent.custom_app import app
    print("   ✓ Custom app imported successfully")
except Exception as e:
    print(f"   ✗ Error importing custom app: {e}")

try:
    from ghl_agent.tools.battery_tools import calculate_battery_runtime
    print("   ✓ Battery tools imported successfully")
except Exception as e:
    print(f"   ✗ Error importing battery tools: {e}")

print("\n3. Testing agent availability:")
try:
    from ghl_agent.agent.graph import graph
    print(f"   ✓ Graph nodes: {list(graph.nodes.keys())}")
except Exception as e:
    print(f"   ✗ Error accessing graph: {e}")

print("\n" + "=" * 50)
print("Setup test complete!")
print("\nNext steps:")
print("1. Make sure all required environment variables are set")
print("2. Run 'python test_agent_direct.py' to test the agent")
print("3. Run 'python run_local.py' to start the webhook server")
print("4. In another terminal, run 'python test_webhook_local.py' to test webhooks")