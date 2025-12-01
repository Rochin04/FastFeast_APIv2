from fastapi import APIRouter, Depends, status
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginRequest, LoginResponse

router = APIRouter()

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(login_data: LoginRequest, service: AuthService = Depends()):
    return service.authenticate_user(login_data)
