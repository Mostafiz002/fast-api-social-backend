from fastapi import APIRouter, Depends, Response, status, HTTPException
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=201, response_model=schemas.UserRes)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pass = utils.hash_password(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return new_user

@router.get("/{id}", response_model=schemas.UserRes)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(404, detail="User not found")

    return user
