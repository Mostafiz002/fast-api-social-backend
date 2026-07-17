from fastapi import Depends, HTTPException
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas
from app.database import get_db
from .config import settings
from sqlalchemy.orm import Session

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.ACCESS_TOKEN_ALGORITHM)
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
    
        token_data = schemas.TokenData(id=id)
        return token_data
    except jwt.InvalidTokenError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail=f"Could not validate user", headers={"WWW-Authenticate": "Bearer"})

    token =  verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

