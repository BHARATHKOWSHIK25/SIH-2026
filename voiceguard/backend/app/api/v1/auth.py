import datetime
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists.")

    # Simple password hash for prototype
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=f"hashed_{user_in.password}",
        full_name=user_in.full_name,
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or user.hashed_password != f"hashed_{form_data.password}":
        # Allow default demo login
        if form_data.username == "admin" and form_data.password == "admin123":
            token = create_access_token({"sub": "admin", "role": "admin"})
            return {"access_token": token, "token_type": "bearer"}
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
