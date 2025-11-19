from sqlmodel import Session, select
from app.models.comida_model import Comida
from app.schemas.comida_shcema import ComidaCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

class ComidaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_comidas(self) -> list[Comida]:
        return self.session.exec(select(Comida)).all()

    def get_comida_by_id(self, id: uuid.UUID) -> Comida | None:
        return self.session.get(Comida, id)

    def create_comida(self, comida: ComidaCreate) -> Comida:
        db_comida = Comida.model_validate(comida)
        self.session.add(db_comida)
        try:
            self.session.commit()
            self.session.refresh(db_comida)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se pudo crear la comida. El vendedor con id '{comida.merchant_id}' no existe."
            )
        return db_comida


    def update_comida(self, id: uuid.UUID, comida_data: ComidaCreate) -> Comida | None:
        db_comida = self.get_comida_by_id(id)
        if db_comida:
            db_comida.name = comida_data.name
            db_comida.description = comida_data.description
            db_comida.price = comida_data.price
            db_comida.category = comida_data.category
            db_comida.image_url = comida_data.image_url
            self.session.add(db_comida)
            self.session.commit()
            self.session.refresh(db_comida)
        return db_comida

    def delete_comida(self, id: uuid.UUID) -> bool:
        db_comida = self.get_comida_by_id(id)
        if db_comida:
            self.session.delete(db_comida)
            self.session.commit()
            return True
        return False
