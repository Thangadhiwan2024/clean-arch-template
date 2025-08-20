"""
Shared utility functions for date and time operations.
These utilities are not tied to any specific business logic.
"""

import datetime
from typing import Union


def format_datetime(dt: Union[datetime.datetime, str], format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object or string into a specific format.
    
    Args:
        dt: Datetime object or string to format
        format_str: Format string to use
    
    Returns:
        Formatted datetime string
    """
    if isinstance(dt, str):
        try:
            dt = datetime.datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except ValueError:
            # Try to parse common formats
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    dt = datetime.datetime.strptime(dt, fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Could not parse datetime string: {dt}")
    
    return dt.strftime(format_str)


def get_current_utc_datetime() -> datetime.datetime:
    """
    Get the current UTC datetime.
    
    Returns:
        Current UTC datetime
    """
    return datetime.datetime.now(datetime.timezone.utc)


def calculate_date_difference(
    start_date: Union[datetime.date, datetime.datetime, str],
    end_date: Union[datetime.date, datetime.datetime, str] = None
) -> int:
    """
    Calculate the number of days between two dates.
    
    Args:
        start_date: Start date
        end_date: End date, defaults to current date if None
    
    Returns:
        Number of days between the two dates
    """
    # Convert string dates to datetime objects if needed
    if isinstance(start_date, str):
        start_date = datetime.datetime.fromisoformat(start_date.replace('Z', '+00:00')).date()
    elif isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
    
    if end_date is None:
        end_date = datetime.date.today()
    elif isinstance(end_date, str):
        end_date = datetime.datetime.fromisoformat(end_date.replace('Z', '+00:00')).date()
    elif isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
    
    # Calculate the difference
    delta = end_date - start_date
    return delta.days
