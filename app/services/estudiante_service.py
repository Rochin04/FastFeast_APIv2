from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.estudiante_repository import EstudianteRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.estudiante_schema import EstudianteCreate, EstudianteUpdate
from app.models.estudiante_model import Estudiante
import uuid

class EstudianteService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = EstudianteRepository(session)
        self.usuario_repo = UsuarioRepository(session)

    def get_all_estudiantes(self) -> list[Estudiante]:
        return self.repo.get_all_estudiantes()

    def get_estudiante_by_id(self, user_id: uuid.UUID) -> Estudiante:
        estudiante = self.repo.get_estudiante_by_id(user_id)
        if not estudiante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante not found")
        return estudiante

    def create_estudiante(self, estudiante: EstudianteCreate) -> Estudiante:
        # Validar si el usuario existe
        usuario = self.usuario_repo.get_usuario_by_id(estudiante.user_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id '{estudiante.user_id}' no existe."
            )
        
        return self.repo.create_estudiante(estudiante)

    def update_estudiante(self, user_id: uuid.UUID, estudiante_data: EstudianteUpdate) -> Estudiante:
        updated_estudiante = self.repo.update_estudiante(user_id, estudiante_data)
        if not updated_estudiante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante not found")
        return updated_estudiante

    def delete_estudiante(self, user_id: uuid.UUID):
        success = self.repo.delete_estudiante(user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante not found")
