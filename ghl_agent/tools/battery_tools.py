"""Battery calculation and consultation tools"""
from typing import Dict, List, Optional, Any
from langchain_core.tools import tool
import structlog

logger = structlog.get_logger()

# Equipment power consumption in watts
EQUIPMENT_CONSUMPTION = {
    "nevera": 300,
    "tv": 70,
    "abanico": 60,
    "celulares": 15,
    "bombilla_led": 10,
    "freezer": 300,
    "microondas": 1000,
    "computadora": 150,
    "router_internet": 20,
    "cafetera": 800,
    "lavadora": 500,
    "aire_acondicionado_pequeno": 1000,
    "ventilador_techo": 75
}

# Battery options
BATTERY_OPTIONS = [
    {
        "model": "EcoFlow DELTA 2",
        "capacity_wh": 1024,
        "price_range": "$999 - $1,199",
        "best_for": "apartamento",
        "features": ["Portátil", "Recarga por LUMA en 1.2 horas", "Múltiples salidas AC/USB"]
    },
    {
        "model": "Jackery Explorer 2000 Pro",
        "capacity_wh": 2160,
        "price_range": "$2,199 - $2,499",
        "best_for": "apartamento",
        "features": ["Ultra portátil", "Carga rápida", "Panel solar opcional"]
    },
    {
        "model": "BLUETTI AC200P",
        "capacity_wh": 2000,
        "price_range": "$1,799 - $1,999",
        "best_for": "casa",
        "features": ["Gran capacidad", "Múltiples opciones de carga", "Inversor potente"]
    },
    {
        "model": "Goal Zero Yeti 3000X",
        "capacity_wh": 3032,
        "price_range": "$3,199 - $3,499",
        "best_for": "casa",
        "features": ["Alta capacidad", "Expansible", "Compatible con paneles solares"]
    },
    {
        "model": "EcoFlow DELTA Pro",
        "capacity_wh": 3600,
        "price_range": "$3,599 - $3,999",
        "best_for": "casa",
        "features": ["Capacidad profesional", "Expandible a 25kWh", "Smart Home Ready"]
    },
    {
        "model": "Anker PowerHouse 767",
        "capacity_wh": 2048,
        "price_range": "$1,999 - $2,299",
        "best_for": "ambos",
        "features": ["10 años garantía", "Carga ultra rápida", "App control"]
    }
]


@tool
def calculate_battery_runtime(equipment_list: List[str], battery_capacity_wh: float) -> Dict[str, Any]:
    """
    Calculate how long a battery will last with given equipment.
    
    Args:
        equipment_list: List of equipment names in Spanish (e.g., ["nevera", "tv", "abanico"])
        battery_capacity_wh: Battery capacity in watt-hours
    
    Returns:
        Dictionary with consumption details and runtime
    """
    try:
        total_consumption = 0
        equipment_details = []
        unknown_equipment = []
        
        for equipment in equipment_list:
            equipment_lower = equipment.lower().strip()
            if equipment_lower in EQUIPMENT_CONSUMPTION:
                watts = EQUIPMENT_CONSUMPTION[equipment_lower]
                total_consumption += watts
                equipment_details.append({
                    "name": equipment,
                    "watts": watts
                })
            else:
                unknown_equipment.append(equipment)
        
        if total_consumption > 0:
            runtime_hours = battery_capacity_wh / total_consumption
            runtime_formatted = f"{runtime_hours:.1f} horas"
            
            # Convert to hours and minutes
            hours = int(runtime_hours)
            minutes = int((runtime_hours - hours) * 60)
            runtime_detailed = f"{hours} horas y {minutes} minutos"
        else:
            runtime_hours = 0
            runtime_formatted = "No se puede calcular"
            runtime_detailed = "No se puede calcular"
        
        return {
            "total_consumption_watts": total_consumption,
            "equipment_details": equipment_details,
            "unknown_equipment": unknown_equipment,
            "runtime_hours": runtime_hours,
            "runtime_formatted": runtime_formatted,
            "runtime_detailed": runtime_detailed,
            "battery_capacity_wh": battery_capacity_wh
        }
        
    except Exception as e:
        logger.error("Error calculating battery runtime", error=str(e))
        return {
            "error": f"Error en el cálculo: {str(e)}",
            "total_consumption_watts": 0,
            "runtime_hours": 0
        }


@tool
def recommend_battery_system(housing_type: str, total_consumption_watts: float, budget: Optional[str] = None) -> Dict[str, Any]:
    """
    Recommend appropriate battery systems based on housing type and consumption.
    
    Args:
        housing_type: "casa" or "apartamento"
        total_consumption_watts: Total power consumption in watts
        budget: Optional budget range
    
    Returns:
        Dictionary with battery recommendations
    """
    try:
        recommendations = []
        
        # Calculate minimum battery capacity needed for 6-8 hours
        min_capacity_6h = total_consumption_watts * 6
        min_capacity_8h = total_consumption_watts * 8
        
        # Filter batteries based on housing type and capacity
        for battery in BATTERY_OPTIONS:
            if battery["best_for"] in [housing_type, "ambos"]:
                if battery["capacity_wh"] >= min_capacity_6h:
                    runtime = battery["capacity_wh"] / total_consumption_watts
                    recommendations.append({
                        "model": battery["model"],
                        "capacity_wh": battery["capacity_wh"],
                        "runtime_hours": round(runtime, 1),
                        "price_range": battery["price_range"],
                        "features": battery["features"],
                        "suitable": runtime >= 6
                    })
        
        # Sort by runtime
        recommendations.sort(key=lambda x: x["runtime_hours"], reverse=True)
        
        # Additional recommendations based on housing type
        installation_notes = []
        if housing_type == "apartamento":
            installation_notes.append("Recomendamos baterías portátiles que se recargan fácilmente con LUMA")
            installation_notes.append("No requieren instalación permanente ni permisos")
        else:
            installation_notes.append("Puede considerar sistema con placas solares para recarga automática")
            installation_notes.append("También compatible con generador o conexión a LUMA")
            installation_notes.append("Instalación profesional disponible")
        
        return {
            "housing_type": housing_type,
            "total_consumption_watts": total_consumption_watts,
            "minimum_capacity_6h": min_capacity_6h,
            "minimum_capacity_8h": min_capacity_8h,
            "recommendations": recommendations[:3],  # Top 3 recommendations
            "installation_notes": installation_notes
        }
        
    except Exception as e:
        logger.error("Error recommending battery system", error=str(e))
        return {
            "error": f"Error en la recomendación: {str(e)}",
            "recommendations": []
        }


@tool
def format_consultation_request(name: str, phone: str, email: str, housing_type: str, equipment_list: List[str]) -> str:
    """
    Format customer information for consultation scheduling.
    
    Args:
        name: Customer name
        phone: Customer phone
        email: Customer email
        housing_type: "casa" or "apartamento"
        equipment_list: List of equipment to power
    
    Returns:
        Formatted message for the consultation team
    """
    equipment_text = ", ".join(equipment_list) if equipment_list else "No especificado"
    
    message = f"""
🔋 NUEVA CONSULTA DE BATERÍA

Cliente: {name}
Teléfono: {phone}
Email: {email}
Tipo de vivienda: {housing_type}
Equipos a energizar: {equipment_text}

El cliente está interesado en recibir orientación personalizada sobre sistemas de batería.
"""
    
    return message.strip()


@tool
def update_conversation_state(
    housing_type: Optional[str] = None,
    equipment_list: Optional[List[str]] = None,
    customer_name: Optional[str] = None,
    customer_phone: Optional[str] = None,
    interested_in_consultation: Optional[bool] = None
) -> str:
    """
    Update conversation state with extracted information.
    
    Args:
        housing_type: "casa" or "apartamento" if mentioned
        equipment_list: List of equipment mentioned (e.g., ["nevera", "abanicos", "luces"])
        customer_name: Customer's name if provided
        customer_phone: Customer's phone if provided
        interested_in_consultation: True if customer wants consultation
        
    Returns:
        Confirmation of what was updated
    """
    updates = []
    
    if housing_type:
        updates.append(f"housing_type: {housing_type}")
    if equipment_list:
        updates.append(f"equipment: {', '.join(equipment_list)}")
    if customer_name:
        updates.append(f"name: {customer_name}")
    if customer_phone:
        updates.append(f"phone: {customer_phone}")
    if interested_in_consultation is not None:
        updates.append(f"consultation: {'yes' if interested_in_consultation else 'no'}")
    
    if updates:
        return f"State updated: {'; '.join(updates)}"
    return "No updates provided"


# Export all tools
BATTERY_TOOLS = [
    calculate_battery_runtime,
    recommend_battery_system,
    format_consultation_request,
    update_conversation_state
]