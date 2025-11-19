from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.comidas_repository import ComidaRepository
from app.schemas.comida_shcema import ComidaCreate
from app.models.comida_model import Comida
import uuid

class ComidaService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = ComidaRepository(session)

    def get_all_comidas(self) -> list[Comida]:
        return self.repo.get_all_comidas()

    def get_comida_by_id(self, id: uuid.UUID) -> Comida:
        comida = self.repo.get_comida_by_id(id)
        if not comida:
            raise HTTPException(status_code=404, detail="Comida not found")
        return comida

    def create_comida(self, comida: ComidaCreate) -> Comida:
        return self.repo.create_comida(comida)

    def update_comida(self, id: uuid.UUID, comida_data: ComidaCreate) -> Comida:
        updated_comida = self.repo.update_comida(id, comida_data)
        if not updated_comida:
            raise HTTPException(status_code=404, detail="Comida not found")
        return updated_comida

    def delete_comida(self, id: uuid.UUID):
        success = self.repo.delete_comida(id)
        if not success:
            raise HTTPException(status_code=404, detail="Comida not found")