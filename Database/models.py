import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, Text, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from Database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)

    created_at = Column(Date, server_default=func.current_date())

class Predefined_Exercises(Base):
    __tablename__ = "predefined_exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)

class User_Defined_Workouts(Base):
    __tablename__ = "user_defined_workouts"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="CASCADE"))

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    scheduled_at = Column(Date, nullable=True)
    status = Column(String, nullable=False)

    created_at = Column(Date, server_default=func.current_date())
    completed_at = Column(Date, nullable=True)

class Workout_comments(Base):
    __tablename__ = "workout_comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)

    workout_id = Column(Integer, ForeignKey("user_defined_workouts.id", ondelete="CASCADE"), nullable=False)
    comment = Column(Text, nullable=False)

    comment_at = Column(Date, server_default=func.current_date())

class Workout_Exercises(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True)

    workout_id = Column(Integer, ForeignKey("user_defined_workouts.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("predefined_exercises.id", ondelete="CASCADE"), nullable=False)

    reps = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)

    added_at = Column(Date, server_default=func.current_date())

class Workout_Sessions(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True)

    workout_id = Column(Integer, ForeignKey("user_defined_workouts.id", ondelete="CASCADE"))

    scheduled_at = Column(Date, nullable=True)
    started_at = Column(Date, nullable=True)
    completed_at = Column(Date, nullable=True)

    status = Column(String, nullable=False, default="pending")
    notes = Column(String, nullable=True)


class Session_Exercises(Base):
    __tablename__ = "session_exercises"

    id = Column(Integer, primary_key=True, nullable=False)

    session_id = Column(Integer,ForeignKey("workout_sessions.id", ondelete="CASCADE"),nullable=False)
    workout_exercise_id = Column(Integer,ForeignKey("workout_exercises.id", ondelete="RESTRICT"),nullable=False)

    sets_completed = Column(Integer, nullable=False)
    reps_completed = Column(Integer, nullable=False)
    weight_used = Column(Numeric(8, 2), nullable=False)