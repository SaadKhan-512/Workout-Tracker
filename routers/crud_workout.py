from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from Database import database, models
from Authorization import token
import schemas

router = APIRouter(prefix="/workout", tags=["CRUD-Workout"])

@router.post("")
def create_workout(workout: schemas.Workout_Schema, 
                   db: Session = Depends(database.get_db), 
                   user: models.User = Depends(token.get_current_user)):
    
    ###                                                 Code                                                      ###
    workout_model = models.User_Defined_Workouts(user_id=user.uuid, **workout.dict())

    db.add(workout_model)
    db.commit()
    db.refresh(workout_model)

    return {
        "message": "Workout added successfully.",
        "message": "Go to /add-exercise to add exercise to new workout.",
        "workout_id": workout_model.id
    }

@router.get("")
def get_workout(db: Session = Depends(database.get_db), user: models.User = Depends(token.get_current_user)):
    # Get all workouts
    workouts = db.query(models.User_Defined_Workouts).filter(models.User_Defined_Workouts.user_id == user.uuid).all()

    all_workouts = {
        "username": user.username
    }

    # Traverse on every single workout
    for workout in workouts:
        # Get all exercises in workout
        exercises = db.query(models.Workout_Exercises).filter(
            models.Workout_Exercises.workout_id == workout.id
        ).all()

        all_workouts[f"Workout_id: {workout.id}"] = {
            "name": workout.name
        }

        for i, exercise in enumerate(exercises, start=1):
            # Get exercise name
            exercise_name = db.query(models.Predefined_Exercises).filter(models.Predefined_Exercises.id == exercise.id).first()
            all_workouts[f"Workout_id: {workout.id}"][f"Exercise {i}"] = {
                "exercise id": exercise.id,
                "exercise name": exercise_name.name,
                "reps": exercise.reps,
                "sets": exercise.sets,
                "weight": exercise.weight
            }
        
    # return all workouts + exercises in workout
    return all_workouts

@router.put("")
def update_workout(id: int, updated_workout: schemas.Workout_Schema, 
                   db: Session = Depends(database.get_db), 
                   user: models.User = Depends(token.get_current_user)):
    # Code
    actual_workout = db.query(models.User_Defined_Workouts).filter(models.User_Defined_Workouts.id == id).first()

    # Check if workout exists?
    if actual_workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found.")

    # Check if user owns this workout?
    if actual_workout.user_id != user.uuid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot able to update someone else workout plan.")

    actual_workout.name = updated_workout.name
    actual_workout.description = updated_workout.description
    actual_workout.scheduled_at = updated_workout.scheduled_at
    actual_workout.status = updated_workout.status

    db.commit()

    new_updated_workout = db.query(models.User_Defined_Workouts).filter(models.User_Defined_Workouts.id == id).first()

    return new_updated_workout

@router.delete("")
def delete_workout(id: int, 
                   db: Session = Depends(database.get_db), 
                   user: models.User = Depends(token.get_current_user)):

    workout_to_be_delete = db.query(models.User_Defined_Workouts).filter(models.User_Defined_Workouts.id == id).first()

    # Check if workout exists?
    if workout_to_be_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found.")
    
    # Check if user owns this workout?
    if workout_to_be_delete.user_id != user.uuid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot able to delete someone else workout plan.")

    db.delete(workout_to_be_delete)
    db.commit()

    return {
        "message": "Workout plan deleted successfully."
    }