from fastapi import FastAPI, Depends, status, exceptions
from typing import Annotated
from database import get_db
import models 
from sqlalchemy.orm import Session
from schemas import UserCreate, UserLogin, UserOut, Token
from utils import hash, verify
from oauth2 import create_access_token, get_current_user

app = FastAPI()

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db : Session = Depends(get_db)):
    user.password = hash(user.password)     
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
def login_user(user_credentials: UserLogin, db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user:
        return exceptions.HTTPException(status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")
    if not verify(user_credentials.password, user.password):
        return exceptions.HTTPException(status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")
    access_token = create_access_token({"user_id" : user.id})
    return Token(access_token=access_token, token_type="bearer")


@app.get("/me", response_model=UserOut)
def get_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user