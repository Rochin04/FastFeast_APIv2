from app.db.session import create_db_and_tables, engine
from app.routers.comidas_router import router as comida_router
from app.routers.categorias_router import router as category_routes
from app.routers.usuario_router import router as usuario_router
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Lifespan ended.")

app = FastAPI(lifespan=lifespan)
app.include_router(comida_router, prefix="/api/v1", tags=["Comidas"])
app.include_router(category_routes, prefix="/api/v1", tags=["Categories"])
app.include_router(usuario_router, prefix="/api/v1", tags=["Usuarios"])

@app.get("/")
async def root():
    return {"message": "Hello World!"}
