from fastapi import APIRouter, Depends, Response, status
from app.schemas.promocion_shcema import PromotionCreate, PromotionResponse, PromotionReadResponse, PromotionListReadResponse
from app.services.promocion_service import PromotionService
import uuid

router = APIRouter()

@router.get("/promociones", response_model=PromotionListReadResponse)
async def read_promotions(service: PromotionService = Depends()):
    data = service.get_all_promotions()
    return {"data": data}

@router.get("/promociones/{id}", response_model=PromotionReadResponse)
async def read_promotion(id: uuid.UUID, service: PromotionService = Depends()):
    data = service.get_promotion_by_id(id)
    return {"data": data}

@router.get("/promociones/merchant/{merchant_id}", response_model=PromotionListReadResponse)
async def read_promotions_by_merchant(merchant_id: uuid.UUID, service: PromotionService = Depends()):
    data = service.get_promotions_by_merchant_id(merchant_id)
    return {"data": data}

@router.post("/promociones", status_code=status.HTTP_201_CREATED, response_model=PromotionResponse)
async def create_promotion(promotion: PromotionCreate, service: PromotionService = Depends()):
    db_promotion = service.create_promotion(promotion)
    return {"data": db_promotion}

@router.put("/promociones/{id}", response_model=PromotionResponse)
async def update_promotion(id: uuid.UUID, promotion: PromotionCreate, service: PromotionService = Depends()):
    data = service.update_promotion(id, promotion)
    return {"data": data}

@router.delete("/promociones/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_promotion(id: uuid.UUID, service: PromotionService = Depends()):
    service.delete_promotion(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
