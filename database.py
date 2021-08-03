from models import PostModel, UserModel
import motor.motor_asyncio
from dotenv import dotenv_values

config = dotenv_values(".env")
DATABASE_URI = config.get("DATABASE_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = client.SocMedia
usersCollection = database.users
postsCollection = database.posts

async def fetch_one_user(nanoid: str):
    document = await usersCollection.find_one({"nanoid": nanoid}, {"_id": 0})
    return document

async def create_user(user: UserModel):
    document = user.dict()
    usersCollection.insert_one(document)
    result = await fetch_one_user(user.nanoid)
    return result