from sqlmodel import Session, select
from app.models.promocion_model import Promotion
from app.schemas.promocion_shcema import PromotionCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

class PromotionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_promotions(self) -> list[Promotion]:
        return self.session.exec(select(Promotion)).all()

    def get_promotion_by_id(self, id: uuid.UUID) -> Promotion | None:
        promotion = self.session.get(Promotion, id)
        if promotion:
           return promotion
        
        statement = select(Promotion).where(Promotion.merchant_id == id)
        promotion = self.session.exec(statement).first()
        return promotion

    def get_promotions_by_merchant_id(self, merchant_id: uuid.UUID) -> list[Promotion]:
        statement = select(Promotion).where(Promotion.merchant_id == merchant_id)
        return self.session.exec(statement).all()

    def create_promotion(self, promotion: PromotionCreate) -> Promotion:
        db_promotion = Promotion.model_validate(promotion)
        self.session.add(db_promotion)
        try:
            self.session.commit()
            self.session.refresh(db_promotion)
        except IntegrityError as e:
            self.session.rollback()
            error_msg = str(e.orig)
            if "fk_merchant" in error_msg:
                 raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El comerciante con id '{promotion.merchant_id}' no existe."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad al crear la promoción."
            )
        return db_promotion

    def update_promotion(self, id: uuid.UUID, promotion_data: PromotionCreate) -> Promotion | None:
        db_promotion = self.get_promotion_by_id(id)
        
        if db_promotion:
            db_promotion.title = promotion_data.title
            db_promotion.description = promotion_data.description
            db_promotion.discount_type = promotion_data.discount_type
            db_promotion.discount_value = promotion_data.discount_value
            db_promotion.start_date = promotion_data.start_date
            db_promotion.end_date = promotion_data.end_date
            db_promotion.is_active = promotion_data.is_active
            
            try:
                self.session.add(db_promotion)
                self.session.commit()
                self.session.refresh(db_promotion)
            except IntegrityError as e:
                self.session.rollback()
                if "fk_merchant" in str(e.orig):
                     raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"El comerciante con id '{promotion_data.merchant_id}' no existe."
                    )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error de integridad al actualizar la promoción."
                )
        return db_promotion

    def delete_promotion(self, id: uuid.UUID) -> bool:
        db_promotion = self.get_promotion_by_id(id)
        if db_promotion:
            self.session.delete(db_promotion)
            self.session.commit()
            return True
        return False
