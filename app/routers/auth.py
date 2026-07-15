from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import schemas
from app.oauth2 import create_access_token
from .. import database
from .. import models, utils

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")
    
    access_token = create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }