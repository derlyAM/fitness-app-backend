from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.auth import LoginRequest, LoginResponse
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/api", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta")
ALGORITHM = "HS256"
TOKEN_EXPIRY = 60 * 24

_bearer = HTTPBearer()

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Security(_bearer),
) -> int:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return user_id

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=UsuarioResponse)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    nuevo = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password=hash_password(usuario.password)
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    if not usuario or not verify_password(credentials.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer", "usuario": usuario}
