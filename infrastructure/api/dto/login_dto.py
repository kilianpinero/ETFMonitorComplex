from pydantic import BaseModel, EmailStr


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"
    email: EmailStr
    username: str
