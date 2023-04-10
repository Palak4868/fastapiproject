from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from . import config

#models.Base.metadata.create_all(bind=engine)

app=FastAPI()
origins=["*"]
app.add_middleware(CORSMiddleware, allow_origins = origins, allow_credentials =True, allow_methods=["*"], allow_headers=["*"])


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/") #decorator - turns the below code into path 
#synatx @ is symbol, app is our fast api instance then . operation with get method (http method - send a get request) 
# and in bracket  is URL it is rootpath - refers to path we want to go in url 
def root(): # it is a function name root  
    return {"message": "Welcome to my API!"} #returning python dictionary





