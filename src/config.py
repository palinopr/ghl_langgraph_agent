import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()


class Settings(BaseSettings):
    # GoHighLevel Configuration
    ghl_api_key: str = os.getenv("GHL_API_KEY", "")
    ghl_location_id: str = os.getenv("GHL_LOCATION_ID", "")
    ghl_api_base_url: str = os.getenv("GHL_API_BASE_URL", "https://services.leadconnectorhq.com")
    ghl_calendar_id: str = os.getenv("GHL_CALENDAR_ID", "")
    
    # Meta Configuration
    meta_verify_token: str = os.getenv("META_VERIFY_TOKEN", "")
    meta_app_secret: str = os.getenv("META_APP_SECRET", "")
    
    # LLM Configuration
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    langchain_api_key: Optional[str] = os.getenv("LANGCHAIN_API_KEY")
    langchain_tracing_v2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    langchain_project: str = os.getenv("LANGCHAIN_PROJECT", "ghl-langgraph-agent")
    
    # Server Configuration
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    
    # Agent Configuration
    default_llm_model: str = "gpt-4-turbo"
    conversation_timeout_minutes: int = 30
    max_retries: int = 3
    timezone: str = os.getenv("TIMEZONE", "UTC")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Validate required configuration
def validate_config():
    """Validate that required configuration is present"""
    errors = []
    
    if not settings.ghl_api_key:
        errors.append("GHL_API_KEY is required")
    
    if not settings.ghl_location_id:
        errors.append("GHL_LOCATION_ID is required")
    
    if not settings.openai_api_key and not settings.anthropic_api_key:
        errors.append("Either OPENAI_API_KEY or ANTHROPIC_API_KEY is required")
    
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease set the required environment variables in your .env file")
        return False
    
    return True