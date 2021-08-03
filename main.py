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

@app.put("/api/add-user{user: UserModel}", response_model=UserModel)
async def add_user(user: UserModel):
    userCreated = await create_user(user)
    if not userCreated: return HTTPException(500, "Internal server error while creating user")
    return userCreated