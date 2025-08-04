"""LangGraph Cloud deployment graph - Battery Consultation Agent"""
from typing import TypedDict, Annotated, Sequence, Dict, Any, List, Optional, Literal, Union
from typing_extensions import TypedDict as ExtTypedDict, Annotated as ExtAnnotated
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
import os
import asyncio

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from ghl_agent.tools.ghl_tools import (
    send_ghl_message,
    get_ghl_contact_info,
    update_ghl_contact,
    get_available_calendar_slots,
    book_ghl_appointment
)

import structlog
logger = structlog.get_logger()

from ghl_agent.tools.battery_tools import (
    calculate_battery_runtime,
    recommend_battery_system,
    format_consultation_request
)

# Input schema - what the API accepts
class InputState(ExtTypedDict):
    """Input schema for the battery consultation agent"""
    messages: List[Dict[str, str]]  # Simple dict format for API input
    contact_id: str
    conversation_id: Optional[str]

# Output schema - what the API returns
class OutputState(ExtTypedDict):
    """Output schema for the battery consultation agent"""
    response: Optional[str]
    tool_calls: Optional[List[Dict[str, Any]]]
    error: Optional[str]
    
# Full state definition - internal state management
class State(ExtTypedDict):
    """Complete state for the battery consultation workflow"""
    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]
    contact_id: str
    conversation_id: Optional[str]
    # Battery consultation specific state
    housing_type: Optional[Literal["casa", "apartamento"]]
    equipment_list: Optional[List[str]]
    total_consumption: Optional[float]
    battery_recommendation: Optional[str]
    interested_in_consultation: Optional[bool]
    customer_name: Optional[str]
    customer_phone: Optional[str]
    customer_email: Optional[str]
    # Error tracking
    error: Optional[str]
    response: Optional[str]
    tool_calls: Optional[List[Dict[str, Any]]]


# Initialize the model
model = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.7
)

# Enhanced tools with better error handling
async def safe_send_ghl_message(contact_id: str, message: str, conversation_id: Optional[str] = None) -> str:
    """Send message with enhanced error handling"""
    try:
        result = await send_ghl_message.ainvoke({
            "contact_id": contact_id,
            "message": message,
            "conversation_id": conversation_id
        })
        return result
    except Exception as e:
        logger.error(f"Tool error in send_ghl_message: {str(e)}")
        raise Exception(f"Failed to send message: {str(e)}")

# Tools list with proper error handling
tools = [
    send_ghl_message,
    get_ghl_contact_info,
    update_ghl_contact,
    get_available_calendar_slots,
    book_ghl_appointment,
    calculate_battery_runtime,
    recommend_battery_system,
    format_consultation_request
]

# Bind tools to model
model_with_tools = model.bind_tools(tools)

# System prompt
SYSTEM_PROMPT = """Eres un agente de servicio al cliente especializado en sistemas de baterías y energía solar para Puerto Rico.
Tu objetivo es ayudar a los clientes a encontrar la solución de batería ideal para sus necesidades.

REGLA CRÍTICA: SIEMPRE debes usar la función send_ghl_message para enviar TODAS tus respuestas al cliente. 
No escribas respuestas directamente - SIEMPRE usa la herramienta send_ghl_message.

FLUJO DE CONVERSACIÓN:
1. Saluda cordialmente y pregunta si viven en casa o apartamento
2. Pregunta qué equipos desean energizar durante un apagón (6-8 horas)
3. Para apartamentos: Recomienda batería portátil (se recarga con la luz de LUMA)
4. Para casas: Menciona opciones de recarga (placas solares, luz de LUMA, planta eléctrica)
5. Calcula consumo con valores estándar (Nevera:300W, TV:70W, Abanico:60W, etc.)
6. Explica la fórmula: Horas = Capacidad batería (Wh) / Consumo total (W)
7. Pregunta si desean orientación personalizada o ver el catálogo

PRODUCTOS RECOMENDADOS:
- Apartamentos/Bajo consumo (<1000W): EcoFlow Delta 2 (1024Wh)
- Casas/Consumo medio (1000-2000W): EG4 LifePower 48V 100Ah (5120Wh)
- Alto consumo (>2000W): Sistema expandible Growatt o múltiples EG4

Mantén respuestas cortas y conversacionales (2-3 oraciones máximo)."""

# Helper function to convert dict messages to BaseMessage objects
def convert_messages(messages: List[Union[Dict, BaseMessage]]) -> List[BaseMessage]:
    """Convert dict messages to proper BaseMessage objects"""
    converted = []
    for msg in messages:
        if isinstance(msg, BaseMessage):
            converted.append(msg)
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "human" or role == "user":
                converted.append(HumanMessage(content=content))
            elif role == "assistant" or role == "ai":
                converted.append(AIMessage(content=content))
            elif role == "system":
                converted.append(SystemMessage(content=content))
            else:
                converted.append(HumanMessage(content=content))
    return converted

# Agent node
async def agent(state: State) -> State:
    """Main agent logic"""
    try:
        messages = state["messages"]
        
        # Convert dict messages to BaseMessage objects if needed
        if messages and isinstance(messages[0], dict):
            messages = convert_messages(messages)
        
        # Add system message if not present
        if not messages or (len(messages) > 0 and hasattr(messages[0], 'type') and messages[0].type != "system"):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
        # Invoke model
        response = await model_with_tools.ainvoke(messages)
        
        # Track tool calls for output
        tool_calls = []
        if response.tool_calls:
            for tc in response.tool_calls:
                tool_calls.append({
                    "name": tc["name"],
                    "args": tc["args"]
                })
        
        # Update state
        return {
            "messages": [response],
            "tool_calls": tool_calls,
            "response": response.content if response.content else None
        }
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        return {
            "error": str(e),
            "messages": [AIMessage(content="Disculpa, tuve un problema procesando tu mensaje. ¿Podrías repetirlo?")]
        }

# Error handling node
def error_node(state: State) -> State:
    """Handle errors gracefully"""
    error_msg = state.get("error", "Error desconocido")
    logger.error(f"Error node triggered: {error_msg}")
    
    # Try to send error message to user
    try:
        contact_id = state.get("contact_id")
        if contact_id:
            # Create a simple error message
            error_response = AIMessage(
                content="Disculpa, estoy teniendo problemas técnicos. Por favor intenta nuevamente en unos momentos."
            )
            return {
                "messages": [error_response],
                "error": error_msg,
                "response": "Error técnico - por favor intenta nuevamente"
            }
    except:
        pass
    
    return state

# Conditional edge function
def should_continue(state: State) -> str:
    """Determine next step in the graph"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check for errors
    if state.get("error"):
        return "error"
    
    # If LLM makes tool call, route to tools
    if last_message.tool_calls:
        return "tools"
    
    # Otherwise end
    return "end"

# Create the graph with explicit schemas
workflow = StateGraph(
    State, 
    input_schema=InputState,
    output_schema=OutputState
)

# Custom tool node that formats output properly
async def tool_node(state: State) -> State:
    """Execute tools and format output"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        tool_node_instance = ToolNode(tools)
        # Use ainvoke for async execution
        result = await tool_node_instance.ainvoke(state)
        
        # Extract tool response for output
        tool_response = None
        if "messages" in result and len(result["messages"]) > 0:
            for msg in result["messages"]:
                if hasattr(msg, "content"):
                    tool_response = msg.content
                    break
        
        # Update state with tool results
        return {
            "messages": result.get("messages", []),
            "response": tool_response or "Tool executed successfully"
        }
    
    return state

# Add nodes
workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)
workflow.add_node("error", error_node)

# Set entry point
workflow.add_edge(START, "agent")

# Add conditional routing
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "error": "error",
        "end": END
    }
)

# Route tools directly to end (no loop back to agent)
workflow.add_edge("tools", END)

# Error node goes to end
workflow.add_edge("error", END)

# Compile the graph
graph = workflow.compile()

# Cloud-optimized message processing function
async def process_ghl_message(
    contact_id: str,
    conversation_id: Optional[str],
    message: str,
    conversation_history: List[Dict[str, str]] = None
) -> str:
    """Process a message from GoHighLevel webhook - optimized for cloud deployment"""
    try:
        # Check if running in cloud deployment
        is_cloud = os.getenv("LANGGRAPH_AUTH_TYPE") is not None
        
        if is_cloud:
            # Cloud deployment - use direct tool invocation
            logger.info("Using cloud-optimized message processing")
            
            # Use direct GHL tool
            send_tool_name = "send_ghl_message"
            
            system_prompt = f"""Eres un agente de servicio al cliente especializado en sistemas de baterías y energía solar para Puerto Rico.
Tu objetivo es ayudar a los clientes a encontrar la solución de batería ideal para sus necesidades.

REGLA CRÍTICA: SIEMPRE usa la función {send_tool_name} para enviar tu respuesta.
Contact ID: {contact_id}

FLUJO DE CONVERSACIÓN:
1. Saluda cordialmente y pregunta si viven en casa o apartamento
2. Pregunta qué equipos desean energizar por 6-8 horas
3. Para apartamentos: Recomienda batería portátil (recarga por LUMA)
4. Para casas: Menciona opciones con placas solares, LUMA o planta eléctrica
5. Calcula el consumo con valores estándar (Nevera:300W, TV:70W, Abanico:60W, etc.)
6. Explica la fórmula: Horas = Capacidad batería (Wh) / Consumo total (W)
7. Pregunta si desean orientación personalizada o ver el catálogo

Mantén respuestas cortas y conversacionales (2-3 oraciones máximo)."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            # Get response with retry handling
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = await model_with_tools.ainvoke(messages)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Model invocation attempt {attempt + 1} failed: {e}")
                    await asyncio.sleep(1)
            
            # Execute tool calls
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    if tool_call['name'] == 'send_ghl_message':
                        args = tool_call['args'].copy()
                        if conversation_id:
                            args['conversation_id'] = conversation_id
                        
                        try:
                            # Use direct GHL tool
                            result = await send_ghl_message.ainvoke(args)
                            logger.info(f"WhatsApp message sent: {result}")
                        except Exception as tool_error:
                            logger.error(f"Tool execution error: {tool_error}")
                            # Return error info for debugging
                            return f"Tool error: {str(tool_error)}"
                
                return "Message processed and sent via WhatsApp"
            else:
                # Force send if no tool calls
                if response.content:
                    # Use the direct GHL tool
                    await send_ghl_message.ainvoke({
                        "contact_id": contact_id,
                        "message": response.content,
                        "conversation_id": conversation_id
                    })
                    return "Message sent via WhatsApp (forced)"
                
                return "No response generated"
                
        else:
            # Local mode - use full graph
            logger.info("Using local graph processing")
            
            # Convert conversation history to messages
            messages = []
            if conversation_history:
                for msg in conversation_history:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    if role == "assistant":
                        messages.append(AIMessage(content=content))
                    else:
                        messages.append(HumanMessage(content=content))
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Create state
            state = {
                "messages": messages,
                "contact_id": contact_id,
                "conversation_id": conversation_id
            }
            
            # Invoke graph
            result = await graph.ainvoke(state)
            
            # Extract response
            if result.get("error"):
                return f"Error: {result['error']}"
            elif result.get("response"):
                return result["response"]
            else:
                return "Message processed"
                
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to send error message
        try:
            await send_ghl_message.ainvoke({
                "contact_id": contact_id,
                "message": "Disculpa, estoy teniendo problemas técnicos. Por favor intenta nuevamente.",
                "conversation_id": conversation_id
            })
        except:
            pass
            
        return f"Error processing message: {str(e)}"


# Optional: Add checkpointer for production
def get_checkpointer():
    """Get checkpointer for production use"""
    postgres_uri = os.getenv("POSTGRES_URI")
    if postgres_uri:
        try:
            from langgraph.checkpoint.postgres import PostgresSaver
            return PostgresSaver.from_conn_string(postgres_uri)
        except ImportError:
            logger.warning("PostgresSaver not available, using memory checkpointer")
    
    # Default to memory checkpointer for development
    from langgraph.checkpoint.memory import MemorySaver
    return MemorySaver()


# Export for cloud deployment
__all__ = ["graph", "process_ghl_message", "State"]