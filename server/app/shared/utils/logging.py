"""Logging utilities for the application."""

import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
import threading

from fastapi import Request
import uuid


class RequestIdFilter(logging.Filter):
    """Filter that adds request_id to log records."""
    
    _thread_local = threading.local()
    
    @classmethod
    def set_request_id(cls, request_id: str):
        """Set the request ID for the current thread."""
        cls._thread_local.request_id = request_id
    
    @classmethod
    def get_request_id(cls):
        """Get the request ID for the current thread."""
        return getattr(cls._thread_local, "request_id", "no-request-id")
    
    def filter(self, record):
        """Add request_id to the log record."""
        if not hasattr(record, "request_id"):
            record.request_id = self.get_request_id()
        return True


class StructuredLogger:
    """A structured logger that adds context to log messages."""
    
    def __init__(self, name: str):
        """Initialize the structured logger with a name."""
        self.logger = logging.getLogger(name)
    
    def _format_log(self, level: str, message: str, request: Optional[Request] = None, 
                   extra: Optional[Dict[str, Any]] = None, exc_info: Any = None) -> Dict[str, Any]:
        """Format a log message with additional context."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
        }
        
        # Add request context if available
        if request:
            log_data.update({
                "request_id": getattr(request.state, "request_id", str(uuid.uuid4())),
                "method": request.method,
                "path": str(request.url.path),
                "client_ip": request.client.host if request.client else None,
            })
        
        # Add any extra context
        if extra:
            log_data.update(extra)
            
        return log_data
    
    def info(self, message: str, request: Optional[Request] = None, 
             extra: Optional[Dict[str, Any]] = None) -> None:
        """Log an info message with context."""
        log_data = self._format_log("INFO", message, request, extra)
        self.logger.info(json.dumps(log_data))
    
    def warning(self, message: str, request: Optional[Request] = None, 
               extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a warning message with context."""
        log_data = self._format_log("WARNING", message, request, extra)
        self.logger.warning(json.dumps(log_data))
    
    def error(self, message: str, request: Optional[Request] = None, 
             extra: Optional[Dict[str, Any]] = None, exc_info: Any = None) -> None:
        """Log an error message with context."""
        log_data = self._format_log("ERROR", message, request, extra)
        self.logger.error(json.dumps(log_data), exc_info=exc_info)
    
    def debug(self, message: str, request: Optional[Request] = None, 
             extra: Optional[Dict[str, Any]] = None) -> None:
        """Log a debug message with context."""
        log_data = self._format_log("DEBUG", message, request, extra)
        self.logger.debug(json.dumps(log_data))


def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger with the given name."""
    return StructuredLogger(name)


# Generate a request ID middleware for FastAPI
async def request_id_middleware(request: Request, call_next):
    """Middleware to add a request ID to each request."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Set the request ID for the current thread
    RequestIdFilter.set_request_id(request_id)
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
