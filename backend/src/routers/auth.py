"""API routes for authentication."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..auth import create_access_token, hash_password, verify_password
from ..database import get_db
from ..models import User
from ..schemas import TokenResponse, UserLogin, UserRegister, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, session: Session = Depends(get_db)) -> TokenResponse:
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, session: Session = Depends(get_db)) -> TokenResponse:
    user = session.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(user.id)
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))
