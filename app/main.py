from fastapi import FastAPI
from .config import settings
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Users",
        "description": "Create account and read user details. Most read operations require authentication.",
    },
    {
        "name": "Posts",
        "description": "Create, list, search, update, and delete posts. Owner-only checks apply on protected operations.",
    },
    {
        "name": "Vote",
        "description": "Like/unlike posts. Send `dir=1` to like and `dir=0` to remove a like.",
    },
        {
        "name": "Authentication",
        "description": "Login endpoint. Use email as `username` and password to generate a bearer token. Swagger uses OAuth2 Password flow for authorization.",
    },
]

app=FastAPI(
    title="FastAPI Social API",
    version="1.0.0",
    description="""
A social API with JWT authentication.

Quick start in Swagger:
1. Create account: `POST /users/`
2. Click **Authorize** (top-right in Swagger)
3. Enter credentials in OAuth2 form:
   - `username` = your email
   - `password` = your password
4. Click **Authorize** in the popup
5. Use protected endpoints for posts, users, and votes

Manual token generation (optional):
- Use `POST /login` with form fields (`username`, `password`)
- Response returns `access_token` and `token_type`

Core operations:
- Users: signup, list users, view your own profile
- Authentication: login and get JWT bearer token
- Posts: create, list, filter latest, view single post, update, delete
- Vote: like/unlike posts
""",
    openapi_tags=tags_metadata,
    debug=settings.debug,
)

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {'message':'Hello There, Welcome Akshay!'}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
