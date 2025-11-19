from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.comidas_repository import ComidaRepository
from app.repositories.categorias_repository import CategoryRepository
# from app.repositories.comerciante_repository import comerciante_repository
from app.schemas.comida_shcema import ComidaCreate
from app.models.comida_model import Comida
import uuid

class ComidaService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = ComidaRepository(session)
        self.category_repo = CategoryRepository(session)

    def get_all_comidas(self) -> list[Comida]:
        return self.repo.get_all_comidas()

    def get_comida_by_id(self, id: uuid.UUID) -> Comida:
        comida = self.repo.get_comida_by_id(id)
        if not comida:
            raise HTTPException(status_code=404, detail="Comida not found")
        return comida

    def create_comida(self, comida: ComidaCreate) -> Comida:
        category = self.category_repo.get_category_by_id(comida.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, # 400 Bad Request es apropiado para IDs inválidos
                detail=f"Category with ID '{comida.category_id}' does not exist."
            )
        # merchant = self.merchant_repo.get_merchant_by_id(comida.merchant_id)
        # if not merchant:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f"Merchant with ID '{comida.merchant_id}' does not exist."
        #     )
        
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