from fastapi import APIRouter, Depends, Response, status
from app.schemas.estudiante_schema import EstudianteCreate, EstudianteUpdate, EstudianteResponse, EstudianteReadResponse, EstudianteListReadResponse
from app.services.estudiante_service import EstudianteService
import uuid

router = APIRouter()

@router.get("/estudiantes", response_model=EstudianteListReadResponse)
async def read_estudiantes(service: EstudianteService = Depends()):
    data = service.get_all_estudiantes()
    return {"data": data}

@router.get("/estudiantes/{user_id}", response_model=EstudianteReadResponse)
async def read_estudiante(user_id: uuid.UUID, service: EstudianteService = Depends()):
    data = service.get_estudiante_by_id(user_id)
    return {"data": data}

@router.post("/estudiantes", status_code=status.HTTP_201_CREATED, response_model=EstudianteResponse)
async def create_estudiante(estudiante: EstudianteCreate, service: EstudianteService = Depends()):
    db_estudiante = service.create_estudiante(estudiante)
    return {"data": db_estudiante}
    ##No deberia pedirte el is_verified##

@router.put("/estudiantes/{user_id}", response_model=EstudianteResponse)
async def update_estudiante(user_id: uuid.UUID, estudiante: EstudianteUpdate, service: EstudianteService = Depends()):
    data = service.update_estudiante(user_id, estudiante)
    return {"data": data}
    ##No deberia pedirte el is_verifie ni el user_id##

@router.delete("/estudiantes/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estudiante(user_id: uuid.UUID, service: EstudianteService = Depends()):
    service.delete_estudiante(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
