import hashlib
import json
import os
import re
from typing import Any, Dict, List, Optional, Union

from api.config import settings
from openai import OpenAI

# Import OpenAI library with version 1.52.0
openai = OpenAI()

# Import configuration settings from config.py
from api.config import settings

# For logging
import structlog

logger = structlog.get_logger()

def generate_text(text: str, model: str = "text-davinci-003") -> str:
    """Generates text using the OpenAI API.

    Args:
        text (str): The text to generate.
        model (str, optional): The OpenAI model to use. Defaults to "text-davinci-003".

    Returns:
        str: The generated text.
    """
    try:
        response = openai.completions.create(
            model=model,
            prompt=text,
            max_tokens=1024,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise HTTPException(status_code=400, detail=f"Error generating text: {e}")

def translate_text(text: str, source_language: str, target_language: str) -> str:
    """Translates text from one language to another using the OpenAI API.

    Args:
        text (str): The text to translate.
        source_language (str): The source language code.
        target_language (str): The target language code.

    Returns:
        str: The translated text.
    """
    try:
        response = openai.translations.create(
            model="gpt-3.5-turbo",
            input=text,
            source_language=source_language,
            target_language=target_language,
        )
        return response.translation
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        raise HTTPException(status_code=400, detail=f"Error translating text: {e}")

def summarize_text(text: str, model: str = "text-davinci-003") -> str:
    """Summarizes a given text using the OpenAI API.

    Args:
        text (str): The text to summarize.
        model (str, optional): The OpenAI model to use. Defaults to "text-davinci-003".

    Returns:
        str: The summarized text.
    """
    try:
        response = openai.completions.create(
            model=model,
            prompt=f"Summarize this text: {text}",
            max_tokens=1024,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        raise HTTPException(status_code=400, detail=f"Error summarizing text: {e}")

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validates an email address using a regular expression.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None

def sanitize_input(data: Any) -> Any:
    """Sanitizes input data by converting it to a string and stripping whitespace.

    Args:
        data (Any): The input data to sanitize.

    Returns:
        Any: The sanitized data.
    """
    if isinstance(data, str):
        return data.strip()
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, dict):
        return {key: sanitize_input(value) for key, value in data.items()}
    else:
        return data

def format_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Formats the API response into a consistent structure.

    Args:
        response (Dict[str, Any]): The API response to format.

    Returns:
        Dict[str, Any]: The formatted response.
    """
    formatted_response = {}
    for key, value in response.items():
        if isinstance(value, (list, dict)):
            formatted_response[key] = format_response(value)
        else:
            formatted_response[key] = str(value).strip()
    return formatted_response

def get_api_key() -> str:
    """Retrieves the OpenAI API key from the environment variables.

    Returns:
        str: The OpenAI API key.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return api_key

def get_database_url() -> str:
    """Retrieves the database connection URL from the environment variables.

    Returns:
        str: The database connection URL.
    """
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set.")
    return database_url

def get_jwt_secret_key() -> str:
    """Retrieves the JWT secret key from the environment variables.

    Returns:
        str: The JWT secret key.
    """
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY environment variable is not set.")
    return secret_key

def get_launchdarkly_sdk_key() -> str:
    """Retrieves the LaunchDarkly SDK key from the environment variables.

    Returns:
        str: The LaunchDarkly SDK key.
    """
    sdk_key = os.environ.get("LAUNCHDARKLY_SDK_KEY")
    if not sdk_key:
        raise ValueError("LAUNCHDARKLY_SDK_KEY environment variable is not set.")
    return sdk_key

def get_launchdarkly_environment_key() -> str:
    """Retrieves the LaunchDarkly environment key from the environment variables.

    Returns:
        str: The LaunchDarkly environment key.
    """
    env_key = os.environ.get("LAUNCHDARKLY_ENV_KEY")
    if not env_key:
        raise ValueError("LAUNCHDARKLY_ENV_KEY environment variable is not set.")
    return env_key

def get_redis_url() -> str:
    """Retrieves the Redis connection URL from the environment variables.

    Returns:
        str: The Redis connection URL.
    """
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set.")
    return redis_url

def get_server_port() -> int:
    """Retrieves the server port from the environment variables.

    Returns:
        int: The server port.
    """
    port = os.environ.get("PORT")
    if not port:
        raise ValueError("PORT environment variable is not set.")
    return int(port)

def get_api_endpoint_url(endpoint: str) -> str:
    """Constructs the full API endpoint URL based on the base URL and the provided endpoint.

    Args:
        endpoint (str): The API endpoint path.

    Returns:
        str: The full API endpoint URL.
    """
    base_url = settings.API_BASE_URL
    return f"{base_url}{endpoint}"

def get_api_endpoint_headers() -> Dict[str, str]:
    """Retrieves the API endpoint headers, including authentication tokens (if applicable).

    Returns:
        Dict[str, str]: The API endpoint headers.
    """
    headers = {"Content-Type": "application/json"}
    auth_token = settings.AUTH_TOKEN
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    return headers

def get_cache_key(key: str) -> str:
    """Generates a unique cache key based on the provided key.

    Args:
        key (str): The base key.

    Returns:
        str: The unique cache key.
    """
    return hashlib.sha256(key.encode()).hexdigest()

def get_cache_data(key: str, cache: Any) -> Optional[Union[str, Dict[str, Any]]]:
    """Retrieves cached data based on the provided key.

    Args:
        key (str): The cache key.
        cache (Any): The cache object (e.g., Redis).

    Returns:
        Optional[Union[str, Dict[str, Any]]]: The cached data, or None if not found.
    """
    cached_data = cache.get(key)
    if cached_data:
        try:
            return json.loads(cached_data)
        except json.JSONDecodeError:
            return cached_data
    return None

def set_cache_data(key: str, data: Union[str, Dict[str, Any]], cache: Any):
    """Stores data in the cache with the provided key.

    Args:
        key (str): The cache key.
        data (Union[str, Dict[str, Any]]): The data to cache.
        cache (Any): The cache object (e.g., Redis).
    """
    cache.set(key, json.dumps(data))

def clear_cache_data(key: str, cache: Any):
    """Removes data from the cache based on the provided key.

    Args:
        key (str): The cache key.
        cache (Any): The cache object (e.g., Redis).
    """
    cache.delete(key)