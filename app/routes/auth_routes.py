from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..models.models import Client, OTP
from ..schemas.schemas import ClientCreate, ClientLogin, Token, OTPSend, OTPVerify
from ..auth.auth_handler import get_password_hash, verify_password, signJWT, generate_otp
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, description="Register a new client using email and the OTP code sent to that email.")
def register_client(user: ClientCreate, db: Session = Depends(get_db)):
    # 1. Verify OTP
    otp_record = db.query(OTP).filter(OTP.email == user.email, OTP.code == user.otp_code).first()
    if not otp_record or otp_record.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # 2. Check if email already registered
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
    
    # Clean up OTP record
    db.delete(otp_record)
    db.commit()
    
    return signJWT(new_user.email)

@router.post("/send-otp", description="Generate a 6-digit OTP and 'send' it to the provided email. For this demo, it is returned in the response.")
def send_otp(payload: OTPSend, db: Session = Depends(get_db)):
    otp_code = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=10)
    
    # Update or create OTP record
    db_otp = db.query(OTP).filter(OTP.email == payload.email).first()
    if db_otp:
        db_otp.code = otp_code
        db_otp.expires_at = expires_at
    else:
        db_otp = OTP(email=payload.email, code=otp_code, expires_at=expires_at)
        db.add(db_otp)
    
    db.commit()
    
    # In production, send via email. Here we return so you can test easily.
    return {"message": "OTP sent successfully", "code": otp_code}

@router.post("/login", response_model=Token, description="Authenticate a client and return an access token.")
def login_client(user: ClientLogin, db: Session = Depends(get_db)):
    db_user = db.query(Client).filter(Client.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return signJWT(db_user.email)
