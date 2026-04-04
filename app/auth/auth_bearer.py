from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth_handler import decodeJWT
from ..database.db import get_db
from sqlalchemy.orm import Session
from ..models.models import Client

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            payload = decodeJWT(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

def get_current_user(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    email = token.get("user_email")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(Client).filter(Client.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
