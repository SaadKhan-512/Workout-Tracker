from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from typing import Optional
from datetime import date

# User signup
class User_Create(BaseModel):
    username: str
    email: EmailStr
    password: str

# Define a Workout
class Workout_Schema(BaseModel):
    name: str
    description: str
    scheduled_at: date
    status: str

# Workout_exercise schema
class Workout_Exercise_Schema(BaseModel):
    workout_id: int
    exercise_id: int
    reps: int
    sets: int
    weight: int


# Workout_Session Schema
class Workout_Sessions_Schema(BaseModel):
    workout_id: int
    notes: Optional[str] = None

# Workout_Exercise_Session Schema
class Workout_Exercise_Session_Schema (BaseModel):
    session_id: int
    workout_exercise_id: int
    sets_completed: int
    reps_completed: int
    weight_used: int

# Schema for token data
class Token_Data(BaseModel):
    id: Optional[UUID] = None