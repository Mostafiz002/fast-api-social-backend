from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import get_db

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(db: Session = Depends(get_db())):
    