import logging
import os
from typing import Any, Dict, Optional

import structlog

from api.config import settings

# Initialize the structlog logger with a custom formatter
logger = structlog.get_logger(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.KeyValueRenderer(key_prefix=""),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# Set up the default logging level from environment variable
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level))

# Define a custom logger function to handle logging with structlog
def log(level: str, message: str, context: Optional[Dict[str, Any]] = None):
    """Logs a message at the specified level with optional context.

    Args:
        level (str): The log level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
        message (str): The log message to be logged.
        context (Optional[Dict[str, Any]]): Additional context to be included with the log message.

    Returns:
        None
    """
    if context is None:
        context = {}
    logger.log(level, message, **context)

# Define specific logger functions for different log levels
def debug(message: str, context: Optional[Dict[str, Any]] = None):
    """Logs a debug message with optional context."""
    log("DEBUG", message, context)

def info(message: str, context: Optional[Dict[str, Any]] = None):
    """Logs an informational message with optional context."""
    log("INFO", message, context)

def warning(message: str, context: Optional[Dict[str, Any]] = None):
    """Logs a warning message with optional context."""
    log("WARNING", message, context)

def error(message: str, context: Optional[Dict[str, Any]] = None):
    """Logs an error message with optional context."""
    log("ERROR", message, context)

def critical(message: str, context: Optional[Dict[str, Any]] = None):
    """Logs a critical message with optional context."""
    log("CRITICAL", message, context)