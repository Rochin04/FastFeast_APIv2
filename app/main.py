from app.db.session import create_db_and_tables, engine
from app.routers.comidas_router import router as comida_router
from app.routers.categorias_router import router as category_routes
from app.routers.usuario_router import router as usuario_router
from app.routers.estudiante_router import router as estudiante_router
from app.routers.comerciante_router import router as comerciante_router
from app.routers.promocion_router import router as promocion_router
from app.routers.auth_router import router as auth_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Lifespan ended.")

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comida_router, prefix="/api/v1", tags=["Comidas"])#aqui se crean las comidas por los comerciantes
app.include_router(category_routes, prefix="/api/v1", tags=["Categories"])#aqui se crean las categorias por los comerciantes
app.include_router(usuario_router, prefix="/api/v1", tags=["Usuarios"])#aqui se crean los usuarios
app.include_router(estudiante_router, prefix="/api/v1", tags=["Estudiantes"])#aqui se crean los estudiantes
app.include_router(comerciante_router, prefix="/api/v1", tags=["Comerciantes"])#aqui se crean los comerciantes
app.include_router(promocion_router, prefix="/api/v1", tags=["Promociones"])#aqui se crean las promociones por los comerciantes
app.include_router(auth_router, prefix="/api/v1", tags=["Auth"])#login endpoint

@app.get("/")
async def root():
    return {"message": "Hello World!"}
