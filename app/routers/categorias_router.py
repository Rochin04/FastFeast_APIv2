from fastapi import APIRouter, Depends, Response, status
from app.schemas.categorias_schema import CategoryCreate, CategoryResponse, CategoryReadResponse, CategoryListReadResponse
from app.services.categorias_service import CategoryService
import uuid

router = APIRouter()

@router.get("/categories", response_model=CategoryListReadResponse)
async def read_categories(service: CategoryService = Depends()):
    data = service.get_all_categories()
    return {"data": data}

@router.get("/categories/{id}", response_model=CategoryReadResponse)
async def read_category(id: uuid.UUID, service: CategoryService = Depends()):
    data = service.get_category_by_id(id)
    return {"data": data}

@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(category: CategoryCreate, service: CategoryService = Depends()):
    db_category = service.create_category(category)
    return {"data": db_category}

@router.put("/categories/{id}", response_model=CategoryResponse)
async def update_category(id: uuid.UUID, category: CategoryCreate, service: CategoryService = Depends()):
    data = service.update_category(id, category)
    return {"data": data}

@router.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: uuid.UUID, service: CategoryService = Depends()):
    service.delete_category(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
