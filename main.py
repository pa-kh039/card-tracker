from fastapi import FastAPI, Depends
from fastapi.params import Body
from routers import card,user

app=FastAPI()  #api name

app.include_router(card.router)
app.include_router(user.router) #for future implementation of users

