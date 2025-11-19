from sqlmodel import Session, select
from datetime import datetime
from app.db.session import create_db_and_tables, engine
from app.models.comida_model import Comida
from app.routers.comidas_router import router as comida_router
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Lifespan ended.")

app = FastAPI(lifespan=lifespan)
app.include_router(comida_router, prefix="/api/v1", tags=["Comidas"])

@app.get("/")
async def root():
    return {"message": "Hello World!"}
