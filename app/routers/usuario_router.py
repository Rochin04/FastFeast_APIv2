from fastapi import APIRouter, Depends, Response, status
from app.schemas.usuarios_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioReadResponse, UsuarioListReadResponse
from app.services.usuarios_service import UsuarioService
import uuid

router = APIRouter()

@router.get("/usuarios", response_model=UsuarioListReadResponse)
async def read_usuarios(service: UsuarioService = Depends()):
    data = service.get_all_usuarios()
    return {"data": data}

@router.get("/usuarios/{id}", response_model=UsuarioReadResponse)
async def read_usuario(id: uuid.UUID, service: UsuarioService = Depends()):
    data = service.get_usuario_by_id(id)
    return {"data": data}

@router.post("/usuarios", status_code=status.HTTP_201_CREATED, response_model=UsuarioResponse)
async def create_usuario(usuario: UsuarioCreate, service: UsuarioService = Depends()):
    db_usuario = service.create_usuario(usuario)
    return {"data": db_usuario}

@router.put("/usuarios/{id}", response_model=UsuarioResponse)
async def update_usuario(id: uuid.UUID, usuario: UsuarioUpdate, service: UsuarioService = Depends()):
    data = service.update_usuario(id, usuario)
    return {"data": data}

@router.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: uuid.UUID, service: UsuarioService = Depends()):
    service.delete_usuario(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)