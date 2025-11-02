from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from infrastructure.api.auth.auth import hash_password, verify_password, create_auth_tokens
from infrastructure.repository.user_repository import UserRepository
from infrastructure.api.dto.login_dto import LoginResponse

router = APIRouter()
users = UserRepository()

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    user_data = {"sub": user.email, "id": str(user.id), "username": user.username}
    tokens = create_auth_tokens(user_data)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "expires_in": tokens["expires_in"],
        "token_type": "bearer",
        "email": user.email,
        "username": user.username
    }

@router.post("/register")
def register(user: dict):
    try:
        hashed = hash_password(user["password"])
        users.create_user(username=user["username"], email=user["email"], password=hashed)
        return {"success": True, "message": "Usuario registrado correctamente."}
    except IntegrityError:
        raise HTTPException(status_code=409, detail="El usuario o email ya existe.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
