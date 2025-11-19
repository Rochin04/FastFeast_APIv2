from fastapi import APIRouter, Depends, Response, status
from app.schemas.comida_shcema import ComidaCreate, ComidaResponse, ComidaReadResponse, ComidaListReadResponse 
from app.services.comida_service import ComidaService
import uuid

router = APIRouter()

@router.get("/comidas", response_model=ComidaListReadResponse)
async def read_comidas(service: ComidaService = Depends()):
    data = service.get_all_comidas()
    return {"data": data}

@router.get("/comidas/{id}", response_model=ComidaReadResponse)
async def read_comida(id: uuid.UUID, service: ComidaService = Depends()):
    data = service.get_comida_by_id(id)
    return {"data": data}

@router.post("/comidas", status_code=status.HTTP_201_CREATED, response_model=ComidaResponse)
async def create_comida(comida: ComidaCreate, service: ComidaService = Depends()):
    db_comida = service.create_comida(comida)
    return {"data": db_comida}

@router.put("/comidas/{id}", response_model=ComidaResponse)
async def update_comida(id: uuid.UUID, comida: ComidaCreate, service: ComidaService = Depends()):
    data = service.update_comida(id, comida)
    return {"data": data}

@router.delete("/comidas/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comida(id: uuid.UUID, service: ComidaService = Depends()):
    service.delete_comida(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
