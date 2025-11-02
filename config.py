"""
Configuration module for Multi-Modal AI Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the multi-modal agent"""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Model Settings
    USE_LOCAL_MODELS = os.getenv("USE_LOCAL_MODELS", "true").lower() == "true"
    CLIP_MODEL = os.getenv("CLIP_MODEL", "openai/clip-vit-large-patch14")
    BLIP_MODEL = os.getenv("BLIP_MODEL", "Salesforce/blip-image-captioning-large")

    # Agent Settings
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "5"))
    VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"

    # Device Configuration
    DEVICE = "cuda" if os.getenv("USE_GPU", "false").lower() == "true" else "cpu"

    # App Settings
    APP_TITLE = "Multi-Modal AI Agent"
    APP_DESCRIPTION = """
    This agent can understand images and text, using:
    - CLIP for visual-text matching
    - BLIP for image captioning
    - LangChain agents with multiple tools
    """

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.USE_LOCAL_MODELS and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY required when USE_LOCAL_MODELS=false")
        return True

# Validate config on import
Config.validate()
