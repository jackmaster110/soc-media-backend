from models import PostModel, UserModel
import motor.motor_asyncio
from dotenv import dotenv_values

config = dotenv_values(".env")
DATABASE_URI = config.get("DATABASE_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = client.SocMedia
usersCollection = database.users
postsCollection = database.posts

async def fetch_all_users():
    users = []
    cursor = await usersCollection.find()
    async for document in cursor:
        users.append(UserModel(**document))
    return users

async def fetch_all_posts():
    posts = []
    cursor = postsCollection.find()
    async for document in cursor:
        posts.append(PostModel(**document))
    return posts

async def fetch_all_posts_from_user(user: str):
    posts = []
    cursor = postsCollection.find()
    async for document in cursor:
        if document.get("user") == user: posts.append(PostModel(**document))
    return posts

async def fetch_one_post(nanoid: str):
    document = await postsCollection.find_one({"nanoid": nanoid}, {"_id": 0})
    return document

async def fetch_one_user(nanoid: str):
    document = await usersCollection.find_one({"nanoid": nanoid}, {"_id": 0})
    return document

async def create_user(user: UserModel):
    document = user.dict()
    usersCollection.insert_one(document)
    result = await fetch_one_user(user.nanoid)
    return result

async def create_post(post: PostModel):
    document = post.dict()
    postsCollection.insert_one(document)
    result = await fetch_one_post(post.nanoid)
    return result 