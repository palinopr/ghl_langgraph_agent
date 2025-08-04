"""Configuration loader for the GHL Agent"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field
import structlog

logger = structlog.get_logger()

class BusinessConfig(BaseModel):
    """Business configuration"""
    name: str
    email: str
    phone: str
    timezone: str
    language: str = "es"

class QualificationConfig(BaseModel):
    """Lead qualification settings"""
    min_budget: int = 5000
    max_response_time: int = 300
    business_hours: Dict[str, Any]

class CalendarConfig(BaseModel):
    """Calendar settings"""
    appointment_duration: int = 60
    buffer_time: int = 15
    days_ahead: int = 7
    preferred_slots: Dict[str, str]

class MemoryConfig(BaseModel):
    """Memory persistence settings"""
    enable_persistence: bool = True
    store_type: str = "memory"
    retention_days: int = 90

class BehaviorConfig(BaseModel):
    """Agent behavior settings"""
    enable_human_review: bool = False
    parallel_tool_calls: bool = True
    max_retry_attempts: int = 3
    response_delay: int = 2

class Config(BaseModel):
    """Complete configuration"""
    business: BusinessConfig
    qualification: QualificationConfig
    products: Dict[str, Any]
    equipment_consumption: Dict[str, int]
    templates: Dict[str, str]
    triage: Dict[str, Any]
    calendar: CalendarConfig
    integrations: Dict[str, Any]
    memory: MemoryConfig
    behavior: BehaviorConfig
    logging: Dict[str, Any]

class ConfigLoader:
    """Load and manage configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config loader
        
        Args:
            config_path: Path to config file. If None, looks in standard locations
        """
        self.config_path = self._find_config_file(config_path)
        self._raw_config = None
        self._config = None
        self._load_config()
    
    def _find_config_file(self, config_path: Optional[str] = None) -> Path:
        """Find configuration file"""
        if config_path:
            return Path(config_path)
        
        # Standard locations to check
        locations = [
            Path("ghl_agent/config.yaml"),
            Path("config.yaml"),
            Path.home() / ".ghl_agent" / "config.yaml",
            Path("/etc/ghl_agent/config.yaml"),
        ]
        
        for location in locations:
            if location.exists():
                logger.info(f"Found config file at {location}")
                return location
        
        # Default location
        default = Path("ghl_agent/config.yaml")
        logger.warning(f"No config file found, using default at {default}")
        return default
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file not found at {self.config_path}, using defaults")
                self._use_defaults()
                return
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._raw_config = yaml.safe_load(f)
            
            # Substitute environment variables
            self._substitute_env_vars()
            
            # Validate and create config object
            self._config = Config(**self._raw_config)
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._use_defaults()
    
    def _substitute_env_vars(self):
        """Substitute environment variables in config"""
        def substitute_in_dict(d: Dict[str, Any]):
            for key, value in d.items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_var = value[2:-1]
                    env_value = os.getenv(env_var)
                    if env_value:
                        d[key] = env_value
                    else:
                        logger.warning(f"Environment variable {env_var} not found")
                elif isinstance(value, dict):
                    substitute_in_dict(value)
        
        if self._raw_config:
            substitute_in_dict(self._raw_config)
    
    def _use_defaults(self):
        """Use default configuration"""
        self._raw_config = {
            "business": {
                "name": "Battery Solutions",
                "email": "info@example.com",
                "phone": "+1234567890",
                "timezone": "America/New_York",
                "language": "es"
            },
            "qualification": {
                "min_budget": 5000,
                "max_response_time": 300,
                "business_hours": {
                    "start": "09:00",
                    "end": "18:00",
                    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                }
            },
            "products": {},
            "equipment_consumption": {
                "nevera": 300,
                "televisor": 70,
                "abanico": 60
            },
            "templates": {
                "greeting": "¡Hola! Soy tu especialista en baterías. ¿Cómo puedo ayudarte?"
            },
            "triage": {
                "auto_respond": ["información", "precio"],
                "notify_human": ["urgente", "problema"],
                "ignore": ["spam"]
            },
            "calendar": {
                "appointment_duration": 60,
                "buffer_time": 15,
                "days_ahead": 7,
                "preferred_slots": {}
            },
            "integrations": {
                "ghl": {
                    "location_id": os.getenv("GHL_LOCATION_ID", ""),
                    "calendar_id": os.getenv("GHL_CALENDAR_ID", "")
                }
            },
            "memory": {
                "enable_persistence": True,
                "store_type": "memory",
                "retention_days": 90
            },
            "behavior": {
                "enable_human_review": False,
                "parallel_tool_calls": True,
                "max_retry_attempts": 3,
                "response_delay": 2
            },
            "logging": {
                "level": "INFO",
                "enable_langsmith": True,
                "trace_all_conversations": True
            }
        }
        self._config = Config(**self._raw_config)
    
    @property
    def config(self) -> Config:
        """Get configuration object"""
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation
        
        Args:
            key: Dot-separated key (e.g., "business.name")
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        parts = key.split('.')
        value = self._raw_config
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def reload(self):
        """Reload configuration from file"""
        logger.info("Reloading configuration")
        self._load_config()

# Global config instance
_config_loader = None

def get_config() -> Config:
    """Get global configuration"""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader.config

def get_config_value(key: str, default: Any = None) -> Any:
    """Get specific configuration value"""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader.get(key, default)