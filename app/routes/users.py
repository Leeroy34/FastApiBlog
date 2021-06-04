from datetime import timedelta

from jose import JWTError, jwt

from app import models
from .. import database, schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from ..services import auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/user",
    tags=['Users']
)
get_db = database.get_db

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/ me/")
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@router.post("/users/")
def create_user(
        user: schemas.UserCreate, db: Session = Depends(get_db)
):
    return auth.create_user(db=db, user=user)
