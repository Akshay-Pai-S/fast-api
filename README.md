# FastAPI Social API

Production-style backend API built with FastAPI for user management, authentication, post management, and voting.

## Recruiter Keywords
`FastAPI` `Python` `REST API` `JWT Authentication` `OAuth2 Password Flow` `PostgreSQL` `SQLAlchemy 2.0` `Pydantic v2` `Alembic Migrations` `API Security` `CRUD Operations` `OpenAPI/Swagger` `Backend Development`

## Project Overview
This project is a social-style backend service where users can:
- Register and login securely
- Create, update, delete, and fetch posts
- Like/unlike posts
- Retrieve posts with aggregated vote counts

The API includes protected routes using Bearer token auth and interactive API testing through Swagger UI.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy ORM (2.0 style)
- PostgreSQL (`psycopg`)
- Alembic (database migrations)
- Pydantic v2 (request/response validation)
- JWT (`pyjwt`) for token-based auth
- `pwdlib` for password hashing

## Core Features
- Secure user signup with hashed passwords
- JWT-based login (`/login`)
- OAuth2 Bearer protection for private routes
- Post CRUD with owner-based authorization
- Vote system with conflict handling
- Post listing with vote count aggregation
- Search + pagination (`limit`, `skip`, `search`) for latest posts
- Environment-driven configuration via `.env`

## API Modules
- `app/routers/auth.py` - login and token issuance
- `app/routers/user.py` - user creation and user retrieval
- `app/routers/post.py` - post CRUD, my posts, latest posts, vote counts
- `app/routers/vote.py` - like/unlike posts
- `app/oauth2.py` - JWT creation and token verification
- `app/models.py` - SQLAlchemy models (`User`, `Post`, `Vote`)
- `app/schemas.py` - Pydantic schemas and validations

## Authentication Flow
1. Register via `POST /users/`
2. Login via `POST /login` with form-data:
   - `username` = user email
   - `password` = plaintext password
3. Receive:
   - `access_token`
   - `token_type` (`bearer`)
4. Call protected endpoints using:
   - `Authorization: Bearer <access_token>`

## Key Endpoints
- `POST /users/` - create user
- `GET /users/` - list users (protected)
- `GET /users/{id}` - get own profile (protected)
- `POST /login` - authenticate and get JWT
- `GET /posts/` - list posts with vote counts (protected)
- `POST /posts/` - create post (protected)
- `GET /posts/myposts/` - current user posts (protected)
- `GET /posts/myposts/{id}` - own post by id (protected)
- `GET /posts/latest` - latest posts with filters (protected)
- `GET /posts/{id}` - get post by id (protected)
- `PUT /posts/{id}` - update own post (protected)
- `DELETE /posts/{id}` - delete own post (protected)
- `POST /vote/` - like/unlike post (protected)

## Validation Highlights
- Email validation with `EmailStr`
- Phone number regex validation (`+` optional, 10-15 digits)
- Title/content length constraints
- Vote direction constrained to `0` or `1`

## Database Schema
- `users`
  - `id`, `email (unique)`, `name`, `password`, `phone_number`, `created_at`
- `posts`
  - `id`, `title`, `content`, `published`, `created_at`, `owner_id -> users.id`
- `votes`
  - composite primary key: `user_id + post_id`
  - foreign keys to users/posts with cascade delete

## Local Setup
## 1) Clone and enter project
```bash
git clone <your-repo-url>
cd fast_api
```

## 2) Create and activate virtual environment
```bash
python -m venv venv_fastapi
# Windows
venv_fastapi\Scripts\activate
```

## 3) Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg pydantic pydantic-settings pyjwt pwdlib alembic email-validator
```

## 4) Configure environment
Create `.env` in project root:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_db_password_here
DATABASE_NAME=your_db_name_here
DATABASE_USERNAME=your_db_user_name_here
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=dev
DEBUG=true
SQL_ECHO=true
```

## 5) Run migrations
```bash
alembic upgrade head
```

## 6) Start API server
```bash
uvicorn app.main:app --reload
```

## API Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Engineering Strengths Demonstrated
- Clean router-based API architecture
- Dependency injection (`Depends`) for DB session/auth
- Secure authentication and authorization patterns
- ORM query composition with aggregation and joins
- Input/output schema discipline with Pydantic
- Migration-based DB versioning for production workflows

## Future Enhancements
- Automated tests (unit + integration)
- Role-based authorization (RBAC)
- Refresh token strategy
- Docker + CI/CD pipeline
- API rate limiting and observability

## Author
Akshay Pai S
