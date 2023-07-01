from fastapi import Depends, HTTPException, status, APIRouter

from api.models.user_model import Base, UserModel
from api.core.config import SECRET_KEY, AlGORITHM
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.db.DataBasse import engine, SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt, JWTError

from api.models.admin_model import AdminModel

SECRET_KEY = SECRET_KEY
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token/")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Authenticate Error"}},
)

Base.metadata.create_all(bind=engine)


def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def password_hash(password):
    if password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="password is None")
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    if plain_password is None or hashed_password is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="failed verify password")
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_admin(gmail: str, password: str, db):
    user = db.query(AdminModel).filter(AdminModel.gmail == gmail).first()

    if user is None:
        user = db.query(UserModel).filter(UserModel.gmail == gmail).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not valid")

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not valid")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="password is not valid")
    return user


def create_access_token(
        username: str, user_id: int, express_delta: Optional[timedelta] = None
):
    encode = {"username": username, "id": user_id}
    if express_delta:
        expire = datetime.utcnow() + express_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


def create_refresh_token(
        username: str,
        user_id: int,
        express_delta: Optional[timedelta] = None
):
    encode = {"username": username, "id": user_id}
    if express_delta:
        expire = datetime.utcnow() + express_delta
    else:
        expire = datetime.utcnow() + timedelta(days=10)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)

):

    try:
        user = authenticate_admin(form_data.username, form_data.password, db=db)
        if not user:
            raise token_exception()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    token_expires = timedelta(minutes=20)

    token = create_access_token(user.gmail, user.id, express_delta=token_expires)
    get_refresh_token = create_refresh_token(user.gmail, user.id)

    return {"access_token": token,
            "refresh_token": get_refresh_token}


@router.post("/refresh_token")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_access_token = jwt.encode({"sub": user_id}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": new_access_token}



# Exceptions


def get_user_exceptions():
    credential_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credential_exceptions


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response


def for_user_exception():
    credential_exceptions = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="You are not admin ",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credential_exceptions
