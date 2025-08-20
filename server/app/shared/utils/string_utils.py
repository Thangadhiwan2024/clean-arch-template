"""
Shared utility functions for string operations.
These utilities are not tied to any specific business logic.
"""

import re
import uuid
from typing import Optional


def generate_uuid() -> str:
    """
    Generate a random UUID.
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())


def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    
    Args:
        text: Text to convert
    
    Returns:
        Slugified text
    """
    # Convert to lowercase
    text = text.lower()
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def truncate_string(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate a string to a maximum length, adding a suffix if truncated.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of the string
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def is_valid_uuid(value: str) -> bool:
    """
    Check if a string is a valid UUID.
    
    Args:
        value: String to check
    
    Returns:
        True if the string is a valid UUID, False otherwise
    """
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False
