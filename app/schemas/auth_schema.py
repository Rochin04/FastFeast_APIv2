from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: str | None = None
    user_type: str | None = None
