import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the LangGraph Business Analysis System"""
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral:7b")
    
    # Search Configuration
    SEARCH_MAX_RESULTS: int = int(os.getenv("SEARCH_MAX_RESULTS", "10"))
    SEARCH_REGION: str = os.getenv("SEARCH_REGION", "wt-wt")
    SEARCH_SAFESEARCH: str = os.getenv("SEARCH_SAFESEARCH", "moderate")
    
    # PDF Configuration
    PDF_OUTPUT_DIR: str = os.getenv("PDF_OUTPUT_DIR", "./reports")
    PDF_TEMPLATE_DIR: str = os.getenv("PDF_TEMPLATE_DIR", "./templates")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/business_analysis.log")
    
    # System Configuration
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    RATE_LIMIT_DELAY: float = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))
    
    # LLM Configuration
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """Get model configuration dictionary"""
        return {
            "model": cls.OLLAMA_MODEL,
            "base_url": cls.OLLAMA_BASE_URL,
            "temperature": cls.LLM_TEMPERATURE,
            "num_predict": cls.LLM_MAX_TOKENS,
        }
    
    @classmethod
    def get_search_config(cls) -> Dict[str, Any]:
        """Get search configuration dictionary"""
        return {
            "max_results": cls.SEARCH_MAX_RESULTS,
            "region": cls.SEARCH_REGION,
            "safesearch": cls.SEARCH_SAFESEARCH,
        }
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist"""
        directories = [
            cls.PDF_OUTPUT_DIR,
            cls.PDF_TEMPLATE_DIR,
            os.path.dirname(cls.LOG_FILE),
        ]
        
        for directory in directories:
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """Validate configuration and return status"""
        status = {
            "ollama_accessible": False,
            "directories_created": False,
            "environment_loaded": False,
        }
        
        try:
            # Check if directories can be created
            cls.ensure_directories()
            status["directories_created"] = True
        except Exception:
            pass
        
        # Check if environment variables are loaded
        if cls.OLLAMA_BASE_URL and cls.OLLAMA_MODEL:
            status["environment_loaded"] = True
        
        # Note: We don't check Ollama accessibility here as it might not be running
        # This should be checked in the actual model interface
        
        return status