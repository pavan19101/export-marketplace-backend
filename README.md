# Export Marketplace Backend

A production-ready FastAPI backend for an Export Marketplace platform.

## Tech Stack
- **FastAPI**: Modern, fast, and high-performance Python framework.
- **SQLAlchemy**: Powerful ORM for database orchestration.
- **Pydantic**: Data validation and response modeling.
- **JWT**: Secure authentication for protected routes.
- **SQLite**: Default SQL database (ready for migration to PostgreSQL).
- **Swagger/ReDoc**: Automatically generated API documentation.

## Features
- **Full Marketplace Logic**: Manage Clients, Dealers, Products, and Stocks.
- **Automated Order Processing**: Auto-stock reduction, tracking generation, and delivery agent assignment.
- **Security**: JWT-based authentication with bcrypt password hashing.
- **Automatic Seeding**: Seeds the database with sample data on startup if empty.

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
uvicorn app.main:app --reload
```

### 3. API Documentation
Detailed API documentation and testing interface:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
```
app/
 ├── main.py          # Entry point and initialization
 ├── models/          # SQLAlchemy Database Models
 ├── schemas/         # Pydantic Schemas for Validation
 ├── routes/          # API Route Modules
 ├── database/        # DB Configuration and Session
 ├── auth/            # JWT and Authentication Utilities
 ├── seed.py          # Database Seeding Logic
 ├── utils/           # Shared Utility Functions
```

## Seed Credentials
Once running, you can log in with:
- **Email**: `john@example.com`
- **Password**: `password123`
