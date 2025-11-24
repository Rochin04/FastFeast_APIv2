from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.promocion_repository import PromotionRepository
from app.repositories.comerciante_repository import MerchantRepository
from app.schemas.promocion_shcema import PromotionCreate
from app.models.promocion_model import Promotion
import uuid

class PromotionService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = PromotionRepository(session)
        self.merchant_repo = MerchantRepository(session)

    def get_all_promotions(self) -> list[Promotion]:
        return self.repo.get_all_promotions()

    def get_promotion_by_id(self, id: uuid.UUID) -> Promotion:
        promotion = self.repo.get_promotion_by_id(id)
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        return promotion

    def get_promotions_by_merchant_id(self, merchant_id: uuid.UUID) -> list[Promotion]:
        # Validar si el comerciante existe
        merchant = self.merchant_repo.get_comerciante_by_id(merchant_id)
        if not merchant:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comerciante con id '{merchant_id}' no existe."
            )
        return self.repo.get_promotions_by_merchant_id(merchant_id)

    def create_promotion(self, promotion: PromotionCreate) -> Promotion:
        # Validar si el comerciante existe
        merchant = self.merchant_repo.get_comerciante_by_id(promotion.merchant_id)
        if not merchant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comerciante con id '{promotion.merchant_id}' no existe."
            )
        
        return self.repo.create_promotion(promotion)

    def update_promotion(self, id: uuid.UUID, promotion_data: PromotionCreate) -> Promotion:
        updated_promotion = self.repo.update_promotion(id, promotion_data)
        if not updated_promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        return updated_promotion

    def delete_promotion(self, id: uuid.UUID):
        success = self.repo.delete_promotion(id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
