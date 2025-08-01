"""Battery product knowledge base from manufacturer documentation"""
from typing import Dict, List, Optional, Any
from datetime import datetime

# SUNBEAT STACK ENERGY PRO - Modular Stackable Systems
STACKABLE_BATTERIES = {
    "stack_10k": {
        "name": "Stack Energy Pro 10K",
        "capacity_kwh": 10.24,
        "capacity_wh": 10240,
        "modules": 2,  # 2x 5.12kWh modules
        "voltage": "51.2V",
        "battery_type": "LiFePO4",
        "price": "$12,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema modular expandible",
            "Pantalla LCD integrada",
            "Comunicación RS485/CAN",
            "Compatible con inversores principales",
            "Resistente al agua",
            "Control por aplicación móvil"
        ],
        "best_for": "apartamento",
        "installation": "Profesional requerida"
    },
    "stack_15k": {
        "name": "Stack Energy Pro 15K",
        "capacity_kwh": 15.36,
        "capacity_wh": 15360,
        "modules": 3,  # 3x 5.12kWh modules
        "voltage": "51.2V",
        "battery_type": "LiFePO4",
        "price": "$16,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema modular expandible",
            "Pantalla LCD integrada",
            "Comunicación RS485/CAN",
            "Compatible con inversores principales",
            "Resistente al agua",
            "Control por aplicación móvil"
        ],
        "best_for": "casa",
        "installation": "Profesional requerida"
    },
    "stack_20k": {
        "name": "Stack Energy Pro 20K",
        "capacity_kwh": 20.48,
        "capacity_wh": 20480,
        "modules": 4,  # 4x 5.12kWh modules
        "voltage": "51.2V",
        "battery_type": "LiFePO4",
        "price": "$18,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema modular expandible",
            "Pantalla LCD integrada",
            "Comunicación RS485/CAN",
            "Compatible con inversores principales",
            "Resistente al agua",
            "Control por aplicación móvil"
        ],
        "best_for": "casa",
        "installation": "Profesional requerida"
    }
}

# BLUETTI ENERGY TANK - Stackable Systems
BLUETTI_STACKABLE = {
    "bluetti_10k": {
        "name": "BLUETTI Energy Tank 10K",
        "capacity_kwh": 10,
        "capacity_wh": 10000,
        "modules": 3,
        "battery_type": "LiFePO4",
        "price": "$12,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema modular BLUETTI",
            "Expandible hasta 30kWh",
            "Resistente al agua",
            "Control por aplicación móvil",
            "Compatible con inversores BLUETTI"
        ],
        "best_for": "ambos",
        "installation": "Profesional requerida"
    },
    "bluetti_15k": {
        "name": "BLUETTI Energy Tank 15K",
        "capacity_kwh": 15,
        "capacity_wh": 15000,
        "modules": 5,
        "battery_type": "LiFePO4",
        "price": "$16,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema modular BLUETTI",
            "Expandible hasta 30kWh",
            "Resistente al agua",
            "Control por aplicación móvil",
            "Compatible con inversores BLUETTI"
        ],
        "best_for": "casa",
        "installation": "Profesional requerida"
    },
    "bluetti_20k": {
        "name": "BLUETTI Energy Tank 20K",
        "capacity_kwh": 20,
        "capacity_wh": 20000,
        "modules": 7,
        "battery_type": "LiFePO4",
        "price": "$18,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema modular BLUETTI",
            "Expandible hasta 30kWh",
            "Resistente al agua",
            "Control por aplicación móvil",
            "Compatible con inversores BLUETTI"
        ],
        "best_for": "casa",
        "installation": "Profesional requerida"
    }
}

# FORTRESS POWER - Fixed Wall Systems
FORTRESS_BATTERIES = {
    "fortress_9.6k": {
        "name": "Fortress Power 9.6K",
        "capacity_kwh": 9.6,
        "capacity_wh": 9600,
        "battery_type": "LiFePO4",
        "price": "$15,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema de montaje en pared",
            "Diseño compacto",
            "Resistente al agua",
            "Control por aplicación móvil",
            "Compatible con múltiples inversores"
        ],
        "best_for": "apartamento",
        "installation": "Profesional requerida"
    },
    "fortress_19.2k": {
        "name": "Fortress Power 19.2K",
        "capacity_kwh": 19.2,
        "capacity_wh": 19200,
        "battery_type": "LiFePO4",
        "price": "$21,999.00",
        "warranty_years": 15,
        "features": [
            "Sistema de montaje en pared",
            "Alta capacidad",
            "Resistente al agua",
            "Control por aplicación móvil",
            "Compatible con múltiples inversores"
        ],
        "best_for": "casa",
        "installation": "Profesional requerida"
    }
}

# PORTABLE POWER STATIONS - With Solar Option
PORTABLE_STATIONS = {
    "yeti_6000pro": {
        "name": "Goal Zero YETI 6000 PRO",
        "capacity_kwh": 6.071,
        "capacity_wh": 6071,
        "battery_type": "LiFePO4",
        "price": "$6,999.00",
        "price_with_install": "$6,999.00",
        "features": [
            "Portátil con ruedas",
            "6 salidas AC 110V",
            "Puertos USB múltiples",
            "Panel solar 400W incluido",
            "Transfer switch incluido",
            "Control por aplicación móvil",
            "Recarga por LUMA en 5.5 horas"
        ],
        "runtime_examples": {
            "nevera": "85 horas (55W)",
            "maquinas_medicas": "8 horas (55W)",
            "lavadora": "6 horas (1000W)"
        },
        "best_for": "ambos",
        "installation": "Instalación eléctrica incluida"
    },
    "gendome_home3000": {
        "name": "Gendome Home 3000",
        "capacity_kwh": 3.2,
        "capacity_wh": 3200,
        "battery_type": "LiFePO4",
        "price": "$4,999.00",
        "price_with_install": "$4,999.00",
        "features": [
            "Diseño compacto portátil",
            "4 salidas AC 110V",
            "Puertos USB múltiples",
            "Panel solar 400W incluido",
            "Transfer switch incluido",
            "Control por aplicación móvil",
            "Ideal para apartamentos"
        ],
        "runtime_examples": {
            "nevera": "58 horas (55W)",
            "maquinas_medicas": "8 horas (55W)",
            "lavadora": "3 horas (1000W)"
        },
        "best_for": "apartamento",
        "installation": "Instalación eléctrica incluida"
    },
    "oukitel_p5000pro": {
        "name": "OUKITEL P5000 Pro",
        "capacity_kwh": 5.12,
        "capacity_wh": 5120,
        "battery_type": "LiFePO4",
        "price": "$6,999.00",
        "price_with_install": "$6,999.00",
        "features": [
            "Portátil con ruedas",
            "5 salidas AC 110V",
            "Carga súper rápida",
            "Panel solar 400W incluido",
            "Transfer switch incluido",
            "Control por aplicación móvil",
            "UPS integrado"
        ],
        "runtime_examples": {
            "nevera": "85 horas (55W)",
            "maquinas_medicas": "8 horas (55W)",
            "lavadora": "5 horas (1000W)"
        },
        "best_for": "ambos",
        "installation": "Instalación eléctrica incluida"
    },
    "wattbricks_6000pro": {
        "name": "WATTBRICKS 6000Pro",
        "capacity_kwh": 6.0,
        "capacity_wh": 6000,
        "battery_type": "LiFePO4",
        "price": "$6,999.00",
        "price_with_install": "$6,999.00",
        "features": [
            "Portátil con ruedas",
            "6 salidas AC 110V",
            "Diseño modular",
            "Panel solar 400W incluido",
            "Transfer switch incluido",
            "Control por aplicación móvil",
            "Pantalla táctil"
        ],
        "runtime_examples": {
            "nevera": "109 horas (55W)",
            "maquinas_medicas": "8 horas (55W)",
            "lavadora": "6 horas (1000W)"
        },
        "best_for": "ambos",
        "installation": "Instalación eléctrica incluida"
    }
}

# SOLAR PANEL INSTALLATION PRICING
SOLAR_PANEL_PRICING = {
    8: 4000.00,
    9: 4500.00,
    10: 5000.00,
    11: 5500.00,
    12: 6000.00,
    13: 6500.00,
    14: 7000.00,
    15: 7500.00,
    16: 8000.00,
    17: 8500.00,
    18: 9000.00,
    19: 9500.00,
    20: 10000.00
}

# SALES COMMISSION STRUCTURE
COMMISSION_STRUCTURE = [
    {"min": 5000, "max": 9999, "commission": 350},
    {"min": 10000, "max": 14999, "commission": 450},
    {"min": 15000, "max": 19999, "commission": 600},
    {"min": 20000, "max": 24999, "commission": 800},
    {"min": 25000, "max": 29999, "commission": 1000},
    {"min": 30000, "max": 45000, "commission": 1200}
]

# TECHNICAL SPECIFICATIONS FROM MANUAL
SUNBEAT_TECHNICAL = {
    "module_specs": {
        "voltage": "51.2V",
        "capacity_ah": 100,
        "energy_wh": 5120,
        "dimensions": {
            "width_mm": 670,
            "depth_mm": 170,
            "height_mm": 430
        },
        "weight_kg": 53.2,
        "cell_type": "LiFePO4",
        "bms_features": [
            "Monitoreo en tiempo real",
            "Protección integral",
            "Balance pasivo",
            "Control de temperatura"
        ]
    },
    "safety_features": [
        "Protección contra sobrecarga",
        "Protección contra descarga profunda",
        "Protección contra cortocircuito",
        "Protección térmica",
        "Sistema de tierra obligatorio"
    ],
    "communication": {
        "protocols": ["RS485", "CAN"],
        "monitoring": "PC Software incluido",
        "display": "LCD integrado por módulo"
    },
    "installation_requirements": [
        "Instalación por personal certificado",
        "Área ventilada",
        "Temperatura: 10-45°C operación",
        "Humedad: 60±30%",
        "Evitar luz solar directa"
    ],
    "maintenance": {
        "cables": "Cada 6 meses",
        "connections": "Anualmente",
        "cleaning": "Cada 6-12 meses",
        "system_check": "Cada 6 meses"
    }
}

# Combine all battery products
ALL_BATTERY_PRODUCTS = {
    **STACKABLE_BATTERIES,
    **BLUETTI_STACKABLE,
    **FORTRESS_BATTERIES,
    **PORTABLE_STATIONS
}

def get_battery_by_capacity_range(min_wh: float, max_wh: float, housing_type: str = None) -> List[Dict[str, Any]]:
    """Get batteries within a specific capacity range"""
    suitable_batteries = []
    
    for battery_id, battery_info in ALL_BATTERY_PRODUCTS.items():
        if min_wh <= battery_info["capacity_wh"] <= max_wh:
            if housing_type is None or battery_info["best_for"] in [housing_type, "ambos"]:
                suitable_batteries.append({
                    "id": battery_id,
                    **battery_info
                })
    
    return sorted(suitable_batteries, key=lambda x: x["capacity_wh"])

def get_commission_for_sale(sale_amount: float) -> float:
    """Calculate commission based on sale amount"""
    for tier in COMMISSION_STRUCTURE:
        if tier["min"] <= sale_amount <= tier["max"]:
            return tier["commission"]
    
    # For sales above $45,000
    if sale_amount > 45000:
        return 1200
    
    return 0

def format_product_comparison(products: List[str]) -> str:
    """Format a comparison table of selected products"""
    comparison = "📊 COMPARACIÓN DE PRODUCTOS\n\n"
    
    for product_id in products:
        if product_id in ALL_BATTERY_PRODUCTS:
            product = ALL_BATTERY_PRODUCTS[product_id]
            comparison += f"**{product['name']}**\n"
            comparison += f"• Capacidad: {product['capacity_kwh']}kWh ({product['capacity_wh']}Wh)\n"
            comparison += f"• Precio: {product['price']}\n"
            comparison += f"• Garantía: {product['warranty_years']} años\n"
            comparison += f"• Mejor para: {product['best_for']}\n"
            comparison += f"• Características principales:\n"
            for feature in product['features'][:3]:
                comparison += f"  - {feature}\n"
            comparison += "\n"
    
    return comparison