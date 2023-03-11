from fastapi import FastAPI
from .database import engine
from . import models
from .routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# we can specify the urls that we can send request to our API from them. if we set origins to ["*"], it means we can send
# request from any web browser url. 
# we have to remember that using postman, we send request from our own computer to the API. But most of the times we 
# send requests from web browsers/mobile devices/etc. so in lines beow we have specified which domain our API is allowed
# to get request from. we can also secify that which soecifuc http request we can accept from user in allow_methods below.
# web browser sends request to our API using javascript fetch API.
# without CORS we can only send request frpm web browser to our API when both of them(Web browser and our API) are on the 
# same domain. but using CORS we can change that and we can send a request to our API on every domain we have allowe them

# list of domains that can talk to our API. so we are going to allow people from youtube and google to talk to us as an API.
# in simple words, we specify the different urls that can talk to our API
# specially when our API is configured for a specific web app, we should specify the exact urls that can talk to pur database
# and send/recieve requests.
origins = [
    "https://www.youtube.com",
    "https://www.google.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#this below command is going to create all of our models (tables)
# at this point, because we use alembic, we no longer need line below, because if we keep this line, our 
# first alembic migration is not going to do anything for us. because our tables are going to be created by below command already.
# line below was for creating the tables when we started 
# to create our models/tables. but now we use alembic and it's responsible for creating tables/columns etc.
# but anyway if we keep it it's not going to create any issue.

# models.Base.metadata.create_all(bind=engine)

#if you remember before we had all of our path operations here, but now we cleaned it up and we moved all codes related 
# to path operations to a separate folder called "routers" in the current directory. basically what we are doing here is that
#  everytime the frontend sends an HTTP request to our API endpoints, our programs runs from up to the bottom of this current file 
# and when it sees these 'app' objects in below lines of codes, it goes ahead and looks inside of posts and users files to find 
# a match to our http request

app.include_router(posts.router)
app.include_router(users.router)        
app.include_router(auth.router)
app.include_router(vote.router)

