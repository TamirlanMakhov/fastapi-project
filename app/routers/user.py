from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from ..database import get_db


router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hash_psw = utils.get_hash(user.password)
    user.password = hash_psw

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{my_id}", response_model=schemas.UserResponse)
def get_user(my_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == my_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {my_id} not found")
    return user
