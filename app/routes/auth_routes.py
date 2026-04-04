from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import Client
from ..schemas.schemas import ClientCreate, ClientLogin, Token
from ..auth.auth_handler import get_password_hash, verify_password, signJWT

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, description="Register a new client and return an access token.")
def register_client(user: ClientCreate, db: Session = Depends(get_db)):
    db_user = db.query(Client).filter(Client.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = Client(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password_hash=hashed_password,
        address=user.address,
        country=user.country
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return signJWT(new_user.email)

@router.post("/login", response_model=Token, description="Authenticate a client and return an access token.")
def login_client(user: ClientLogin, db: Session = Depends(get_db)):
    db_user = db.query(Client).filter(Client.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return signJWT(db_user.email)
