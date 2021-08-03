from pydantic import BaseModel

class UserModel(BaseModel):
    nanoid: str
    name: str
    username: str
    password: str

class PostModel(BaseModel):
    nanoid: str
    post: str
    user: str
    replies: dict
    isReply: bool
