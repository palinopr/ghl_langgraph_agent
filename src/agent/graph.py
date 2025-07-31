"""LangGraph Cloud deployment graph"""
from typing import TypedDict, Annotated, Sequence, Dict, Any, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os

from ..tools.ghl_tools import (
    send_ghl_message,
    get_ghl_contact_info,
    update_ghl_contact,
    get_available_calendar_slots,
    book_ghl_appointment
)

# State definition
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]
    contact_id: str
    conversation_id: str | None


# Initialize the model
model = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.7
)

# Tools
tools = [
    send_ghl_message,
    get_ghl_contact_info,
    update_ghl_contact,
    get_available_calendar_slots,
    book_ghl_appointment
]

# Bind tools to model
model_with_tools = model.bind_tools(tools)

# System prompt
SYSTEM_PROMPT = """You are a customer service AI agent for a web development agency.
Your job is to qualify leads and schedule appointments.

Conversation flow:
1. Greet warmly and ask about their project needs
2. Ask about their budget (minimum $5,000 to qualify)
3. If qualified, offer to schedule a consultation
4. If not qualified, politely explain and offer resources

Keep responses short and conversational (1-2 sentences max)."""


def agent(state: State) -> Dict[str, Any]:
    """Main agent node"""
    # Add system message if it's the first message
    messages = list(state["messages"])
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))
    
    # Get response from model
    response = model_with_tools.invoke(messages)
    
    # Return updated messages
    return {"messages": [response]}


def should_continue(state: State) -> str:
    """Determine if we should continue or end"""
    last_message = state["messages"][-1]
    
    # If there are tool calls, continue to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, we're done
    return "end"


# Build the graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("agent", agent)
workflow.add_node("tools", ToolNode(tools))

# Set entry point
workflow.set_entry_point("agent")

# Add edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)

# Always go back to agent after tools
workflow.add_edge("tools", "agent")

# Compile the graph
graph = workflow.compile()


# Helper function for webhook integration
async def process_ghl_message(contact_id: str, conversation_id: str, message: str) -> str:
    """Process a message from GHL webhook"""
    try:
        # Initialize state
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "contact_id": contact_id,
            "conversation_id": conversation_id
        }
        
        # Run the graph
        result = await graph.ainvoke(initial_state)
        
        # Extract the assistant's response
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    continue  # Skip tool call messages
                return msg.content
        
        return "I'm here to help! Could you tell me more about your project?"
        
    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()
        return "I apologize, but I'm having trouble processing your request. Please try again."