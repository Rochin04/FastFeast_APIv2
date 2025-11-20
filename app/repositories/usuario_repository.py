from sqlmodel import Session, select
from app.models.usuarios_model import Usuario
from app.schemas.usuarios_schema import UsuarioCreate, UsuarioUpdate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_usuarios(self) -> list[Usuario]:
        return self.session.exec(select(Usuario)).all()
    
    def get_usuario_by_id(self, id: uuid.UUID) -> Usuario | None:
        return self.session.get(Usuario, id)
    
    def create_usuario(self, usuario: UsuarioCreate) -> Usuario:
        db_usuario = Usuario.model_validate(usuario)
        self.session.add(db_usuario)
        try:
            self.session.commit()
            self.session.refresh(db_usuario)
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se pudo crear el usuario. El usuario con id '{usuario.id}' ya existe."
            )
        return db_usuario
        
    def update_usuario(self, id: uuid.UUID, usuario_data: UsuarioUpdate) -> Usuario | None:
        db_usuario = self.get_usuario_by_id(id)
        if db_usuario:
            db_usuario.email = usuario_data.email
            db_usuario.password_hash = usuario_data.password_hash
            self.session.add(db_usuario)
            self.session.commit()
            self.session.refresh(db_usuario)
        return db_usuario
    
    def delete_usuario(self, id: uuid.UUID) -> bool:
        db_usuario = self.get_usuario_by_id(id)
        if db_usuario:
            self.session.delete(db_usuario)
            self.session.commit()
            return True
        return False