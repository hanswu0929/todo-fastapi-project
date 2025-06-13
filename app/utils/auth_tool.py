from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.utils.jwt_tools import decode_token

# OAuth2PasswordBearer 讓 Swagger UI 支援 Authorize
auth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def verify_token(token: str = Depends(auth2_scheme)):
    try:
        payload = decode_token(token)
        username = payload["sub"] if isinstance(payload, dict) else payload
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 已過期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token 無效")