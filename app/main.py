from fastapi import FastAPI
from .config import settings
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(
    title="FastAPI Social API",
    version="1.0.0",
    description="API for users, posts, auth and votes.",
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
    return {'message':'Hello welcome hi sap'}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
