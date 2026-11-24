from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from Database import database, models
from Authorization import token
import schemas

router = APIRouter(tags=["CRUD-Workout"])

@router.post("/workout")
def create_workout(workout: schemas.Workout_Schema, db: Session = Depends(database.get_db), user: models.User = Depends(token.get_current_user)):
    workout_model = models.User_Defined_Workouts(user_id=user.uuid, **workout.dict())

    db.add(workout_model)
    db.commit()
    db.refresh(workout_model)

    return {
        "message": "Workout added successfully.",
        "message": "Go to /add-exercise to add exercise to new workout.",
        "workout_id": workout_model.id
    }

@router.post("/add-exercise")
def add_exercise(workout_exercises: schemas.Workout_Exercise_Schema, 
                 db: Session = Depends(database.get_db), 
                 user: models.User = Depends(token.get_current_user)):
    # Code
    is_exists = db.query(models.User_Defined_Workouts).filter(
        models.User_Defined_Workouts.id == workout_exercises.workout_id,
        models.User_Defined_Workouts.user_id == user.uuid
    ).first()

    if is_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This workout id doesn't exists " \
        "OR" \
        " trying to use someone else workout routine.")

    workout_exercises_model = models.Workout_Exercises(**workout_exercises.dict())

    return workout_exercises_model