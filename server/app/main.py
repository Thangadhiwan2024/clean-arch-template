"""Main entry point for the Project Management Service."""

from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import logging
import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.infrastructures.sqlite_db.database import init_db
from app.routers.v1.errors import setup_error_handlers, log_unexpected_error
from app.routers.v1 import router as v1_router
from app.settings import get_settings
from app.shared.utils.logging import request_id_middleware, RequestIdFilter


def setup_middlewares(app: FastAPI, settings) -> None:
    """Setup middleware for the application."""
    # Add request ID middleware
    app.middleware("http")(request_id_middleware)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
        expose_headers=settings.CORS_EXPOSE_HEADERS + ["X-Request-ID"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Set application start time
    app.state.start_time = datetime.now()

    # Initialize database with proper error handling
    try:
        await init_db()
    except Exception as e:
        logging.critical("Database initialization failed: %s", str(e), exc_info=True)
        raise

    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    # Configure logging with request ID filter
    request_id_filter = RequestIdFilter()
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(levelname)s - %(name)s - [request_id=%(request_id)s] - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    
    # Add the request ID filter to the root logger
    root_logger = logging.getLogger()
    root_logger.addFilter(request_id_filter)

    app = FastAPI(
        lifespan=lifespan,
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.PROJECT_MANAGEMENT_SERVICE_DEBUG,
    )

    # Setup middlewares
    setup_middlewares(app, settings)

    return app


app = create_app()
app.include_router(v1_router)

# Setup custom error handlers
setup_error_handlers(app)



@app.get("/")
async def read_root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to the Project Management Service!"}


@app.get("/health")
async def health_check(request: Request) -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Dict containing service health information including:
        - status: Current service status
        - version: Application version
        - start_time: Service start time in ISO format
        - uptime: Service uptime in hh:mm:ss format
    """
    uptime_seconds = (datetime.now() - request.app.state.start_time).total_seconds()
    uptime_str = str(timedelta(seconds=int(uptime_seconds)))
    return {
        "status": "healthy",
        "version": getattr(request.app, "version", "unknown"),
        "start_time": request.app.state.start_time.isoformat(),
        "uptime": uptime_str,
    }


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.PROJECT_MANAGEMENT_SERVICE_HOST,
        port=settings.PROJECT_MANAGEMENT_SERVICE_PORT,
        reload=settings.PROJECT_MANAGEMENT_SERVICE_DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
