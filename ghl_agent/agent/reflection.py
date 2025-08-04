"""Reflection graph for analyzing conversations and extracting insights"""
from typing import TypedDict, Dict, Any, List, Optional
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import structlog
from datetime import datetime

logger = structlog.get_logger()

# Reflection state
class ReflectionState(TypedDict):
    """State for reflection analysis"""
    messages: List[BaseMessage]
    contact_id: str
    extracted_insights: Optional[Dict[str, Any]]
    customer_sentiment: Optional[str]
    next_best_action: Optional[str]
    conversation_summary: Optional[str]
    key_topics: Optional[List[str]]
    pain_points: Optional[List[str]]
    opportunities: Optional[List[str]]

# Initialize reflection model
reflection_model = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.3  # Lower temperature for more consistent analysis
)

REFLECTION_PROMPT = """Analiza esta conversación y extrae información valiosa para mejorar el servicio al cliente.

Tu tarea es:
1. Identificar el sentimiento del cliente (positivo/neutral/negativo)
2. Extraer temas clave discutidos
3. Identificar puntos de dolor o frustraciones
4. Detectar oportunidades de venta o servicio
5. Resumir la conversación en 2-3 oraciones
6. Sugerir la mejor acción siguiente

Proporciona tu análisis en formato estructurado:

SENTIMIENTO: [positivo/neutral/negativo]
TEMAS CLAVE: [lista de temas]
PUNTOS DE DOLOR: [lista de problemas]
OPORTUNIDADES: [lista de oportunidades]
RESUMEN: [resumen breve]
PRÓXIMA ACCIÓN: [acción recomendada]

Conversación a analizar:"""

async def analyze_conversation(state: ReflectionState) -> ReflectionState:
    """Analyze conversation and extract insights"""
    try:
        messages = state["messages"]
        
        # Build conversation text
        conversation_text = "\n".join([
            f"{msg.type.upper()}: {msg.content}"
            for msg in messages[-10:]  # Last 10 messages for context
        ])
        
        # Create analysis prompt
        analysis_messages = [
            SystemMessage(content=REFLECTION_PROMPT),
            HumanMessage(content=conversation_text)
        ]
        
        # Get analysis
        response = await reflection_model.ainvoke(analysis_messages)
        content = response.content
        
        # Parse response (simple parsing, could be enhanced with structured output)
        insights = {}
        sentiment = "neutral"
        topics = []
        pain_points = []
        opportunities = []
        summary = ""
        next_action = ""
        
        lines = content.split('\n')
        for line in lines:
            if line.startswith("SENTIMIENTO:"):
                sentiment = line.replace("SENTIMIENTO:", "").strip()
            elif line.startswith("TEMAS CLAVE:"):
                topics = [t.strip() for t in line.replace("TEMAS CLAVE:", "").split(",")]
            elif line.startswith("PUNTOS DE DOLOR:"):
                pain_points = [p.strip() for p in line.replace("PUNTOS DE DOLOR:", "").split(",")]
            elif line.startswith("OPORTUNIDADES:"):
                opportunities = [o.strip() for o in line.replace("OPORTUNIDADES:", "").split(",")]
            elif line.startswith("RESUMEN:"):
                summary = line.replace("RESUMEN:", "").strip()
            elif line.startswith("PRÓXIMA ACCIÓN:"):
                next_action = line.replace("PRÓXIMA ACCIÓN:", "").strip()
        
        # Build insights dictionary
        insights = {
            "sentiment": sentiment,
            "topics": topics,
            "pain_points": pain_points,
            "opportunities": opportunities,
            "summary": summary,
            "next_action": next_action,
            "analyzed_at": datetime.now().isoformat()
        }
        
        logger.info("Conversation analysis completed", 
                   contact_id=state["contact_id"],
                   sentiment=sentiment,
                   topics_count=len(topics))
        
        return {
            "extracted_insights": insights,
            "customer_sentiment": sentiment,
            "next_best_action": next_action,
            "conversation_summary": summary,
            "key_topics": topics,
            "pain_points": pain_points,
            "opportunities": opportunities
        }
        
    except Exception as e:
        logger.error("Failed to analyze conversation", error=str(e))
        return {
            "extracted_insights": None,
            "customer_sentiment": "unknown",
            "next_best_action": "Continue standard flow"
        }

async def identify_patterns(state: ReflectionState) -> ReflectionState:
    """Identify patterns across multiple conversations"""
    try:
        # This could be enhanced to look at historical conversations
        # For now, we'll focus on current conversation patterns
        
        insights = state.get("extracted_insights", {})
        topics = insights.get("topics", [])
        
        # Identify common battery-related patterns
        patterns = []
        
        if "casa" in str(topics).lower() or "apartamento" in str(topics).lower():
            patterns.append("housing_type_mentioned")
        
        if any(equip in str(topics).lower() for equip in ["nevera", "abanico", "luces"]):
            patterns.append("equipment_specified")
        
        if "presupuesto" in str(topics).lower() or "$" in str(topics).lower():
            patterns.append("budget_discussed")
        
        if "cita" in str(topics).lower() or "consulta" in str(topics).lower():
            patterns.append("appointment_interest")
        
        # Update insights with patterns
        if insights:
            insights["patterns"] = patterns
        
        logger.info("Patterns identified", patterns=patterns)
        
        return {"extracted_insights": insights}
        
    except Exception as e:
        logger.error("Failed to identify patterns", error=str(e))
        return state

async def generate_recommendations(state: ReflectionState) -> ReflectionState:
    """Generate recommendations based on analysis"""
    try:
        insights = state.get("extracted_insights", {})
        sentiment = state.get("customer_sentiment", "neutral")
        pain_points = state.get("pain_points", [])
        opportunities = state.get("opportunities", [])
        
        recommendations = []
        
        # Sentiment-based recommendations
        if sentiment == "negativo":
            recommendations.append("Prioritize empathetic response")
            recommendations.append("Offer immediate assistance")
        elif sentiment == "positivo":
            recommendations.append("Capitalize on positive momentum")
            recommendations.append("Move towards closing")
        
        # Pain point based recommendations
        if "precio" in str(pain_points).lower():
            recommendations.append("Emphasize value and ROI")
            recommendations.append("Mention financing options")
        
        if "urgencia" in str(pain_points).lower():
            recommendations.append("Highlight quick installation")
            recommendations.append("Offer expedited consultation")
        
        # Opportunity based recommendations
        if opportunities:
            recommendations.append(f"Focus on: {', '.join(opportunities[:2])}")
        
        # Update insights
        if insights:
            insights["recommendations"] = recommendations
        
        logger.info("Recommendations generated", 
                   count=len(recommendations),
                   sentiment=sentiment)
        
        return {"extracted_insights": insights}
        
    except Exception as e:
        logger.error("Failed to generate recommendations", error=str(e))
        return state

# Build reflection graph
reflection_workflow = StateGraph(ReflectionState)

# Add nodes
reflection_workflow.add_node("analyze", analyze_conversation)
reflection_workflow.add_node("patterns", identify_patterns)
reflection_workflow.add_node("recommendations", generate_recommendations)

# Add edges
reflection_workflow.add_edge(START, "analyze")
reflection_workflow.add_edge("analyze", "patterns")
reflection_workflow.add_edge("patterns", "recommendations")
reflection_workflow.add_edge("recommendations", END)

# Compile reflection graph
reflection_graph = reflection_workflow.compile()

async def reflect_on_conversation(
    messages: List[BaseMessage],
    contact_id: str
) -> Dict[str, Any]:
    """Run reflection analysis on a conversation"""
    try:
        state = {
            "messages": messages,
            "contact_id": contact_id
        }
        
        result = await reflection_graph.ainvoke(state)
        
        return result.get("extracted_insights", {})
        
    except Exception as e:
        logger.error("Reflection failed", error=str(e))
        return {}

# Export
__all__ = ["reflection_graph", "reflect_on_conversation", "ReflectionState"]