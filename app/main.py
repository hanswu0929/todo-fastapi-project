from fastapi import FastAPI
from app.routes import todos, auth
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

app = FastAPI()

app.include_router(todos.router, prefix="/api")
app.include_router(auth.router, prefix="/api")