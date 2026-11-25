from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from Database import database, models
from Authorization import token
import schemas

router = APIRouter(prefix="/exercise", tags=["CRUD-Exercise"])

@router.get("")
def get_exercises(workout_id: int, 
                  db: Session = Depends(database.get_db), 
                  user: models.User = Depends(token.get_current_user)):
    ## Code

    is_exists = db.query(models.User_Defined_Workouts).filter(
        models.User_Defined_Workouts.id == workout_id,
        models.User_Defined_Workouts.user_id == user.uuid
    ).first()
    
    if is_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This workout id doesn't exists " \
        "OR" \
        " trying to use someone else workout plan.")


    all_exercises = {
        "Workout id": workout_id
    }

    exercises = db.query(models.Workout_Exercises).filter(
        models.Workout_Exercises.workout_id == workout_id
    ).all()

    for i, exercise in enumerate(exercises, start=1):
        # Get exercise name
        exercise_name = db.query(models.Predefined_Exercises).filter(models.Predefined_Exercises.id == exercise.id).first()
        all_exercises[f"Exercise {i}"] = {
            "exercise id": exercise.id,
            "exercise name": exercise_name.name,
            "reps": exercise.reps,
            "sets": exercise.sets,
            "weight": exercise.weight
        }

    return all_exercises

@router.post("")
def add_exercise(workout_exercise: schemas.Workout_Exercise_Schema, 
                 db: Session = Depends(database.get_db), 
                 user: models.User = Depends(token.get_current_user)):
    # Code
    # Check if workout exists

    is_exists = db.query(models.User_Defined_Workouts).filter(
        models.User_Defined_Workouts.id == workout_exercise.workout_id,
        models.User_Defined_Workouts.user_id == user.uuid
    ).first()

    if is_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This workout id doesn't exists " \
        "OR" \
        " trying to use someone else workout plan.")

    # Check if exercise exists in predefined_exercises table.
    is_exercise_exists = db.query(models.Predefined_Exercises).filter(
        models.Predefined_Exercises.id == workout_exercise.exercise_id
    ).first()

    if is_exercise_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise not found(Select id between 1 - 10)")

    # Check if exercise exists in workout
    is_exercise_exists_in_workout = db.query(models.Workout_Exercises).filter(
        models.Workout_Exercises.workout_id == workout_exercise.workout_id,
        models.Workout_Exercises.exercise_id == workout_exercise.exercise_id
    ).first()

    if is_exercise_exists_in_workout:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Exercise already exists in workout. Try to add another exercise.")

    # Add exercise
    workout_exercises_model = models.Workout_Exercises(**workout_exercise.dict())

    db.add(workout_exercises_model)
    db.commit()
    db.refresh(workout_exercises_model)

    return {
        "message": "Exercise added successfully."
    }

@router.put("")
def update_exercise(updated_workout_exercise: schemas.Workout_Exercise_Schema, 
                    db: Session = Depends(database.get_db), 
                    user: models.User = Depends(token.get_current_user)):
    ## Code

    is_exists = db.query(models.User_Defined_Workouts).filter(
        models.User_Defined_Workouts.id == updated_workout_exercise.workout_id,
        models.User_Defined_Workouts.user_id == user.uuid
    ).first()
    
    if is_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This workout id doesn't exists " \
        "OR" \
        " trying to use someone else workout plan.")

    exercise = db.query(models.Workout_Exercises).filter(
        models.Workout_Exercises.workout_id == updated_workout_exercise.workout_id,
        models.Workout_Exercises.exercise_id == updated_workout_exercise.exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    exercise.weight = updated_workout_exercise.weight
    exercise.sets = updated_workout_exercise.sets
    exercise.reps = updated_workout_exercise.reps

    db.commit()

    return {
        "message": f"Exercise with id of {updated_workout_exercise.exercise_id} has been updated successfully."
    }

@router.delete("")
def update_exercise(workout_id: int, exercise_id: int, 
                    db: Session = Depends(database.get_db), 
                    user: models.User = Depends(token.get_current_user)):
    ## Code

    is_exists = db.query(models.User_Defined_Workouts).filter(
        models.User_Defined_Workouts.id == workout_id,
        models.User_Defined_Workouts.user_id == user.uuid
    ).first()
    
    if is_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This workout id doesn't exists " \
        "OR" \
        " trying to use someone else workout plan.")

    exercise = db.query(models.Workout_Exercises).filter(
        models.Workout_Exercises.workout_id == workout_id,
        models.Workout_Exercises.exercise_id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    db.delete(exercise)
    db.commit()

    return {
        "message": f"Exercise with id of {exercise_id} hass been deleted."
    }