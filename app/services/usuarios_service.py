from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuarios_schema import UsuarioCreate, UsuarioUpdate
from app.models.usuarios_model import Usuario
import uuid

class UsuarioService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = UsuarioRepository(session)
    
    def get_all_usuarios(self) -> list[Usuario]:
        return self.repo.get_all_usuarios()
    
    def get_usuario_by_id(self, id: uuid.UUID) -> Usuario:
        usuario = self.repo.get_usuario_by_id(id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario not found")
        return usuario

    def create_usuario(self, usuario: UsuarioCreate) -> Usuario:
        return self.repo.create_usuario(usuario)

    def update_usuario(self, id: uuid.UUID, usuario_data: UsuarioUpdate) -> Usuario:
        updated_usuario = self.repo.update_usuario(id, usuario_data)
        if not updated_usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario not found")
        return updated_usuario
        

    def delete_usuario(self, id: uuid.UUID):
        success = self.repo.delete_usuario(id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario not found")