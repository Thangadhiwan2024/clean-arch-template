# Clean Architecture Guide

This comprehensive guide explains the Clean Architecture principles, project structure, and error handling approach used in this template.

## Table of Contents

- [Project Structure](#project-structure)
- [Architecture Layers](#architecture-layers)
- [Request Flow](#request-flow)
- [Error, Constants, and Utils Organization](#error-constants-and-utils-organization)
- [Error Handling](#error-handling)

## Project Structure

```text
project_management_service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration utilities
│   ├── entities/               # Domain Layer - Business rules and models
│   │   ├── errors/             # Domain-specific errors
│   │   │   ├── base.py
│   │   │   └── project.py
│   │   ├── constants/          # Domain-specific constants
│   │   ├── models/             # Domain entities and value objects
│   │   │   ├── base.py
│   │   │   └── project.py
│   │   ├── repositories/       # Repository interfaces
│   │   │   └── project.py
│   │   └── utils/              # Domain-specific utilities
│   ├── infrastructures/        # Infrastructure Layer - Technical implementations
│   │   ├── errors/             # Infrastructure-specific errors
│   │   ├── constants/          # Infrastructure constants
│   │   ├── utils/              # Infrastructure utilities
│   │   └── sqlite_db/          # SQLite implementation
│   │       ├── database.py     # Database connection and session management
│   │       ├── project.py      # Concrete repository implementation
│   │       └── models/         # ORM models
│   │           └── project.py
│   ├── routers/                # Presentation Layer - API endpoints
│   │   ├── __init__.py
│   │   ├── errors/             # HTTP error handling
│   │   ├── constants/          # API constants
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── services.py     # Dependency injection
│   │       ├── endpoints/      # API routes
│   │       │   └── project.py
│   │       └── schemas/        # Request/response schemas
│   │           ├── base.py
│   │           ├── errors.py
│   │           └── project.py
│   ├── settings/               # Application settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── config.py
│   │   └── dev.py
│   ├── shared/                 # Cross-cutting concerns
│   │   ├── constants/          # Shared constants
│   │   └── utils/              # Shared utilities
│   └── use_cases/              # Application Layer - Use cases orchestration
│       ├── project.py          # Use case services
│       ├── constants/          # Use case constants
│       ├── dto/                # Data Transfer Objects
│       │   ├── base.py
│       │   └── project.py
│       ├── errors/             # Application-specific errors
│       │   ├── base.py
│       │   └── project.py
│       ├── mappers/            # Data mapping utilities
│       │   └── project.py
│       └── utils/              # Use case utilities
├── pyproject.toml              # Project dependencies and configuration
├── README.md                   # Project documentation
└── project_management.db       # SQLite database
```

## Architecture Layers

### 1. Domain Layer (`app/entities/`)

The core of the application containing business logic and rules, independent of frameworks:

- **Models**: Project entities and value objects
- **Repository Interfaces**: Abstract classes defining data access methods
- **Domain Errors**: Business-specific exceptions
- **Constants**: Business rule constants
- **Utils**: Domain-specific utilities for implementing business rules

### 2. Application Layer (`app/use_cases/`)

Coordinates the application workflow:

- **Use Case Services**: Orchestrate business operations
- **DTOs**: Data Transfer Objects for passing data between layers
- **Mappers**: Transform data between domain models and DTOs
- **Errors**: Application-specific errors
- **Constants**: Application-specific constants
- **Utils**: Helper functions for use cases

### 3. Infrastructure Layer (`app/infrastructures/`)

Provides technical implementations:

- **Repository Implementations**: Concrete implementations of repository interfaces
- **Database Models**: SQLite ORM models
- **Database Utilities**: Connection and session management
- **Errors**: Infrastructure-specific errors
- **Constants**: External system settings
- **Utils**: Helpers for external systems

### 4. Presentation Layer (`app/routers/`)

Handles HTTP requests and responses:

- **Endpoints**: FastAPI route definitions
- **Schemas**: Pydantic models for request/response validation
- **Services**: Dependency injection providers
- **Errors**: HTTP error handlers
- **Constants**: API-specific constants

### 5. Shared (`app/shared/`)

Cross-cutting concerns used across multiple layers:

- **Constants**: Common constants used across the application
- **Utils**: Technical helpers not tied to domain

## Request Flow

1. **Client Request**: Client sends HTTP request to an endpoint
2. **API Endpoint**: Validates request data and calls appropriate use case service
3. **Use Case Service**: Orchestrates business logic using domain models and repository interfaces
4. **Repository Interface**: Defines data operations without implementation details
5. **Repository Implementation**: Executes actual database operations
6. **Response**: Data flows back through the layers to the client

## Error, Constants, and Utils Organization

### Errors

Errors are defined in each layer's `errors/` directory:

1. **Domain Errors** (`app/entities/errors/`): Business rule violations
   - Example: `ProjectNotFoundError`, `InvalidProjectStateError`

2. **Use Case Errors** (`app/use_cases/errors/`): Application-specific errors
   - Example: `ProjectManagementUseCaseError`

3. **Infrastructure Errors** (`app/infrastructures/errors/`): External system errors
   - Example: `DatabaseConnectionError`, `DatabaseQueryError`

4. **Presentation Errors** (`app/routers/errors/`): HTTP error handlers
   - Maps domain, use case, and infrastructure errors to HTTP responses

### Constants

Constants are organized by layer:

1. **Domain Constants** (`app/entities/constants/`): Business rules
   - Example: `PROJECT_NAME_MIN_LENGTH`, `MAX_PROJECTS_PER_USER`

2. **Use Case Constants** (`app/use_cases/constants/`): Application-specific constants
   - Example: `DEFAULT_PROJECT_PAGE_SIZE`, `PROJECT_CACHE_EXPIRY_SECONDS`

3. **Infrastructure Constants** (`app/infrastructures/constants/`): External system settings
   - Example: `DB_POOL_SIZE`, `QUERY_TIMEOUT`

4. **Presentation Constants** (`app/routers/constants/`): API-specific constants
   - Example: `API_DEFAULT_PAGE_SIZE`, `RATE_LIMIT_MAX_REQUESTS`

5. **Shared Constants** (`app/shared/constants/`): Cross-cutting constants
   - Example: `DATE_FORMAT`, `EMAIL_REGEX`

### Utils (Helpers)

Utilities are organized by layer:

1. **Domain Utils** (`app/entities/utils/`): Business rule helpers
   - Example: `validate_project_name()`, `is_valid_state_transition()`

2. **Use Case Utils** (`app/use_cases/utils/`): Application helpers
   - Example: `map_project_to_dto()`, `build_pagination_response()`

3. **Infrastructure Utils** (`app/infrastructures/utils/`): External system helpers
   - Example: `with_db_transaction()`, `with_query_timeout()`

4. **Shared Utils** (`app/shared/utils/`): Cross-cutting helpers
   - Example: `format_datetime()`, `generate_uuid()`

## Error Handling

### Error Hierarchy

#### Domain Errors (entities/errors/)

These are errors that represent violations of domain rules and are independent of how the application is delivered:

- `BaseEntityError`: Base class for all domain errors
- `ProjectNotFoundError`: When a project doesn't exist
- `ProjectNameExistsError`: When a project with that name already exists
- `InvalidProjectStateError`: When a state transition is invalid

#### Use Case Errors (use_cases/errors/)

These are errors specific to application use cases that aren't directly tied to domain rules:

- `ProjectManagementUseCaseError`: Base class for use case errors
- `ProjectValidationError`: When use case input validation fails
- `ProjectOperationNotAllowedError`: When an operation is not allowed
- `ProjectLimitExceededError`: When a user has reached their project limit

The use case layer re-exports domain errors through `__init__.py` so use cases can import all errors from one place.

#### Infrastructure Errors (infrastructures/errors/)

These are errors related to external systems:

- `InfrastructureError`: Base class for infrastructure errors
- `DatabaseConnectionError`: When database connection fails
- `DatabaseQueryError`: When a database query fails
- `EntityNotFoundInDBError`: When an entity is not found in the database

### Best Practices

1. **Error Handling**:
   - Define errors closest to where they are raised
   - Use exception handlers to map domain errors to HTTP responses
   - Always include helpful error messages and contextual data

2. **Constants**:
   - Business rules go in domain constants
   - Configuration settings go in settings module
   - Presentation-specific constants go in routers/constants

3. **Utilities**:
   - Domain utils contain pure business logic functions
   - Shared utils contain technical helpers not tied to domain
   - Infrastructure utils contain helpers for external systems

### How Errors Flow

1. **Domain Errors** are raised in domain entities and value objects
2. **Use Case Errors** are raised in use cases or wrap domain errors
3. **Infrastructure Errors** are raised in repositories/adapters and mapped to domain errors

### Example Usage

```python
# Using domain constants and utils
from app.entities.constants.project import PROJECT_NAME_MIN_LENGTH
from app.entities.utils.project import validate_project_name

# Using shared utilities
from app.shared.utils.date_utils import format_datetime
from app.shared.constants.common import DATE_FORMAT

# Error handling in presentation layer
from app.routers.errors.handlers import setup_error_handlers

# In a use case
from app.use_cases.errors import ProjectNotFoundError, ProjectLimitExceededError

async def create_project(self, user_id, name, description):
    # Check if user has reached limit
    project_count = await self.repository.get_project_count(user_id)
    if project_count >= MAX_PROJECTS_PER_USER:
        raise ProjectLimitExceededError(user_id, MAX_PROJECTS_PER_USER)
    
    # Create project...
```

The API layer will catch and translate these errors to appropriate HTTP responses.
