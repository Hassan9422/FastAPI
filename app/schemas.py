from datetime import datetime
import email
from msilib.schema import Class
from typing import Optional
from urllib import response
from jinja2 import pass_environment
from pydantic import BaseModel, EmailStr

from app.models import Post

class PostBase(BaseModel):
    title: str
    content: str
    # rating: Optional[int]=None
    published: bool=True

# there is an important thing here. we can add 'owner_id: int' in below class which is PostCreate. but what does that mean?
# it means that whenever we create a post, we have to pass into the id of the user as well. this is 100% possible and we can do that.
# but we are not going to require the user to pass his id into the body when he creats a post. instead, we wanna grab the id from 
# the logic that we have defined inside of our 'login' route in auth.py.  in fact, what we are going to do is that
# we are going to grab the user id from the token when the user logs in. so in this way we have the id and we can grab it 
# and put it in the response that is turned back to us when we get all posts. and for that we have to add 'owner_id' field
# in the ResponsePost schema .


class UserCreate(BaseModel):
    email:EmailStr
    password:str


class Response_User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
class PostCreate(PostBase):
    pass


class ResponsePost(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # The reason tha twe added line below is that we wanna see the inforamation about the user who has created the post!
    # this information as we know is a pydantic model that we have defined before in Response_User class in this file
    # (Response_User class is a pydantic model that returns all the inforamation to us about the user)
    owner: Response_User
    class Config:
        orm_mode = True


# one important thing is that when we join two tables using sqlalchemy, the pydantic models of the response post, 
# is not going to remain the same as before! and it's gonna be changed because of the joining operation oftwo tables.
# so this causes us to define a new schema for our response post, after we joing two tables
class Post_Out(BaseModel):
    Post: ResponsePost
    votes: int
    class Config:
        orm_mode = True



class Token(BaseModel):
    jwt_token: str
    token_type: str

class tokenData(BaseModel):
    id: Optional[str]= None

class Vote(BaseModel):
    post_id: int
    dir: bool