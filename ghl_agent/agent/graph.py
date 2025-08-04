"""LangGraph Cloud deployment graph - Battery Consultation Agent"""
from typing import TypedDict, Annotated, Sequence, Dict, Any, List, Optional, Literal, Union
from typing_extensions import TypedDict as ExtTypedDict, Annotated as ExtAnnotated
from operator import add
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.errors import NodeInterrupt
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
import os
import asyncio
import uuid
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from ghl_agent.tools.ghl_tools import (
    send_ghl_message,
    get_ghl_contact_info,
    update_ghl_contact,
    get_available_calendar_slots,
    book_ghl_appointment,
    get_conversation_messages
)

import structlog
logger = structlog.get_logger()

from ghl_agent.tools.battery_tools import (
    calculate_battery_runtime,
    recommend_battery_system,
    format_consultation_request
)

from ghl_agent.config_loader import get_config, get_config_value

# Load configuration
config = get_config()

# Configuration schema for deployment
class AgentConfig(BaseModel):
    """Configuration for the battery consultation agent"""
    min_budget: int = Field(default_factory=lambda: config.qualification.min_budget, description="Minimum budget requirement in USD")
    calendar_days_ahead: int = Field(default_factory=lambda: config.calendar.days_ahead, description="Days to look ahead for appointments")
    response_language: str = Field(default_factory=lambda: config.business.language, description="Language for responses (es/en)")
    max_retry_attempts: int = Field(default_factory=lambda: config.behavior.max_retry_attempts, description="Max retries for failed operations")
    enable_human_review: bool = Field(default_factory=lambda: config.behavior.enable_human_review, description="Enable human review for appointments")
    enable_memory: bool = Field(default_factory=lambda: config.memory.enable_persistence, description="Enable conversation memory persistence")
    parallel_tool_calls: bool = Field(default_factory=lambda: config.behavior.parallel_tool_calls, description="Enable parallel tool execution")

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
    
# Memory schemas
class ConversationMemory(BaseModel):
    """Schema for storing conversation context"""
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    housing_type: Optional[Literal["casa", "apartamento"]] = None
    equipment_list: List[str] = Field(default_factory=list)
    total_consumption: Optional[float] = None
    budget_confirmed: Optional[bool] = None
    appointment_scheduled: Optional[bool] = None
    last_interaction: datetime = Field(default_factory=datetime.now)

class CustomerPreferences(BaseModel):
    """Schema for storing customer preferences"""
    preferred_contact_method: Optional[Literal["sms", "whatsapp", "call"]] = None
    preferred_time_slots: List[str] = Field(default_factory=list)
    language_preference: str = "es"
    notes: List[str] = Field(default_factory=list)

# Full state definition - internal state management
class State(ExtTypedDict):
    """Complete state for the battery consultation workflow"""
    messages: Annotated[Sequence[BaseMessage], add]  # Auto-merge messages
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
    # Conversation tracking
    conversation_stage: Optional[Literal["greeting", "discovery", "qualification", "scheduling", "completed"]]
    retry_count: int
    # Error tracking
    error: Optional[str]
    response: Optional[str]
    tool_calls: Optional[List[Dict[str, Any]]]
    # Configuration
    config: Optional[AgentConfig]
    # Memory store reference
    store: Optional[BaseStore]


# Initialize the model
model = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.7
)

# Memory management functions
def get_memory_store(state: State) -> BaseStore:
    """Get or create memory store for the conversation"""
    if state.get("store"):
        return state["store"]
    return InMemoryStore()

def load_conversation_memory(store: BaseStore, contact_id: str) -> Optional[ConversationMemory]:
    """Load conversation memory from store"""
    try:
        namespace = ("conversation", contact_id)
        memories = store.search(namespace)
        if memories:
            return ConversationMemory(**memories[0].value)
    except Exception as e:
        logger.warning(f"Failed to load conversation memory: {e}")
    return None

def save_conversation_memory(store: BaseStore, contact_id: str, memory: ConversationMemory):
    """Save conversation memory to store"""
    try:
        namespace = ("conversation", contact_id)
        store.put(namespace, str(uuid.uuid4()), memory.model_dump(mode="json"))
    except Exception as e:
        logger.error(f"Failed to save conversation memory: {e}")

def load_customer_preferences(store: BaseStore, contact_id: str) -> Optional[CustomerPreferences]:
    """Load customer preferences from store"""
    try:
        namespace = ("preferences", contact_id)
        memories = store.search(namespace)
        if memories:
            return CustomerPreferences(**memories[0].value)
    except Exception as e:
        logger.warning(f"Failed to load customer preferences: {e}")
    return None

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
    get_conversation_messages,
    calculate_battery_runtime,
    recommend_battery_system,
    format_consultation_request
]

# Bind tools to model with parallel execution support
model_with_tools = model.bind_tools(tools, parallel_tool_calls=True)

# Build system prompt from config
def build_system_prompt():
    """Build system prompt from configuration"""
    equipment_list = ", ".join([f"{k.capitalize()}:{v}W" for k, v in list(config.equipment_consumption.items())[:5]])
    
    products_text = []
    for category, products in config.products.items():
        for product in products:
            products_text.append(f"- {product['best_for']}: {product['name']} ({product['capacity_wh']}Wh)")
    
    return f"""Eres un agente de servicio al cliente de {config.business.name}.
Tu objetivo es ayudar a los clientes a encontrar la solución de batería ideal para sus necesidades.

REGLA CRÍTICA: SIEMPRE debes usar la función send_ghl_message para enviar TODAS tus respuestas al cliente. 
No escribas respuestas directamente - SIEMPRE usa la herramienta send_ghl_message.

CONTEXTO DE CONVERSACIÓN:
Si recibes un conversation_id, SIEMPRE debes primero usar get_conversation_messages para obtener el historial de conversación completo antes de responder. Esto te ayudará a entender el contexto y continuar la conversación apropiadamente.

FLUJO DE CONVERSACIÓN:
1. Saluda cordialmente y pregunta si viven en casa o apartamento
2. Pregunta qué equipos desean energizar durante un apagón (6-8 horas)
3. Para apartamentos: Recomienda batería portátil (se recarga con la luz de LUMA)
4. Para casas: Menciona opciones de recarga (placas solares, luz de LUMA, planta eléctrica)
5. Calcula consumo con valores estándar ({equipment_list}, etc.)
6. Explica la fórmula: Horas = Capacidad batería (Wh) / Consumo total (W)
7. Pregunta si desean orientación personalizada o ver el catálogo

PRODUCTOS RECOMENDADOS:
{chr(10).join(products_text)}

Presupuesto mínimo: ${config.qualification.min_budget}

Mantén respuestas cortas y conversacionales (2-3 oraciones máximo).
Responde en {config.business.language}."""

# System prompt
SYSTEM_PROMPT = build_system_prompt()

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

# Conditional execution helpers
def should_book_appointment(state: State) -> bool:
    """Check if we have enough info to book an appointment"""
    return bool(
        state.get("interested_in_consultation") and 
        state.get("customer_phone") and
        state.get("total_consumption") is not None
    )

def should_calculate_consumption(state: State) -> bool:
    """Check if we have equipment list to calculate consumption"""
    return bool(state.get("equipment_list") and len(state["equipment_list"]) > 0)

def get_conversation_stage(state: State) -> str:
    """Determine current conversation stage based on state"""
    if not state.get("housing_type"):
        return "discovery"
    elif not state.get("total_consumption"):
        return "qualification"
    elif state.get("interested_in_consultation") and not state.get("customer_phone"):
        return "scheduling"
    elif state.get("customer_phone"):
        return "completed"
    return "greeting"

# Agent node with memory support
async def agent(state: State) -> State:
    """Main agent logic with enhanced error handling and memory support"""
    try:
        messages = state["messages"]
        contact_id = state["contact_id"]
        config = state.get("config", AgentConfig())
        
        # Get memory store
        store = get_memory_store(state)
        
        # Load conversation memory if enabled
        conversation_memory = None
        customer_preferences = None
        if config.enable_memory:
            conversation_memory = load_conversation_memory(store, contact_id)
            customer_preferences = load_customer_preferences(store, contact_id)
        
        # Convert dict messages to BaseMessage objects if needed
        if messages and isinstance(messages[0], dict):
            messages = convert_messages(messages)
        
        # Build enhanced system prompt with memory context
        system_content = SYSTEM_PROMPT
        
        # Add conversation_id to context if available
        conversation_id = state.get("conversation_id")
        if conversation_id:
            system_content += f"\n\nConversation ID: {conversation_id}\nRecuerda: DEBES usar get_conversation_messages con este ID para obtener el historial completo antes de responder."
        
        if conversation_memory:
            memory_context = f"\n\nCONTEXTO DE CONVERSACIÓN PREVIA:\n"
            if conversation_memory.customer_name:
                memory_context += f"- Nombre del cliente: {conversation_memory.customer_name}\n"
            if conversation_memory.housing_type:
                memory_context += f"- Tipo de vivienda: {conversation_memory.housing_type}\n"
            if conversation_memory.equipment_list:
                memory_context += f"- Equipos mencionados: {', '.join(conversation_memory.equipment_list)}\n"
            if conversation_memory.total_consumption:
                memory_context += f"- Consumo calculado: {conversation_memory.total_consumption}W\n"
            if conversation_memory.budget_confirmed:
                memory_context += f"- Presupuesto confirmado: {'Sí' if conversation_memory.budget_confirmed else 'No'}\n"
            system_content += memory_context
        
        # Add system message if not present
        if not messages or (len(messages) > 0 and hasattr(messages[0], 'type') and messages[0].type != "system"):
            messages = [SystemMessage(content=system_content)] + messages
        
        # Update conversation stage
        current_stage = get_conversation_stage(state)
        
        # Check for human review requirement
        if config.enable_human_review and should_book_appointment(state):
            raise NodeInterrupt(
                f"Human review required before booking appointment. "
                f"Customer: {state.get('customer_name', 'Unknown')}, "
                f"Phone: {state.get('customer_phone', 'Unknown')}"
            )
        
        # Configure model for parallel tool calls if enabled
        active_model = model_with_tools if config.parallel_tool_calls else model.bind_tools(tools, parallel_tool_calls=False)
        
        # Invoke model with retry logic
        retry_count = state.get("retry_count", 0)
        max_retries = config.max_retry_attempts
        
        response = None
        for attempt in range(max_retries):
            try:
                response = await active_model.ainvoke(messages)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Model invocation attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(1)
        
        # Track tool calls for output
        tool_calls = []
        if response.tool_calls:
            for tc in response.tool_calls:
                tool_calls.append({
                    "name": tc["name"],
                    "args": tc["args"]
                })
        
        # Save updated memory if enabled
        if config.enable_memory and any([
            state.get("customer_name"),
            state.get("housing_type"),
            state.get("equipment_list"),
            state.get("total_consumption")
        ]):
            new_memory = ConversationMemory(
                customer_name=state.get("customer_name") or (conversation_memory.customer_name if conversation_memory else None),
                customer_phone=state.get("customer_phone") or (conversation_memory.customer_phone if conversation_memory else None),
                customer_email=state.get("customer_email") or (conversation_memory.customer_email if conversation_memory else None),
                housing_type=state.get("housing_type") or (conversation_memory.housing_type if conversation_memory else None),
                equipment_list=state.get("equipment_list") or (conversation_memory.equipment_list if conversation_memory else []),
                total_consumption=state.get("total_consumption") or (conversation_memory.total_consumption if conversation_memory else None),
                budget_confirmed=state.get("interested_in_consultation"),
                appointment_scheduled=current_stage == "completed"
            )
            save_conversation_memory(store, contact_id, new_memory)
        
        # Update state
        return {
            "messages": [response],
            "tool_calls": tool_calls,
            "response": response.content if response.content else None,
            "conversation_stage": current_stage,
            "retry_count": 0,  # Reset on success
            "store": store  # Pass store reference
        }
    except NodeInterrupt:
        raise  # Re-raise interrupts for human review
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        retry_count = state.get("retry_count", 0)
        return {
            "error": str(e),
            "messages": [AIMessage(content="Disculpa, tuve un problema procesando tu mensaje. ¿Podrías repetirlo?")],
            "retry_count": retry_count + 1
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

# Conditional edge function with enhanced routing
def should_continue(state: State) -> str:
    """Determine next step in the graph"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # Check for errors first
    if state.get("error"):
        # Check retry count
        config = state.get("config", AgentConfig())
        if state.get("retry_count", 0) >= config.max_retry_attempts:
            return "error"
        return "agent"  # Retry
    
    # Use standard tools_condition for tool routing
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Check if conversation is complete
    if state.get("conversation_stage") == "completed":
        return "end"
    
    # Otherwise end
    return "end"

# Parallel enrichment nodes (example of parallel execution pattern)
async def enrich_contact_info(state: State) -> State:
    """Enrich contact information from GHL (runs in parallel with battery calculation)"""
    try:
        contact_id = state["contact_id"]
        if contact_id and not state.get("customer_name"):
            # This could run in parallel with other operations
            contact_info = await get_ghl_contact_info.ainvoke({"contact_id": contact_id})
            return {
                "customer_name": contact_info.get("name"),
                "customer_email": contact_info.get("email"),
                "customer_phone": contact_info.get("phone")
            }
    except Exception as e:
        logger.warning(f"Failed to enrich contact info: {e}")
    return {}

async def calculate_consumption_parallel(state: State) -> State:
    """Calculate consumption in parallel (example of parallel node)"""
    try:
        if state.get("equipment_list") and not state.get("total_consumption"):
            # This runs in parallel with contact enrichment
            result = await calculate_battery_runtime.ainvoke({
                "equipment_list": state["equipment_list"],
                "battery_capacity_wh": 1024  # Default for estimation
            })
            # Extract consumption from result
            return {"total_consumption": result.get("total_consumption", 0)}
    except Exception as e:
        logger.warning(f"Failed to calculate consumption: {e}")
    return {}

# Create the graph with explicit schemas
workflow = StateGraph(
    State, 
    input_schema=InputState,
    output_schema=OutputState
)

# Add nodes
workflow.add_node("agent", agent)
workflow.add_node("tools", ToolNode(tools))  # Use standard ToolNode
workflow.add_node("error", error_node)

# Optional: Add parallel enrichment nodes (commented out by default)
# workflow.add_node("enrich_contact", enrich_contact_info)
# workflow.add_node("calculate_consumption", calculate_consumption_parallel)

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

# Route tools back to agent for continued conversation
workflow.add_edge("tools", "agent")

# Error node goes to end
workflow.add_edge("error", END)

# Optional: Example of parallel execution pattern
# To enable parallel enrichment, uncomment these lines:
# workflow.add_edge(START, "enrich_contact")  # Runs in parallel with agent
# workflow.add_edge(START, "calculate_consumption")  # Runs in parallel with agent
# workflow.add_edge("enrich_contact", "agent")  # Merge results
# workflow.add_edge("calculate_consumption", "agent")  # Merge results

# Compile the graph
graph = workflow.compile()

# Streaming helper for better UX
async def stream_graph_updates(state: State, config: AgentConfig = None):
    """Stream updates during graph execution"""
    if not config:
        config = state.get("config", AgentConfig())
    
    # Stream status updates
    yield {"status": "processing", "stage": state.get("conversation_stage", "unknown")}
    
    # If calculating consumption
    if should_calculate_consumption(state):
        yield {"status": "calculating", "message": "Calculando consumo eléctrico..."}
    
    # If booking appointment
    if should_book_appointment(state):
        yield {"status": "booking", "message": "Verificando disponibilidad de calendario..."}
    
    # If we have tool calls
    if state.get("tool_calls"):
        for tool_call in state["tool_calls"]:
            yield {
                "status": "tool_execution",
                "tool": tool_call["name"],
                "message": f"Ejecutando: {tool_call['name']}"
            }

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


# Enhanced checkpointer for production with store support
def get_checkpointer_with_store():
    """Get checkpointer and store for production use"""
    postgres_uri = os.getenv("POSTGRES_URI")
    
    # Try PostgreSQL first
    if postgres_uri:
        try:
            from langgraph.checkpoint.postgres import PostgresSaver
            from langgraph.store.postgres import PostgresStore
            checkpointer = PostgresSaver.from_conn_string(postgres_uri)
            store = PostgresStore.from_conn_string(postgres_uri)
            return checkpointer, store
        except ImportError:
            logger.warning("PostgreSQL packages not available, using memory-based solutions")
    
    # Try Redis if configured
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            from langgraph.checkpoint.redis import RedisSaver
            from langgraph.store.redis import RedisStore
            checkpointer = RedisSaver.from_conn_string(redis_url)
            store = RedisStore.from_conn_string(redis_url)
            return checkpointer, store
        except ImportError:
            logger.warning("Redis packages not available, using memory-based solutions")
    
    # Default to memory-based solutions for development
    from langgraph.checkpoint.memory import MemorySaver
    return MemorySaver(), InMemoryStore()

# Compile graph with optional checkpointer
def compile_graph_with_config(enable_checkpointing: bool = False):
    """Compile graph with optional checkpointing and store"""
    if enable_checkpointing:
        checkpointer, store = get_checkpointer_with_store()
        compiled = workflow.compile(checkpointer=checkpointer)
        # Attach store to compiled graph for runtime access
        compiled.store = store
        return compiled
    return workflow.compile()


# Export for cloud deployment
__all__ = [
    "graph", 
    "process_ghl_message", 
    "State",
    "AgentConfig",
    "stream_graph_updates",
    "get_checkpointer_with_store",
    "compile_graph_with_config",
    "should_book_appointment",
    "should_calculate_consumption",
    "get_conversation_stage",
    "ConversationMemory",
    "CustomerPreferences",
    "load_conversation_memory",
    "save_conversation_memory",
    "enrich_contact_info",
    "calculate_consumption_parallel"
]