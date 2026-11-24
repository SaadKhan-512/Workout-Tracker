from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from Database import models
from Database.database import Base, engine
from Authorization import auth
from routers import crud


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(crud.router)