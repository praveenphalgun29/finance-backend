# Finance Dashboard API

A backend API for a finance dashboard system with role-based access control, built using FastAPI and SQLite.

## Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** SQLite via SQLAlchemy
- **Auth:** JWT tokens using python-jose
- **Password Hashing:** bcrypt via passlib
- **Docs:** Auto-generated Swagger UI at `/docs`

## Setup Instructions

1. Clone the repository
2. Create and activate virtual environment
```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
```
3. Install dependencies
```
   pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-multipart
   pip install bcrypt==4.0.1
```
4. Run the server
```
   uvicorn app.main:app --reload
```
5. Open docs at `http://127.0.0.1:8000/docs`

## Roles

| Role | Permissions |
|------|------------|
| admin | Full access - manage users, create/edit/delete records |
| analyst | View records + access all dashboard summaries |
| viewer | View records only |

## API Endpoints

### Auth & Users
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/` - Get all users (admin only)
- `GET /auth/{user_id}` - Get single user
- `PATCH /auth/{user_id}` - Update user (admin only)
- `DELETE /auth/{user_id}` - Delete user (admin only)

### Financial Records
- `POST /records/` - Create record (admin only)
- `GET /records/` - Get all records with optional filters (all roles)
- `GET /records/{id}` - Get single record (all roles)
- `PATCH /records/{id}` - Update record (admin only)
- `DELETE /records/{id}` - Soft delete record (admin only)

### Dashboard (analyst and admin only)
- `GET /dashboard/summary` - Total income, expenses, net balance
- `GET /dashboard/by-category` - Category wise totals
- `GET /dashboard/trends` - Monthly trends
- `GET /dashboard/recent` - Recent transactions

## Features Implemented

- User and role management (admin/analyst/viewer)
- Financial records CRUD
- Record filtering by date, category, type
- Dashboard summary APIs
- Role based access control via middleware
- Input validation and error handling
- SQLite data persistence
- JWT authentication
- Soft delete for records
- Auto-generated Swagger API documentation

## Assumptions Made

- First registered user can be assigned any role directly (for testing purposes)
- Soft delete is used for records - deleted records are hidden but not removed from DB
- Amounts must be greater than 0
- JWT tokens expire after 24 hours

## Tradeoffs

- SQLite used instead of PostgreSQL for simplicity - easy to swap via the DATABASE_URL
- No pagination implemented to keep the codebase minimal and clean
- Role assignment happens at registration - in production this would be admin-only
