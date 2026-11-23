from fastapi import APIRouter, HTTPException, status, Depends, Cookie, Response
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from Authorization import token
from sqlalchemy.orm import Session
from Database import database, models
import schemas, hashing

router = APIRouter(tags=["Authorization"])

@router.post("/signup")
def create_user(user_credentials: schemas.User_Create, db: Session = Depends(database.get_db)):
    user_obj = models.User(**user_credentials.dict())

    user_obj.password = hashing.hash(user_obj.password)

    # Add new user to db
    try:
        db.add(user_obj)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )


    return {
        "message": f"New user with {user_obj.email} email has been added to database."
    }

@router.post("/login")
def login(
    response: Response,
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)):

    user_data = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()
    
    # User exists?
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Wrong credentials.")

    # Yes, user exists
    # Check password
    if not hashing.verify(user_credentials.password, user_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials.")

    access_token = token.create_access_token({"email":user_data.email, "user_id": user_data.id})

    # For guest who just loggedIn
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }