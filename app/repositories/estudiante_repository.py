from sqlmodel import Session, select
from app.models.estudiante_model import Estudiante
from app.schemas.estudiante_schema import EstudianteCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import uuid

class EstudianteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_estudiantes(self) -> list[Estudiante]:
        return self.session.exec(select(Estudiante)).all()

    def get_estudiante_by_id(self, user_id: uuid.UUID) -> Estudiante | None:
        return self.session.get(Estudiante, user_id)

    def create_estudiante(self, estudiante: EstudianteCreate) -> Estudiante:
        db_estudiante = Estudiante.model_validate(estudiante)
        self.session.add(db_estudiante)
        try:
            self.session.commit()
            self.session.refresh(db_estudiante)
        except IntegrityError as e:
            self.session.rollback()
            error_msg = str(e.orig)
            if "students_student_id_number_key" in error_msg:
                 raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El número de estudiante '{estudiante.student_id_number}' ya está registrado."
                )
            if "fk_user" in error_msg or "students_pkey" in error_msg:
                 raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El usuario con id '{estudiante.user_id}' no existe o ya tiene un perfil de estudiante."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error de integridad al crear el estudiante."
            )
        return db_estudiante

    def update_estudiante(self, user_id: uuid.UUID, estudiante_data: EstudianteCreate) -> Estudiante | None:
        db_estudiante = self.get_estudiante_by_id(user_id)
        if db_estudiante:
            db_estudiante.student_id_number = estudiante_data.student_id_number
            db_estudiante.full_name = estudiante_data.full_name
            db_estudiante.profile_picture_url = estudiante_data.profile_picture_url
            db_estudiante.is_verified = estudiante_data.is_verified
            
            try:
                self.session.add(db_estudiante)
                self.session.commit()
                self.session.refresh(db_estudiante)
            except IntegrityError as e:
                self.session.rollback()
                if "students_student_id_number_key" in str(e.orig):
                     raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"El número de estudiante '{estudiante_data.student_id_number}' ya está registrado."
                    )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error de integridad al actualizar el estudiante."
                )
        return db_estudiante

    def delete_estudiante(self, user_id: uuid.UUID) -> bool:
        db_estudiante = self.get_estudiante_by_id(user_id)
        if db_estudiante:
            self.session.delete(db_estudiante)
            self.session.commit()
            return True
        return False
