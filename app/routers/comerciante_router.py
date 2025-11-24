from fastapi import APIRouter, Depends, Response, status
from app.schemas.comerciante_shcema import MerchantCreate, MerchantResponse, MerchantReadResponse, MerchantListReadResponse
from app.services.comerciante_service import ComercianteService
import uuid

router = APIRouter()

@router.get("/comerciantes", response_model=MerchantListReadResponse)
async def read_comerciantes(service: ComercianteService = Depends()):
    data = service.get_all_comerciantes()
    return {"data": data}

@router.get("/comerciantes/{id}", response_model=MerchantReadResponse)
async def read_comerciante(id: uuid.UUID, service: ComercianteService = Depends()):
    data = service.get_comerciante_by_id(id)
    return {"data": data}

@router.post("/comerciantes", status_code=status.HTTP_201_CREATED, response_model=MerchantResponse)
async def create_comerciante(comerciante: MerchantCreate, service: ComercianteService = Depends()):
    db_comerciante = service.create_comerciante(comerciante)
    return {"data": db_comerciante}

@router.put("/comerciantes/{id}", response_model=MerchantResponse)
async def update_comerciante(id: uuid.UUID, comerciante: MerchantCreate, service: ComercianteService = Depends()):
    data = service.update_comerciante(id, comerciante)
    return {"data": data}

@router.delete("/comerciantes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comerciante(id: uuid.UUID, service: ComercianteService = Depends()):
    service.delete_comerciante(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
