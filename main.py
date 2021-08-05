from logging import exception
from typing import NewType
from fastapi import FastAPI as fast, params
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import *

origins = ["http://localhost:3000", "http://localhost", "http://localhost:5000", "https://jackmaster110.github.io"]

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

#pass in a string `nanoid`
@app.get("/api/get-user/{nanoid}", response_model=UserModel)
async def get_user(nanoid: str): 
    userSearched = await fetch_one_user(nanoid)
    if not userSearched: raise HTTPException(500, "Internal server error searching user")
    return userSearched

@app.get("/api/get-users")
async def get_all_users():
    users = await fetch_all_users()
    if not users : raise HTTPException(500, "Internal server error when fetching users")
    return users

# pass in a string `nanoid`
@app.get("/api/get-post/{nanoid}", response_model=PostModel)
async def get_post(nanoid: str): 
    post = await fetch_one_post(nanoid)
    if not post: raise HTTPException(500, "Internal server error")
    return post

# pass in a string `user`
@app.get("/api/get-posts/{user}")
async def get_users_posts(user: str):
    posts = await fetch_all_posts_from_user(user)
    if not posts: raise HTTPException(500, "Internal server error occured when fetching posts")
    return posts

@app.get("/api/get-posts")
async def get_all_posts():
    posts = await fetch_all_posts()
    if not posts: raise HTTPException(500, "Internal server error when fetching posts")
    return posts

@app.get("/api/get-replies/{nanoid}")
async def get_all_replies_on_post(nanoid: str):
    replies = await fetch_all_replies(nanoid)
    if not replies: raise HTTPException(500, "Internal server error when fetching replies")
    return replies

# pass in a UserModel object `user`
@app.post("/api/add-user", response_model=UserModel)
async def add_user(user: UserModel):
    userCreated = await create_user(user)
    if not userCreated: raise HTTPException(500, "Internal server error while creating user")
    return userCreated

# pass in a PostModel object `post`
@app.post("/api/add-post", response_model=PostModel )
async def add_post(post: PostModel):
    postCreated = await create_post(post)
    if not postCreated: raise HTTPException(500, "Internal server error while creating post")
    return postCreated

@app.post("/api/add-reply/{nanoid}")
async def add_reply(reply: PostModel, nanoid: str):
    postUpdated = await create_comment(reply, nanoid)
    if not postUpdated: raise HTTPException(500, "Internal server error while creating reply")
    return postUpdated