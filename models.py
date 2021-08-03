from pydantic import BaseModel

class UserModel(BaseModel):
    nanoid: str
    name: str
    username: str
    password: str
    posts: list

class PostModel(BaseModel):
    nanoid: str
    post: str
    user: UserModel
    replies: dict
    isReply: bool
