from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.auth_schema import LoginRequest, LoginResponse

class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.repo = UsuarioRepository(session)

    def authenticate_user(self, login_data: LoginRequest) -> LoginResponse:
        user = self.repo.get_usuario_by_email(login_data.email)
        
        if not user:
            return LoginResponse(success=False, message="Invalid email or password")
            
        # NOTE: Comparing plain text password as per current system design
        if user.password_hash != login_data.password:
            return LoginResponse(success=False, message="Invalid email or password")
            
        return LoginResponse(
            success=True, 
            message="Login successful",
            user_id=str(user.id),
            user_type=user.user_type
        )
