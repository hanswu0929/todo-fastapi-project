from fastapi import FastAPI
from app.routes import todos

app = FastAPI()

app.include_router(todos.router, prefix="/api")