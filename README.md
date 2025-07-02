# Inventory API

A modern, fast, and scalable inventory management API built with FastAPI.

## Overview

This project implements a comprehensive inventory management system using FastAPI, a modern Python web framework that offers high performance, automatic API documentation, and type safety. The API provides endpoints for managing products, tracking inventory levels, handling transactions, and generating reports.

## Features

- **FastAPI Framework**: High-performance async web framework with automatic OpenAPI documentation
- **Database Integration**: SQLAlchemy ORM with PostgreSQL support
- **Authentication & Authorization**: JWT-based authentication system
- **CRUD Operations**: Complete Create, Read, Update, Delete operations for inventory items
- **Data Validation**: Pydantic models for request/response validation
- **API Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Testing**: Comprehensive test suite with pytest

## Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Documentation**: OpenAPI/Swagger
- **Testing**: pytest
- **Dependency Management**: Pipenv

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Pipenv (for dependency management)
- PostgreSQL (for database)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory_api
   ```

2. **Install dependencies using Pipenv**
   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**
   ```bash
   pipenv shell
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/inventory_db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

## Project Structure

```
inventory_api/
├── app/
│   ├── api/           # API routes and endpoints
│   ├── auth/          # Authentication and authorization
│   ├── core/          # Core configuration and settings
│   ├── crud/          # Database CRUD operations
│   ├── db/            # Database configuration and session
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic models for validation
│   └── tests/         # Test files
├── Pipfile            # Pipenv dependencies
├── Pipfile.lock       # Locked dependencies
└── README.md          # This file
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8 .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
