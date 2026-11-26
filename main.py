from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from Database import models
from Database.database import Base, engine
from Authorization import auth
from routers import crud_workout, crud_exercise, workout_sessions


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(crud_workout.router)
app.include_router(crud_exercise.router)
app.include_router(workout_sessions.router)