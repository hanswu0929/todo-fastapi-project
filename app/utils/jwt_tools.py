import jwt
import time

SECRET_KEY = "myjwtsecret"
ALGORITHM = "HS256"

def create_token(username: str, exp_sec: int = 600):
    payload = {"sub": username, "exp": int(time.time()) + exp_sec}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])