"""
Database utility functions for the infrastructure layer.
"""

import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

from app.infrastructures.constants.database import QUERY_TIMEOUT
from app.infrastructures.errors.database import DatabaseQueryError

# Type variables for better type hinting
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

# Setup logger
logger = logging.getLogger(__name__)


def with_db_transaction(func: F) -> F:
    """
    Decorator to handle database transactions.
    
    Args:
        func: The function to wrap with transaction handling
    
    Returns:
        Wrapped function with transaction management
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        from app.infrastructures.sqlite_db.database import get_db_session
        
        async with get_db_session() as session:
            try:
                kwargs["session"] = session
                result = await func(*args, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                logger.error(f"Database transaction error: {str(e)}")
                raise
    
    return wrapper  # type: ignore


def with_query_timeout(timeout: int = QUERY_TIMEOUT) -> Callable[[F], F]:
    """
    Decorator to add a timeout to database queries.
    
    Args:
        timeout: Maximum time in seconds for query execution
    
    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                # Create a task for the query
                result = await func(*args, **kwargs)
                
                # Check if the query took too long
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    logger.warning(
                        f"Query took {elapsed_time:.2f}s, which exceeds the "
                        f"timeout of {timeout}s: {func.__name__}"
                    )
                
                return result
            except Exception as e:
                elapsed_time = time.time() - start_time
                logger.error(
                    f"Query failed after {elapsed_time:.2f}s: {func.__name__}, "
                    f"Error: {str(e)}"
                )
                # Re-raise as a database query error
                raise DatabaseQueryError(
                    query=func.__name__,
                    detail=f"Query failed after {elapsed_time:.2f}s: {str(e)}"
                )
        
        return wrapper  # type: ignore
    
    return decorator
