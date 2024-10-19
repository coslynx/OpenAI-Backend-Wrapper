from typing import Optional
from pydantic import BaseSettings, Field, validator
from pathlib import Path
import os
import sys

# Import for logging
import structlog
from utils.logger import log, debug, info, warning, error, critical

# Import for OpenAI API interaction (using OpenAI v1.52.0)
from openai import OpenAI as OpenAI_v1_52_0

# Import for loading environment variables
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import for accessing configuration settings
from config.config import settings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    DATABASE_URL: Optional[str] = Field(None, env="DATABASE_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    LAUNCHDARKLY_SDK_KEY: Optional[str] = Field(None, env="LAUNCHDARKLY_SDK_KEY")
    LAUNCHDARKLY_ENV_KEY: Optional[str] = Field(None, env="LAUNCHDARKLY_ENV_KEY")
    REDIS_URL: Optional[str] = Field(None, env="REDIS_URL")
    PORT: int = Field(8000, env="PORT")
    API_BASE_URL: str = Field("http://localhost:8000", env="API_BASE_URL")  # Set the base URL for the API

    @validator("OPENAI_API_KEY")
    def validate_openai_api_key(cls, value):
        if not value:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        return value

    @validator("SECRET_KEY")
    def validate_secret_key(cls, value):
        if not value:
            raise ValueError("SECRET_KEY environment variable is not set.")
        return value

    class Config:
        env_file = ".env"

# Initialize the OpenAI client with the API key from settings
openai = OpenAI_v1_52_0(api_key=settings.OPENAI_API_KEY)

# Set up the logging system
logger = structlog.get_logger()

# Configure the application settings
settings = Settings()