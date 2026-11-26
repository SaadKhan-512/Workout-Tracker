from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from Database import database, models
from Authorization import token
import schemas

router = APIRouter(tags=["Workout Sessions"])

@router.post("/create-workout-session")
def workout_sessions(data: schemas.Workout_Sessions_Schema, 
                    db: Session = Depends(database.get_db), 
                    user: models.User = Depends(token.get_current_user)):
    # Code

    is_exists = db.query(models.User_Defined_Workouts).filter(
        models.User_Defined_Workouts.id == data.workout_id,
        models.User_Defined_Workouts.user_id == user.uuid
    ).first()

    if is_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This workout id doesn't exists " \
        "OR" \
        " trying to use someone else workout plan.")

    is_session_exists = db.query(models.Workout_Sessions).filter(
        models.Workout_Sessions.workout_id == data.workout_id
    ).first()

    if is_session_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Workout Session exists(session_id = {is_session_exists.id}).")

    session = models.Workout_Sessions(**data.dict())

    print(session.id, session.notes)

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "message": "Session created successfully.",
        "session": session
    }

@router.post("/set-exercise")
def workout_sessions(data: schemas.Workout_Exercise_Session_Schema, 
                    db: Session = Depends(database.get_db), 
                    user: models.User = Depends(token.get_current_user)):
    # Code

    # Check if session exists or not?
    is_session_exists = db.query(models.Workout_Sessions).filter(
        models.Workout_Sessions.id == data.session_id
    ).first()

    if is_session_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout session not found.")

    # Validate data
    if data.reps_completed <= 0 or data.sets_completed <= 0 or data.weight_used <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either reps, sets or weight is less then or equal to 0.")

    print(user.username, user.uuid)
    print(is_session_exists.workout_id)

    # Check if workout exists or not?
    is_workout_exists = db.query(models.User_Defined_Workouts).filter(
        models.User_Defined_Workouts.user_id == user.uuid,
        models.User_Defined_Workouts.id == is_session_exists.workout_id
    ).first()

    if is_workout_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This workout id doesn't exists " \
        "OR" \
        " trying to use someone else workout plan.")

    # Check if exercise exists in workout or not?
    is_exercise_exists = db.query(models.Workout_Exercises).filter(
        models.Workout_Exercises.workout_id == is_workout_exists.id,
        models.Workout_Exercises.exercise_id == data.workout_exercise_id
    ).first()

    if is_exercise_exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This exercise does not exists in workout(id = {is_workout_exists.id}).")

    exercise_session = models.Session_Exercises(**data.dict())
    
    db.add(exercise_session)
    db.commit()

    return {"message": "exercise detailed saved successfully."}