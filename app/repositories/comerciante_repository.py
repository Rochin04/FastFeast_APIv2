from sqlmodel import Session, select
from app.models.comerciante_model import Merchant
from app.schemas.comerciante_shcema import MerchantCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

class MerchantRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_comerciantes(self) -> list[Merchant]:
        return self.session.exec(select(Merchant)).all()

    def get_comerciante_by_id(self, id: uuid.UUID) -> Merchant | None:
        merchant = self.session.get(Merchant, id)
        if merchant:
            return merchant
        
        statement = select(Merchant).where(Merchant.owner_id == id)
        results = self.session.exec(statement).all()
        if results:
            return results[0]
            
        return None

    def create_comerciante(self, comerciante: MerchantCreate) -> Merchant:
        db_comerciante = Merchant.model_validate(comerciante)
        self.session.add(db_comerciante)
        try:
            self.session.commit()
            self.session.refresh(db_comerciante)
        except IntegrityError as e:
            self.session.rollback()
            error_msg = str(e.orig)
            if "fk_owner" in error_msg:
                 raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El usuario propietario con id '{comerciante.owner_id}' no existe."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad al crear el comerciante."
            )
        return db_comerciante

    def update_comerciante(self, id: uuid.UUID, comerciante_data: MerchantCreate) -> Merchant | None:
        db_comerciante = self.get_comerciante_by_id(id)
        
        if db_comerciante:
            db_comerciante.name = comerciante_data.name
            db_comerciante.description = comerciante_data.description
            db_comerciante.logo_url = comerciante_data.logo_url
            db_comerciante.location_latitude = comerciante_data.location_latitude
            db_comerciante.location_longitude = comerciante_data.location_longitude
            db_comerciante.address = comerciante_data.address
            db_comerciante.opening_time = comerciante_data.opening_time
            db_comerciante.closing_time = comerciante_data.closing_time
            # db_comerciante.is_validated = comerciante_data.is_validated
            
            try:
                self.session.add(db_comerciante)
                self.session.commit()
                self.session.refresh(db_comerciante)
            except IntegrityError as e:
                self.session.rollback()
                if "fk_owner" in str(e.orig):
                     raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"El usuario propietario con id '{comerciante_data.owner_id}' no existe."
                    )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error de integridad al actualizar el comerciante."
                )
        return db_comerciante

    def delete_comerciante(self, id: uuid.UUID) -> bool:
        # Reuse get_comerciante_by_id to support finding by ID or owner_id
        db_comerciante = self.get_comerciante_by_id(id)
        if db_comerciante:
            self.session.delete(db_comerciante)
            self.session.commit()
            return True
        return False
