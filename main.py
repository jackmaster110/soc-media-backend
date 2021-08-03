from fastapi import FastAPI as fast
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import *

origins = ["http://localhost:3000", "http://localhost", "http://localhost:5000"]

app = fast()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def get_root():
    return { "Ping": "Pong" }

@app.get("/api/get-user{nanoid}", response_model=UserModel)
async def get_user(nanoid): 
    userSearched = await fetch_one_user(nanoid)
    if not userSearched: return HTTPException(500, "Internal server error searching user")
    return userSearched

@app.get("/api/get-post{nanoid: str}", response_model=PostModel)
async def get_post(nanoid: str): 
    post = await fetch_one_post(nanoid)
    if not post: return HTTPException(500, "Internal server error")
    return post

@app.get("/api/get-posts{user: str}")
async def get_users_posts(user: str):
    posts = await fetch_all_posts_from_user(user)
    if not posts: return HTTPException(500, "Internal server error occured when fetching posts")
    return posts

@app.get("/api/get-posts")
async def get_all_posts():
    posts = await fetch_all_posts()
    if not posts: return HTTPException(500, "Internal server error when fetching posts")
    return posts

@app.put("/api/add-user{user: UserModel}", response_model=UserModel)
async def add_user(user: UserModel):
    userCreated = await create_user(user)
    if not userCreated: return HTTPException(500, "Internal server error while creating user")
    return userCreated

@app.put("/api/add-post{post: PostModel}", response_model=PostModel)
async def add_post(post: PostModel):
    postCreated = await create_post(post)
    if not postCreated: return HTTPException(500, "Internal server error while creating post")
    return postCreated