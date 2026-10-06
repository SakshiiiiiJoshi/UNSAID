from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.db.session import get_db
from app.db.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import InvalidCredentials
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create a new user account."""
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise InvalidCredentials()

    db_user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate and return a JWT."""
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise InvalidCredentials()

    token = create_access_token(subject=user.id)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return current_user
