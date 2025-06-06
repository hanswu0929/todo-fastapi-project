from fastapi import FastAPI
from app.routes import todos
import logging

app = FastAPI()

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

app.include_router(todos.router, prefix="/api")