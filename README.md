# Project Management Service

A Clean Architecture based project management service built with FastAPI and SQLite.

## Features

- Project CRUD operations
- Project state management (PLANNED, IN_PROGRESS, COMPLETED, CANCELLED)
- Pagination for listing projects
- SQLite database for persistence

## Architecture

This project follows Clean Architecture principles, with the following layers:

1. **Entities**: Core business objects and rules
2. **Use Cases**: Application-specific business rules
3. **Interface Adapters**: Adapters between use cases and external frameworks
4. **Frameworks & Drivers**: External frameworks and tools

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -e .
   ```

3. Set up environment variables by copying `.env.example` to `.env`

### Running the Application

```bash
cd server
uvicorn app.main:app --reload
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)
