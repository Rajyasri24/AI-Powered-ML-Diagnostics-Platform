from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db.models import User
from backend.app.core.security import hash_password, verify_password, create_token
from backend.app.api.deps import get_db

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = User(username=username, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"msg": "user created"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        return {"error": "invalid credentials"}

    return {"token": create_token({"sub": username})}