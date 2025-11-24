from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.comerciante_repository import MerchantRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.comerciante_shcema import MerchantCreate
from app.models.comerciante_model import Merchant
import uuid

class ComercianteService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = MerchantRepository(session)
        self.usuario_repo = UsuarioRepository(session)

    def get_all_comerciantes(self) -> list[Merchant]:
        return self.repo.get_all_comerciantes()

    def get_comerciante_by_id(self, id: uuid.UUID) -> Merchant:
        comerciante = self.repo.get_comerciante_by_id(id)
        if not comerciante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comerciante not found")
        return comerciante

    def create_comerciante(self, comerciante: MerchantCreate) -> Merchant:
        # Validar si el usuario propietario existe
        usuario = self.usuario_repo.get_usuario_by_id(comerciante.owner_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id '{comerciante.owner_id}' no existe."
            )
        
        return self.repo.create_comerciante(comerciante)

    def update_comerciante(self, id: uuid.UUID, comerciante_data: MerchantCreate) -> Merchant:
        updated_comerciante = self.repo.update_comerciante(id, comerciante_data)
        if not updated_comerciante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comerciante not found")
        return updated_comerciante

    def delete_comerciante(self, id: uuid.UUID):
        success = self.repo.delete_comerciante(id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comerciante not found")
