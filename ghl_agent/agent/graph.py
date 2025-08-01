"""LangGraph Cloud deployment graph"""
from typing import TypedDict, Annotated, Sequence, Dict, Any, List, Optional, Literal, Union
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
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

# State definition
class State(TypedDict):
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
2. Pregunta qué equipos desean energizar por 6-8 horas
3. Para apartamentos: Recomienda batería portátil (recarga por LUMA)
4. Para casas: Menciona opciones con placas solares, LUMA o planta eléctrica
5. Calcula el consumo usando estos valores estándar:
   - Nevera: 300W
   - TV: 70W
   - Abanico: 60W
   - Celulares: 15W
   - Bombilla LED: 10W
   - Freezer: 300W
6. Explica la fórmula: Horas = Capacidad batería (Wh) / Consumo total (W)
7. Da un ejemplo: Batería 5120Wh / 445W = ~11.5 horas
8. Pregunta si desean orientación personalizada o ver el catálogo

IMPORTANTE:
- SIEMPRE usa send_ghl_message para enviar mensajes al cliente
- El contact_id está disponible en el contexto
- Mantén respuestas cortas y conversacionales (2-3 oraciones máximo)
- Usa un tono amigable y profesional
- Si quieren orientación, recolecta: nombre, teléfono y email
- Si no quieren orientación, ofrece el enlace: tuplantapr.com
- Siempre enfócate en resolver necesidades de energía durante apagones"""


def agent(state: State) -> Dict[str, Any]:
    """Main agent node"""
    # Add system message if it's the first message
    messages = list(state["messages"])
    if not any(isinstance(m, SystemMessage) for m in messages):
        # Include contact_id in the system prompt
        system_content = SYSTEM_PROMPT + f"\n\nCONTEXTO IMPORTANTE:\n- Contact ID del cliente: {state['contact_id']}\n- Usa este contact_id cuando llames a send_ghl_message"
        messages.insert(0, SystemMessage(content=system_content))
    
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
async def process_ghl_message(contact_id: str, conversation_id: Optional[str], message: str, 
                            existing_state: Optional[Dict[str, Any]] = None) -> str:
    """Process a message from GHL webhook"""
    try:
        # Check if we're in cloud environment
        is_cloud = bool(os.getenv("LANGGRAPH_AUTH_TYPE"))
        
        if is_cloud:
            # In cloud, use direct model invocation to avoid state issues
            logger.info("Using cloud-optimized message processing")
            
            system_prompt = f"""Eres un agente de servicio al cliente especializado en sistemas de baterías y energía solar para Puerto Rico.
Tu objetivo es ayudar a los clientes a encontrar la solución de batería ideal para sus necesidades.

REGLA CRÍTICA: SIEMPRE usa la función send_ghl_message para enviar tu respuesta.
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
                    await send_ghl_message.ainvoke({
                        "contact_id": contact_id,
                        "message": response.content,
                        "conversation_id": conversation_id
                    })
                    return "Message sent via WhatsApp (forced)"
                
                return "No response generated"
                
        else:
            # Local environment - use full graph
            logger.info("Using local graph processing")
            
            state = {
                "messages": [HumanMessage(content=message)],
                "contact_id": contact_id,
                "conversation_id": conversation_id,
                "housing_type": None,
                "equipment_list": None,
                "total_consumption": None,
                "battery_recommendation": None,
                "interested_in_consultation": None,
                "customer_name": None,
                "customer_phone": None,
                "customer_email": None
            }
            
            result = await graph.ainvoke(state)
            
            # Check if message was sent
            for msg in result.get("messages", []):
                if hasattr(msg, "name") and msg.name == "send_ghl_message":
                    return "Message processed and sent via WhatsApp"
            
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