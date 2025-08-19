# Clean Architecture Project Template

This is a Python project template implementing Clean Architecture principles for a project management application. It provides a structured approach to building maintainable, testable applications with clear separation of concerns.

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
│   │   ├── models/             # Domain entities and value objects
│   │   │   ├── base.py
│   │   │   └── project.py
│   │   └── repositories/       # Repository interfaces
│   │       └── project.py
│   ├── infrastructures/        # Infrastructure Layer - Technical implementations
│   │   └── sqlite_db/          # SQLite implementation
│   │       ├── database.py     # Database connection and session management
│   │       ├── project.py      # Concrete repository implementation
│   │       └── models/         # ORM models
│   │           └── project.py
│   ├── routers/                # Presentation Layer - API endpoints
│   │   ├── __init__.py
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
│   └── use_cases/              # Application Layer - Use cases orchestration
│       ├── project.py          # Use case services
│       ├── dto/                # Data Transfer Objects
│       │   ├── base.py
│       │   └── project.py
│       ├── errors/             # Application-specific errors
│       │   ├── base.py
│       │   └── project.py
│       └── mappers/            # Data mapping utilities
│           └── project.py
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

### 2. Application Layer (`app/use_cases/`)

Coordinates the application workflow:

- **Use Case Services**: Orchestrate business operations
- **DTOs**: Data Transfer Objects for passing data between layers
- **Mappers**: Transform data between domain models and DTOs

### 3. Infrastructure Layer (`app/infrastructures/`)

Provides technical implementations:

- **Repository Implementations**: Concrete implementations of repository interfaces
- **Database Models**: SQLite ORM models
- **Database Utilities**: Connection and session management

### 4. Presentation Layer (`app/routers/`)

Handles HTTP requests and responses:

- **Endpoints**: FastAPI route definitions
- **Schemas**: Pydantic models for request/response validation
- **Services**: Dependency injection providers

## Request Flow

1. **Client Request**: Client sends HTTP request to an endpoint
2. **API Endpoint**: Validates request data and calls appropriate use case service
3. **Use Case Service**: Orchestrates business logic using domain models and repository interfaces
4. **Repository Interface**: Defines data operations without implementation details
5. **Repository Implementation**: Executes actual database operations
6. **Response**: Data flows back through the layers to the client
