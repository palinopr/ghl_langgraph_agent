#!/usr/bin/env python3
"""Test script for LangGraph Cloud deployment"""
import httpx
import asyncio
import json
import os
from datetime import datetime

# Configuration
DEPLOYMENT_URL = os.getenv("LANGGRAPH_DEPLOYMENT_URL", "https://your-deployment.langgraph.app")
API_KEY = os.getenv("LANGCHAIN_API_KEY", "")


async def test_invoke():
    """Test the invoke endpoint"""
    print("Testing LangGraph Cloud Deployment")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "Initial Contact",
            "message": "Hi, I need help building a website for my business",
            "contact_id": "test-001"
        },
        {
            "name": "Budget Qualification",
            "message": "My budget is around $8,000",
            "contact_id": "test-001"
        },
        {
            "name": "Scheduling",
            "message": "Yes, I'd like to schedule a call. Thursday afternoon works for me",
            "contact_id": "test-001"
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for test in test_cases:
            print(f"\n{test['name']}:")
            print(f"User: {test['message']}")
            
            request_body = {
                "input": {
                    "messages": [{"role": "human", "content": test["message"]}],
                    "contact_id": test["contact_id"],
                    "conversation_id": "test-conv-001"
                },
                "config": {
                    "configurable": {
                        "thread_id": f"test-thread-{test['contact_id']}"
                    }
                }
            }
            
            try:
                response = await client.post(
                    f"{DEPLOYMENT_URL}/runs/invoke",
                    json=request_body,
                    headers={
                        "X-API-Key": API_KEY,
                        "Content-Type": "application/json"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    # Extract assistant response
                    messages = result.get("output", {}).get("messages", [])
                    for msg in messages:
                        if msg.get("type") == "ai":
                            print(f"Agent: {msg.get('content', 'No response')}")
                else:
                    print(f"Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"Error: {e}")
            
            await asyncio.sleep(1)  # Small delay between tests


async def test_stream():
    """Test the streaming endpoint"""
    print("\n\nTesting Streaming Response")
    print("=" * 50)
    
    request_body = {
        "input": {
            "messages": [{"role": "human", "content": "Tell me about your web development services"}],
            "contact_id": "test-stream-001",
            "conversation_id": None
        },
        "stream_mode": "values"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream(
                "POST",
                f"{DEPLOYMENT_URL}/runs/stream",
                json=request_body,
                headers={
                    "X-API-Key": API_KEY,
                    "Content-Type": "application/json"
                },
                timeout=30.0
            ) as response:
                print("Streaming response:")
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            # Process streaming data
                            if "messages" in data:
                                for msg in data["messages"]:
                                    if msg.get("type") == "ai":
                                        print(f"Agent: {msg.get('content', '')}")
                        except json.JSONDecodeError:
                            pass
                            
        except Exception as e:
            print(f"Streaming error: {e}")


async def test_thread_history():
    """Test conversation history"""
    print("\n\nTesting Thread History")
    print("=" * 50)
    
    thread_id = "test-history-001"
    
    # Send two messages in sequence
    messages = [
        "I need a website for my restaurant",
        "My budget is $6,000"
    ]
    
    async with httpx.AsyncClient() as client:
        for i, message in enumerate(messages):
            print(f"\nMessage {i+1}: {message}")
            
            request_body = {
                "input": {
                    "messages": [{"role": "human", "content": message}],
                    "contact_id": "test-history",
                    "conversation_id": "conv-history"
                },
                "config": {
                    "configurable": {
                        "thread_id": thread_id
                    }
                }
            }
            
            try:
                response = await client.post(
                    f"{DEPLOYMENT_URL}/runs/invoke",
                    json=request_body,
                    headers={
                        "X-API-Key": API_KEY,
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    messages = result.get("output", {}).get("messages", [])
                    for msg in messages:
                        if msg.get("type") == "ai" and not msg.get("tool_calls"):
                            print(f"Agent: {msg.get('content', '')}")
                
            except Exception as e:
                print(f"Error: {e}")
            
            await asyncio.sleep(1)


async def main():
    """Run all tests"""
    if not API_KEY:
        print("ERROR: Please set LANGCHAIN_API_KEY environment variable")
        return
    
    if DEPLOYMENT_URL == "https://your-deployment.langgraph.app":
        print("ERROR: Please set LANGGRAPH_DEPLOYMENT_URL environment variable")
        return
    
    print(f"Testing deployment at: {DEPLOYMENT_URL}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    
    # Run tests
    await test_invoke()
    await test_stream()
    await test_thread_history()
    
    print("\n" + "=" * 50)
    print("Testing completed!")
    print("\nView traces at: https://smith.langchain.com")


if __name__ == "__main__":
    asyncio.run(main())