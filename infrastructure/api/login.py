from fastapi import APIRouter, Depends, HTTPException, Body, Request, Cookie, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from infrastructure.api.auth.auth import hash_password, verify_password, create_auth_tokens, refresh_access_token, get_current_user
from infrastructure.repository.user_repository import UserRepository
import os

router = APIRouter()
users = UserRepository()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../../web'))

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    user_data = {"sub": user.email, "id": str(user.id), "username": user.username}
    tokens = create_auth_tokens(user_data)
    response = JSONResponse({
        "expires_in": tokens["expires_in"],
        "token_type": "bearer",
        "email": user.email,
        "username": user.username
    })
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False, # En producción, esto debería ser True si se usa HTTPS
        samesite="lax",
        max_age=tokens["expires_in"]
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False, # En producción, esto debería ser True si se usa HTTPS
        samesite="lax",
        max_age=60*60*24*7  # 7 días por ejemplo
    )
    return response

@router.post("/register")
def register(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    try:
        hashed = hash_password(password)
        users.create_user(username=username, email=email, password=hashed)
        return JSONResponse({"success": True, "message": "Usuario registrado correctamente."}, status_code=201)
    except IntegrityError:
        users.session.rollback()
        raise HTTPException(status_code=409, detail="El usuario o email ya existe.")
    except Exception as e:
        users.session.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/refresh")
def refresh_token_endpoint(refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=400, detail="refresh_token cookie is required")
    tokens = refresh_access_token(refresh_token)
    response = JSONResponse({
        "expires_in": tokens["expires_in"],
        "token_type": "bearer"
    })
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=tokens["expires_in"]
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60*60*24*7
    )
    return response

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    registered = request.query_params.get("registered")
    success_message = None
    if registered:
        success_message = "Usuario registrado correctamente. Ahora puedes iniciar sesión."
    return templates.TemplateResponse("login.html", {"request": request, "success_message": success_message})

@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/preferences", response_class=HTMLResponse)
def preferences_page(request: Request, access_token: str = Cookie(None)):
    is_authenticated = False
    if access_token:
        try:
            user = get_current_user(access_token)
            is_authenticated = True if user else False
        except Exception:
            is_authenticated = False
    return templates.TemplateResponse("preferences.html", {"request": request, "is_authenticated": is_authenticated})
